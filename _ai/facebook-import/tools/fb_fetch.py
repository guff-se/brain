#!/usr/bin/env python3
"""Polite URL fetcher with HTML cache, Wayback fallback, and readability extraction.

Used by Phase 4/5 to pull the content of shared links so they can be judged.
"""
from __future__ import annotations
import hashlib, json, os, subprocess, time, re
from dataclasses import dataclass, asdict
from urllib.parse import urlparse, urlunparse, quote_plus
from typing import Optional

import httpx
import trafilatura

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(HERE)
STAGING = os.path.join(PROJECT, 'staging')
CACHE_HTML = os.path.join(STAGING, 'fetched')
CACHE_META = os.path.join(STAGING, 'fetched_meta')
os.makedirs(CACHE_HTML, exist_ok=True)
os.makedirs(CACHE_META, exist_ok=True)

UA = 'Mozilla/5.0 (Macintosh; gustaf-vault-importer) FacebookExportIngest/0.1'

# Domain rules from PLAN.md §7.2
SKIP_DOMAINS = {
    # Forms
    'docs.google.com', 'forms.gle',
    # Shorteners (resolve, don't ingest the shortener itself)
    # (handled separately as RESOLVERS below)
    # Meme/image hosts
    'imgur.com', 'i.imgur.com', 'm.imgur.com', 'media1.tenor.co', 'media.tenor.com',
    'tenor.com', 'giphy.com', 'media.giphy.com',
}

# *.typeform.com is a wildcard skip
SKIP_SUFFIXES = ('.typeform.com',)

# Resolve these and treat as their destination
SHORTENER_DOMAINS = {'t.co', 'bit.ly', 'buff.ly', 'goo.gl', 'wired.trib.al', 'lnkd.in', 'ow.ly', 'tinyurl.com', 'fb.me', 'l.facebook.com', 'm.facebook.com'}

# Own domains — handled as facts references, not consumed
OWN_DOMAINS = {
    'guff.se', 'theborderland.se', 'wiki.theborderland.se', 'talk.theborderland.se',
    'dreams.theborderland.se', 'entreprenorsjakten.se', 'imbuedart.com', 'makerspark.se',
    'incrediblemusicmachine.se', 'guff.typeform.com',
}

# Route to kind
VIDEO_DOMAINS = {'youtube.com', 'youtu.be', 'm.youtube.com', 'vimeo.com', 'svtplay.se'}
PODCAST_DOMAINS = {'open.spotify.com', 'soundcloud.com'}
BOOK_DOMAINS = {'adlibris.com', 'bokus.com', 'goodreads.com'}

# Paywall-heavy sites: prefer Wayback first (often has the full article cached)
PAYWALL_DOMAINS = {
    'dn.se', 'mobil.dn.se', 'svd.se', 'di.se', 'digital.di.se', 'sydsvenskan.se',
    'gp.se', 'expressen.se', 'nytimes.com', 'washingtonpost.com', 'wsj.com',
    'ft.com', 'telegraph.co.uk', 'economist.com', 'newyorker.com', 'bloomberg.com',
    'esvd.svd.se', 'na.se', 'hd.se', 'bbc.com', 'newscientist.com', 'wired.com',
    'theatlantic.com', 'breakit.se', 'va.se', 'resume.se', 'aftonbladet.se',
}

# Markers that signal we hit a paywall stub even though status was 200
PAYWALL_MARKERS = (
    'logga in för att fortsätta läsa', 'är du redan prenumerant',
    'läs gratis i 3 månader', 'subscribe to continue', 'subscribers only',
    'paywall', 'this article is for subscribers', 'become a subscriber',
)


def looks_paywalled(text: str) -> bool:
    if not text or len(text) > 1500:
        return False
    low = text.lower()
    return any(m in low for m in PAYWALL_MARKERS)


def domain_of(url: str) -> str:
    try:
        d = urlparse(url).netloc.lower()
        return d[4:] if d.startswith('www.') else d
    except Exception:
        return ''


