#!/usr/bin/env bash
# One-command demo: starts the mock Ring API + webhook server, fires all
# three test scenarios, prints the results, then shuts everything down.
#
# Usage:
#   chmod +x run_demo.sh
#   ./run_demo.sh
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="$DIR/venv/bin/python"

if [ ! -f "$PY" ]; then
    echo "No venv found - using system python3 instead. (Run 'pip install -r requirements.txt' first if this fails.)"
    PY="python3"
fi

if [ ! -f "$DIR/.env" ]; then
    echo "No .env found - copying .env.example -> .env (mock values, safe for local testing)"
    cp "$DIR/.env.example" "$DIR/.env"
fi

echo "Starting mock Ring API on :5001 ..."
"$PY" "$DIR/mock_ring_server.py" > "$DIR/mock_server.log" 2>&1 &
MOCK_PID=$!

echo "Starting webhook server on :5000 ..."
"$PY" "$DIR/webhook_server.py" > "$DIR/webhook_server.log" 2>&1 &
WEBHOOK_PID=$!

cleanup() {
    echo ""
    echo "Shutting down..."
    kill "$MOCK_PID" "$WEBHOOK_PID" 2>/dev/null || true
}
trap cleanup EXIT

sleep 2

echo ""
echo "=== STEP 1: list_devices (confirms API connectivity) ==="
(cd "$DIR" && "$PY" ring_client.py)

echo ""
echo "=== STEP 2: night event (3:14 AM, monitored door) -> expect NOTIFY ==="
(cd "$DIR" && "$PY" simulate_event.py night)
sleep 1

echo ""
echo "=== STEP 3: day event (2:00 PM, monitored door) -> expect SUPPRESS ==="
(cd "$DIR" && "$PY" simulate_event.py day)
sleep 1

echo ""
echo "=== STEP 4: night event on a different door -> expect SUPPRESS ==="
(cd "$DIR" && "$PY" simulate_event.py other-door)
sleep 1

echo ""
echo "=== STEP 5: full event log ==="
curl -s http://localhost:5000/log | python3 -m json.tool

echo ""
echo "=== Webhook server console output ==="
cat "$DIR/webhook_server.log"
