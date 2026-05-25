#!/usr/bin/env python3
"""LLM judge applying the durability rubric (PLAN.md §7.1).

Input: a candidate item — Gustaf's post text, and/or the content of a URL he shared.
Output: {verdict: save|skip, confidence, register_hint, kind_hint, tags_hint, reason}.

Cached by content hash. Re-runs are free.
"""
from __future__ import annotations
import hashlib, json, os, subprocess, time
from dataclasses import dataclass, asdict
from typing import Optional


class TokenLimitError(Exception):
    """Raised when the claude subprocess signals a usage/token/session limit."""
    pass


# Substrings in claude stdout/stderr that mean "stop the bulk run", not "retry".
_TOKEN_LIMIT_SIGNALS = (
    'usage limit',
    'session limit',       # claude CLI OAuth session cap
    'hit your session',    # "You've hit your session limit …"
    'hit your usage',
    'rate limit',
    'rate_limit',
    'out of tokens',
    'token limit',
    'context limit',
    'maximum context',
    'context window',
    'billing',
    'quota',
    'insufficient_quota',
    'out of credit',
    'out of credits',
    'no credits',
    'not enough credit',
    'credit balance',
    'spend limit',
    'capacity',
    'temporarily unavailable',
    'please try again',
    'too many requests',
    'overloaded',
    '429',
    'resets ',             # "resets 10am (Europe/Stockholm)" on session limit
)


def is_token_limit_message(text: str) -> bool:
    """True if *text* looks like a Claude usage/session/rate/credit limit (not a generic bug)."""
    if not text:
        return False
    low = text.lower()
    if any(sig in low for sig in _TOKEN_LIMIT_SIGNALS):
        return True
    # Bulk run logged thousands of these when the CLI exited 1 with empty capture.
    if 'claude exited 1' in low:
        return True
    return False


def is_retriable_judge_error(error: str) -> bool:
    """True if a prior judge-error should be retried on the next bulk run.

    Almost all logged failures are empty ``claude exited 1`` from session/credit limits
    (before TokenLimitError stopped the run). Those must retry after the limit resets.

    Non-retriable: model returned prose instead of JSON (missing content in prompt) — rare.
    """
    if not error or not error.strip():
        return True
    if is_token_limit_message(error):
        return True
    low = error.lower()
    if 'claude exited 1' in low:
        return True
    if 'timed out' in low or 'timeout' in low:
        return True
    if 'no json' in low:
        return False
    if 'valueerror' in low and 'no json' in low:
        return False
    # Unknown — retry once more rather than leave stuck
    return True

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(HERE)
STAGING = os.path.join(PROJECT, 'staging')
CACHE = os.path.join(STAGING, 'judged')
os.makedirs(CACHE, exist_ok=True)

MODEL = os.environ.get('FB_JUDGE_MODEL', 'claude-haiku-4-5')
CLAUDE_BIN = os.environ.get('CLAUDE_BIN', '/Users/dante/.local/bin/claude')