def classify_domain(url: str) -> dict:
    """Return {action: skip|resolve|own|fetch, kind: article|video|podcast|book|own|None, reason}"""
    d = domain_of(url)
    if not d:
        return {'action': 'skip', 'kind': None, 'reason': 'no-domain'}
    if d.endswith(SKIP_SUFFIXES) or d in SKIP_DOMAINS:
        return {'action': 'skip', 'kind': None, 'reason': 'skip-domain'}
    if d in SHORTENER_DOMAINS:
        return {'action': 'resolve', 'kind': None, 'reason': 'shortener'}
    if d in OWN_DOMAINS:
        return {'action': 'own', 'kind': 'own', 'reason': 'own-domain'}
    if d in VIDEO_DOMAINS:
        return {'action': 'fetch', 'kind': 'video', 'reason': 'video-route'}
    if d in PODCAST_DOMAINS:
        return {'action': 'fetch', 'kind': 'podcast', 'reason': 'podcast-route'}
    if d in BOOK_DOMAINS:
        return {'action': 'fetch', 'kind': 'book', 'reason': 'book-route'}
    return {'action': 'fetch', 'kind': 'article', 'reason': 'default'}


def _sha(url: str) -> str:
    return hashlib.sha1(url.encode('utf-8')).hexdigest()[:16]


def _wayback_url(url: str) -> Optional[str]:
    """Ask Wayback for the closest snapshot. Returns the snapshot URL or None."""
    try:
        r = httpx.get('https://archive.org/wayback/available',
                      params={'url': url}, timeout=10.0,
                      headers={'User-Agent': UA})
        if r.status_code != 200:
            return None
        data = r.json()
        snap = data.get('archived_snapshots', {}).get('closest')
        if snap and snap.get('available'):
            return snap.get('url')
    except Exception:
        return None
    return None


@dataclass
class FetchResult:
    url: str
    final_url: str
    domain: str
    kind: str            # article|video|podcast|book|own
    action: str          # ok|wayback|failed|skipped|own|paywalled
    status: int
    title: str
    author: str
    text: str            # extracted readable text
    text_len: int
    cached_html: str     # path to cached html, '' if none
    note: str            # extra info / reason for failure
    extra: dict = None   # type-specific metadata (video desc, podcast show, mp3 url, etc.)


def fetch(url: str, *, allow_wayback: bool = True, throttle: float = 1.0) -> FetchResult:
    """Fetch a URL, with caching. Returns FetchResult."""
    sha = _sha(url)
    meta_path = os.path.join(CACHE_META, sha + '.json')
    if os.path.exists(meta_path):
        with open(meta_path) as f:
            data = json.load(f)
            data.setdefault('extra', None)
            return FetchResult(**data)

    cls = classify_domain(url)
    if cls['action'] == 'skip':
        res = FetchResult(url, url, domain_of(url), cls['kind'] or 'skip', 'skipped', 0,
                          '', '', '', 0, '', cls['reason'], None)
        _save_meta(meta_path, res)
        return res
    if cls['action'] == 'own':
        res = FetchResult(url, url, domain_of(url), 'own', 'own', 0,
                          '', '', '', 0, '', 'own-domain', None)
        _save_meta(meta_path, res)
        return res

    target = url
    if cls['action'] == 'resolve':
        try:
            with httpx.Client(timeout=15.0, follow_redirects=True, headers={'User-Agent': UA}) as c:
                r = c.head(url)
                resolved = str(r.url)
                if resolved and domain_of(resolved) not in SHORTENER_DOMAINS:
                    target = resolved
        except Exception:
            pass
        time.sleep(throttle)
        cls = classify_domain(target)
        if cls['action'] in ('skip', 'own'):
            res = FetchResult(url, target, domain_of(target), cls['kind'] or cls['action'],
                              'skipped' if cls['action'] == 'skip' else 'own',
                              0, '', '', '', 0, '', f'shortener->{cls["reason"]}', None)
            _save_meta(meta_path, res)
            return res

    # Route by kind
    if cls['kind'] == 'video':
        res = _fetch_video(url, target, throttle)
        _save_meta(meta_path, res)
        return res
    if cls['kind'] == 'podcast':
        res = _fetch_podcast(url, target, throttle)
        _save_meta(meta_path, res)
        return res

    res = _fetch_article(url, target, cls, allow_wayback, throttle, sha)
    _save_meta(meta_path, res)
    return res


