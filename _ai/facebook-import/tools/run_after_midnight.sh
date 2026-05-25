#!/usr/bin/env bash
# One-shot: sleep until 00:05 Europe/Stockholm, then run fb_bulk.py.
# PID written to staging/scheduled_bulk.pid — kill that PID to cancel.
set -euo pipefail

HERE="$(cd "$(dirname "$0")/.." && pwd)"
cd "$HERE"
LOG="$HERE/staging/scheduled_bulk.log"
PIDFILE="$HERE/staging/scheduled_bulk.pid"

echo $$ >"$PIDFILE"
trap 'rm -f "$PIDFILE"' EXIT

# Optional arg: local time HH:MM in Europe/Stockholm (default 00:05)
WHEN="${1:-00:05}"
SECS="$(python3 -c "
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import sys
tz = ZoneInfo('Europe/Stockholm')
now = datetime.now(tz)
when = sys.argv[1]
h, m = map(int, when.split(':'))
target = now.replace(hour=h, minute=m, second=0, microsecond=0)
if target <= now:
    target += timedelta(days=1)
print(int((target - now).total_seconds()))
" "$WHEN")"

TARGET="$(TZ=Europe/Stockholm date -v+${SECS}S '+%Y-%m-%d %H:%M:%S %Z' 2>/dev/null || TZ=Europe/Stockholm date -d "@$(($(date +%s) + SECS))" '+%Y-%m-%d %H:%M:%S %Z' 2>/dev/null || echo '00:05 Stockholm')"
{
  echo "=== scheduled bulk run ==="
  echo "armed: $(date)"
  echo "sleep: ${SECS}s (~${TARGET})"
} | tee -a "$LOG"

sleep "$SECS"

{
  echo "starting: $(date)"
  echo "---"
} | tee -a "$LOG"

set +e
.venv/bin/python tools/fb_bulk.py 2>&1 | tee -a "$LOG"
EXIT=${PIPESTATUS[0]}
set -e

{
  echo "---"
  echo "finished: $(date) exit=$EXIT"
} | tee -a "$LOG"

echo "AGENT_LOOP_WAKE_fb_bulk {\"prompt\":\"Facebook bulk import finished (exit ${EXIT}). Check _ai/facebook-import/staging/scheduled_bulk.log; re-run fb_bulk.py if exit was 2 (limit).\",\"exit\":${EXIT}}"