def _call_claude(system: str, user: str, timeout: int = 90) -> str:
    """Invoke `claude -p` non-interactively. Uses OAuth from keychain."""
    cmd = [
        CLAUDE_BIN, '-p',
        '--model', MODEL,
        '--append-system-prompt', system,
        # keep it minimal: no MCP, no plugins, no skills
        '--disable-slash-commands',
        '--strict-mcp-config', '--mcp-config', '{"mcpServers":{}}',
        # belt + braces: disallow all tools so the subprocess just answers
        '--disallowedTools', 'Bash,Edit,Write,Read,Glob,Grep,Agent,Task,WebFetch,WebSearch',
    ]
    try:
        proc = subprocess.run(
            cmd, input=user, capture_output=True, text=True, timeout=timeout
        )
    except subprocess.TimeoutExpired as e:
        raise RuntimeError(f'claude timed out after {timeout}s')

    stdout = proc.stdout or ''
    stderr = proc.stderr or ''
    combined = stdout + stderr
    out_stripped = stdout.strip()
    err_stripped = stderr.strip()
    combined_stripped = (out_stripped + err_stripped).strip()

    if proc.returncode != 0:
        detail = (combined_stripped or f'exit {proc.returncode}')[:500]
        if (is_token_limit_message(combined)
                or is_token_limit_message(stdout)
                or is_token_limit_message(stderr)):
            raise TokenLimitError(f'Claude limit (exit {proc.returncode}): {detail}')
        # CLI often returns exit 1 with no piped output when session/credits are exhausted.
        if proc.returncode == 1 and not combined_stripped:
            raise TokenLimitError(
                f'Claude limit (exit 1, no output — likely usage/session/credits): {detail}'
            )
        raise RuntimeError(f'claude exited {proc.returncode}: {detail}')
    # Only check for limit signals on exit 0 if stdout doesn't look like a valid response.
    # The CLI sometimes writes usage info (e.g. "context resets at…") to stderr even on
    # success, causing false positives when checking the combined stdout+stderr.
    stdout_has_verdict = '"verdict"' in stdout
    if not stdout_has_verdict and is_token_limit_message(stderr):
        raise TokenLimitError(f'Claude limit (exit 0, stderr): {err_stripped[:500]}')
    return stdout


RUBRIC = """You are curating Gustaf's external brain (an Obsidian vault). He is importing 20 years of his own Facebook posts and the links he shared.

You receive ONE candidate item. Decide whether it deserves to live as its own note in the vault.

# Save the item if it:
- Contains durable knowledge, ideas, frameworks, or insights that remain useful over time
- Explores causality, mechanisms, patterns, or principles (not just events)
- Shares perspective, analysis, or expertise worth building on
- Could deepen understanding of a topic, domain, or human experience
- **Clearly asserts a principle or value** that reveals what Gustaf finds important — even if stated plainly rather than argued at length. A crisp position on how something should work counts. "X is Y's job, not Z's" or "private entities have the right to do X" are enough if the principle itself is non-trivial.

# Do NOT save if it:
- Is primarily a news announcement or time-bound event report
- Is social banter, small talk, or relational exchange with no embedded knowledge
- Describes that something happened without explaining why or what it means
- Is promotional, transactional, or logistical in nature

# Item types
- `own_text`        — Gustaf wrote this. No external link, or the link was incidental.
- `own_commentary`  — Gustaf's commentary attached to a shared link.
- `shared_article`  — The content of a URL Gustaf shared (possibly without commentary).
- `shared_video`    — Video metadata (title, description) from YouTube/Vimeo/etc.
- `shared_podcast`  — Podcast episode metadata.

# Special: paywalled articles
If the input includes `fetch_note: paywall — only title and commentary available`, do NOT
penalize the article for being paywalled. Judge by the title + Gustaf's commentary alone.
If those signal durable substance, save. We have no way to read the body, so absence of
fetched text is not evidence of low quality.

# Special: thin video/podcast metadata
If the only signal is a generic title (no description, no transcript), be willing to save
if (a) the title alone suggests durable subject matter (named expert, named concept,
specific framework) AND/OR (b) Gustaf's commentary makes the connection explicit. Don't
require deep evidence we cannot access.

# Register hint (if save)
- `voice`    — Polished, finished prose by Gustaf. Rare. Manifestos, essays.
- `thinking` — Gustaf's view in fragments or paragraphs. Most own_text/own_commentary saves land here.
- `consumed` — External authored content (shared_article, shared_video, shared_podcast).

# Output
Respond with ONLY a JSON object, no prose:
{
  "verdict": "save" | "skip",
  "confidence": 0.0-1.0,
  "register_hint": "voice" | "thinking" | "consumed" | null,
  "kind_hint": "article" | "video" | "podcast" | "book" | "clipping" | "note" | null,
  "tags_hint": [up to 3 kebab-case English tags, or branded proper-name tags like "burning-man" or "the-borderland"],
  "reason": "one short sentence — why this verdict"
}
"""