def _fetch_article(orig_url: str, target: str, cls: dict, allow_wayback: bool,
                   throttle: float, sha: str) -> FetchResult:
    dom = domain_of(target)
    paywall_first = dom in PAYWALL_DOMAINS
    html, status, final_url = None, 0, target
    note = ''

    if paywall_first and allow_wayback:
        # Try Wayback first — paywall sites typically return stubs live
        wb = _wayback_url(target)
        if wb:
            html, status, final_url = _live_get(wb, throttle)
            if html:
                note = 'wayback-first'
        if html is None:
            html, status, final_url = _live_get(target, throttle)
            if html:
                # check if it's a paywall stub
                _, _, sniff = _extract(html, target)
                if looks_paywalled(sniff):
                    note = 'paywall-stub'
    else:
        # Live first
        html, status, final_url = _live_get(target, throttle)
        if html:
            _, _, sniff = _extract(html, target)
            if looks_paywalled(sniff) and allow_wayback:
                wb = _wayback_url(target)
                if wb:
                    html2, status2, final_url2 = _live_get(wb, throttle)
                    if html2:
                        _, _, sniff2 = _extract(html2, target)
                        if not looks_paywalled(sniff2) and len(sniff2) > len(sniff):
                            html, status, final_url = html2, status2, wb
                            note = 'wayback-paywall'
                        else:
                            note = 'paywall-stub'
                    else:
                        note = 'paywall-stub'
                else:
                    note = 'paywall-stub'
        if html is None and allow_wayback:
            wb = _wayback_url(target)
            if wb:
                html2, status2, final_url2 = _live_get(wb, throttle)
                if html2:
                    html, status, final_url = html2, status2, wb
                    note = 'wayback'

    if html is None:
        return FetchResult(orig_url, target, dom, cls['kind'] or 'article',
                           'failed', status, '', '', '', 0, '', 'fetch-failed', None)

    html_path = os.path.join(CACHE_HTML, sha + '.html')
    try:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
    except Exception:
        html_path = ''

    title, author, text = _extract(html, target)
    action = 'ok'
    if note == 'paywall-stub':
        action = 'paywalled'
    elif note.startswith('wayback'):
        action = 'wayback'
    return FetchResult(orig_url, final_url or target, domain_of(final_url or target),
                       cls['kind'] or 'article', action,
                       status, title, author, text, len(text), html_path, note, None)


def _fetch_video(orig_url: str, target: str, throttle: float) -> FetchResult:
    """Use yt-dlp to pull title, channel, description, duration. No video download."""
    try:
        proc = subprocess.run(
            ['yt-dlp', '--skip-download', '--no-warnings', '--no-playlist',
             '--dump-single-json', '--socket-timeout', '15', target],
            capture_output=True, text=True, timeout=60
        )
        time.sleep(throttle)
        if proc.returncode != 0 or not proc.stdout:
            return FetchResult(orig_url, target, domain_of(target), 'video',
                               'failed', 0, '', '', '', 0, '',
                               f'yt-dlp: {proc.stderr[:200]}', None)
        info = json.loads(proc.stdout)
        title = info.get('title') or ''
        author = info.get('uploader') or info.get('channel') or ''
        desc = info.get('description') or ''
        extra = {
            'duration_sec': info.get('duration'),
            'upload_date': info.get('upload_date'),
            'view_count': info.get('view_count'),
            'channel_url': info.get('channel_url'),
            'webpage_url': info.get('webpage_url'),
            'tags': info.get('tags') or [],
        }
        return FetchResult(orig_url, info.get('webpage_url') or target, domain_of(target),
                           'video', 'ok', 200, title, author, desc, len(desc),
                           '', 'yt-dlp', extra)
    except subprocess.TimeoutExpired:
        return FetchResult(orig_url, target, domain_of(target), 'video',
                           'failed', 0, '', '', '', 0, '', 'yt-dlp-timeout', None)
    except Exception as e:
        return FetchResult(orig_url, target, domain_of(target), 'video',
                           'failed', 0, '', '', '', 0, '', f'yt-dlp-error: {e}', None)


