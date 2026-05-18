#!/usr/bin/env node
const { execSync } = require('node:child_process');
const path = require('node:path');

const repoRoot = path.resolve(__dirname, '..');
const host = require('/Users/dante/code/obsidian-mcp-host/server.js');

function run(command) {
  return execSync(command, {
    cwd: repoRoot,
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
    env: process.env,
  }).trim();
}

function safeRun(command) {
  try {
    return { ok: true, output: run(command) };
  } catch (error) {
    return {
      ok: false,
      output: String(error.stdout || '').trim(),
      error: String(error.stderr || error.message || error).trim(),
    };
  }
}

(async () => {
  const summary = {
    repoRoot,
    branch: null,
    pull: null,
    processedThoughts: [],
    unsupportedInboxItems: [],
    commit: null,
    push: null,
  };

  summary.branch = run('git branch --show-current');
  summary.pull = safeRun(`git pull --rebase --autostash origin ${summary.branch}`);
  if (!summary.pull.ok) {
    throw new Error(`git pull failed: ${summary.pull.error || summary.pull.output}`);
  }

  const inboxItems = await host.listInboxItems({ processed: false, limit: 1000 });
  for (const item of inboxItems) {
    if (item.path.startsWith('inbox/thoughts/')) {
      const result = await host.processThoughtInboxNote(item.path, { sessionLabel: 'cron-inbox-sync' });
      summary.processedThoughts.push({ path: item.path, result });
    } else {
      summary.unsupportedInboxItems.push(item.path);
    }
  }

  const status = run('git status --porcelain');
  if (status) {
    run('git add .');
    const commitMessage = `brain: process inbox ${new Date().toISOString()}`;
    summary.commit = safeRun(`git commit -m ${JSON.stringify(commitMessage)}`);
    if (!summary.commit.ok) {
      throw new Error(`git commit failed: ${summary.commit.error || summary.commit.output}`);
    }
    summary.push = safeRun(`git push origin ${summary.branch}`);
    if (!summary.push.ok) {
      throw new Error(`git push failed: ${summary.push.error || summary.push.output}`);
    }
  }

  console.log(JSON.stringify(summary, null, 2));
})().catch((error) => {
  console.error(error.stack || String(error));
  process.exit(1);
});