@dataclass
class Judgement:
    verdict: str          # save|skip|error
    confidence: float
    register_hint: Optional[str]
    kind_hint: Optional[str]
    tags_hint: list
    reason: str
    model: str
    item_type: str
    content_sha: str
    error: str = ''


def _atomic_write_json(path: str, data) -> None:
    """tmp + rename so a mid-write kill never corrupts the cache."""
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def hash_item(item_type: str, payload: dict) -> str:
    """Content hash for judged/ cache filenames."""
    h = hashlib.sha1()
    h.update(item_type.encode())
    h.update(b'\0')
    h.update(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode())
    return h.hexdigest()[:20]


_hash_item = hash_item  # backward compat


def judgement_cache_path(item_type: str, payload: dict) -> str:
    return os.path.join(CACHE, hash_item(item_type, payload) + '.json')


def load_cached_judgement(item_type: str, payload: dict) -> Optional[Judgement]:
    path = judgement_cache_path(item_type, payload)
    if not os.path.exists(path):
        return None
    with open(path, encoding='utf-8') as f:
        return Judgement(**json.load(f))


def judge(item_type: str, payload: dict, *, retries: int = 2) -> Judgement:
    """item_type: own_text|own_commentary|shared_article|shared_video|shared_podcast
    payload keys (any subset):
      text: Gustaf's text
      url: source url (if any)
      title: page/video title
      author: author/channel
      domain: domain
      date: ISO date
      fetched_text: extracted body of the URL
    """
    sha = hash_item(item_type, payload)
    cache_path = os.path.join(CACHE, sha + '.json')
    if os.path.exists(cache_path):
        with open(cache_path) as f:
            return Judgement(**json.load(f))

    # Build user message
    parts = [f'Item type: {item_type}']
    for k in ('date', 'url', 'domain', 'title', 'author', 'fetch_note'):
        v = payload.get(k)
        if v:
            parts.append(f'{k}: {v}')
    if payload.get('text'):
        parts.append(f"\nGustaf's text:\n---\n{payload['text'][:4000]}\n---")
    if payload.get('fetched_text'):
        parts.append(f"\nFetched content (truncated):\n---\n{payload['fetched_text'][:6000]}\n---")
    user_msg = '\n'.join(parts)

    last_err = ''
    for attempt in range(retries + 1):
        try:
            raw = _call_claude(RUBRIC, user_msg)
            data = _parse_json(raw)
            j = Judgement(
                verdict=data.get('verdict', 'skip'),
                confidence=float(data.get('confidence', 0.0)),
                register_hint=data.get('register_hint'),
                kind_hint=data.get('kind_hint'),
                tags_hint=data.get('tags_hint') or [],
                reason=data.get('reason', ''),
                model=MODEL,
                item_type=item_type,
                content_sha=sha,
            )
            _atomic_write_json(cache_path, asdict(j))
            return j
        except TokenLimitError:
            raise  # propagate immediately — don't retry, don't cache
        except Exception as e:
            last_err = f'{type(e).__name__}: {e}'
            if is_token_limit_message(last_err) or is_token_limit_message(str(e)):
                raise TokenLimitError(last_err) from e
            time.sleep(1.5 * (attempt + 1))

    if is_token_limit_message(last_err):
        raise TokenLimitError(last_err)
    j = Judgement('error', 0.0, None, None, [], '', MODEL, item_type, sha, error=last_err)
    return j


def _parse_json(raw: str) -> dict:
    raw = raw.strip()
    if raw.startswith('```'):
        raw = raw.split('```', 2)[1]
        if raw.startswith('json'):
            raw = raw[4:]
        raw = raw.rsplit('```', 1)[0]
    # find first { and last }
    a = raw.find('{')
    b = raw.rfind('}')
    if a < 0 or b < 0:
        raise ValueError(f'no json in: {raw[:200]}')
    return json.loads(raw[a:b+1])


if __name__ == '__main__':
    import sys
    payload = {'text': sys.argv[1] if len(sys.argv) > 1 else 'hej hej grattis på födelsedagen'}
    print(json.dumps(asdict(judge('own_text', payload)), indent=2, ensure_ascii=False))