def _fetch_podcast(orig_url: str, target: str, throttle: float) -> FetchResult:
    """Spotify episode → oEmbed for metadata, then try iTunes RSS lookup for mp3."""
    dom = domain_of(target)
    title = ''
    author = ''
    desc = ''
    extra: dict = {}

    if 'spotify.com' in dom:
        try:
            r = httpx.get('https://open.spotify.com/oembed',
                          params={'url': target}, timeout=15.0,
                          headers={'User-Agent': UA})
            time.sleep(throttle)
            if r.status_code == 200:
                d = r.json()
                title = d.get('title', '')
                author = d.get('provider_name', '')
                extra['thumbnail_url'] = d.get('thumbnail_url')
        except Exception as e:
            extra['oembed_error'] = str(e)

        # Also try to fetch the spotify page directly — it has og:description
        try:
            html, _, _ = _live_get(target, throttle)
            if html:
                m = re.search(r'<meta[^>]+property="og:description"[^>]+content="([^"]+)"', html)
                if m:
                    desc = m.group(1)
                m2 = re.search(r'<meta[^>]+property="og:title"[^>]+content="([^"]+)"', html)
                if m2 and not title:
                    title = m2.group(1)
        except Exception:
            pass

        # Best-effort mp3 hunt via iTunes Search API (show → feed → match episode)
        # Heuristic: extract show name from title pattern "Episode Title - Show Name"
        if title:
            show_guess = title.split(' - ')[-1].strip() if ' - ' in title else title
            mp3 = _itunes_find_mp3(show_guess, title)
            if mp3:
                extra['mp3_url'] = mp3
                extra['mp3_source'] = 'itunes-rss'

        return FetchResult(orig_url, target, dom, 'podcast', 'ok' if title else 'failed',
                           200 if title else 0, title, author, desc, len(desc),
                           '', 'spotify-oembed', extra)

    # soundcloud or other: fall back to article fetch
    html, status, final_url = _live_get(target, throttle)
    if html is None:
        return FetchResult(orig_url, target, dom, 'podcast', 'failed', status,
                           '', '', '', 0, '', 'fetch-failed', None)
    title, author, text = _extract(html, target)
    return FetchResult(orig_url, final_url or target, dom, 'podcast', 'ok',
                       status, title, author, text, len(text), '', '', None)


def _itunes_find_mp3(show_query: str, episode_title: str) -> str:
    """Find an mp3 URL via iTunes Search → RSS feed → episode title match. Best-effort."""
    try:
        sr = httpx.get('https://itunes.apple.com/search',
                       params={'term': show_query, 'media': 'podcast', 'limit': 5},
                       timeout=10.0, headers={'User-Agent': UA})
        if sr.status_code != 200:
            return ''
        feeds = [r.get('feedUrl') for r in sr.json().get('results', []) if r.get('feedUrl')]
    except Exception:
        return ''

    ep_low = episode_title.lower().strip()
    for feed in feeds[:3]:
        try:
            fr = httpx.get(feed, timeout=15.0, headers={'User-Agent': UA},
                           follow_redirects=True)
            if fr.status_code != 200:
                continue
            xml = fr.text
            # find <item>…<title>…</title>…<enclosure url="…"…>
            for m in re.finditer(r'<item\b.*?</item>', xml, re.DOTALL):
                blk = m.group(0)
                tm = re.search(r'<title[^>]*>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>', blk, re.DOTALL)
                em = re.search(r'<enclosure[^>]+url="([^"]+)"', blk)
                if tm and em:
                    t = tm.group(1).strip().lower()
                    if t == ep_low or (len(ep_low) > 8 and ep_low in t) or (len(t) > 8 and t in ep_low):
                        return em.group(1)
        except Exception:
            continue
    return ''


def _live_get(url: str, throttle: float):
    try:
        with httpx.Client(timeout=20.0, follow_redirects=True, headers={'User-Agent': UA}) as c:
            r = c.get(url)
        time.sleep(throttle)
        if r.status_code >= 400:
            return None, r.status_code, str(r.url)
        ct = r.headers.get('content-type', '').lower()
        if 'html' not in ct and 'xml' not in ct:
            return None, r.status_code, str(r.url)
        return r.text, r.status_code, str(r.url)
    except Exception:
        return None, 0, url


def _extract(html: str, url: str):
    try:
        meta = trafilatura.extract_metadata(html, default_url=url)
        title = (meta.title if meta else '') or ''
        author = (meta.author if meta else '') or ''
    except Exception:
        title, author = '', ''
    try:
        text = trafilatura.extract(html, include_comments=False,
                                   include_tables=False, no_fallback=False,
                                   url=url) or ''
    except Exception:
        text = ''
    return title.strip(), author.strip() if author else '', text.strip()


def _save_meta(path: str, res: FetchResult):
    """Atomic write: tmp + rename. A mid-write kill never corrupts the cache."""
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(asdict(res), f, ensure_ascii=False, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


if __name__ == '__main__':
    import sys
    for u in sys.argv[1:]:
        r = fetch(u)
        print(json.dumps(asdict(r), ensure_ascii=False, indent=2)[:800])
