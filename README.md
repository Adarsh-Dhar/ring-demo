# Wander Watch — MVP (v1, rules-only)

A minimal, working proof of the core mechanism: a Ring door/motion event during
a defined "quiet hours" window triggers a notification; everything else is
suppressed.

## What was just run and proven (in this sandbox, against a mock Ring API)

This sandbox can't reach Amazon's real Ring API domains, so a local mock
server (`mock_ring_server.py`) stands in for it. Three scenarios were fired
at the webhook server and behaved correctly:

| Scenario | Device | Time | Result |
|---|---|---|---|
| `night` | front-door-cam-001 (monitored) | 3:14 AM | ✅ Notification sent |
| `day` | front-door-cam-001 (monitored) | 2:00 PM | 🔕 Suppressed — outside quiet hours |
| `other-door` | backyard-cam-002 (not monitored) | 3:20 AM | 🔕 Suppressed — wrong device |

This confirms the actual decision logic (`decision.py`) is correct:
quiet-hours window handling (including the overnight midnight-crossing case),
device filtering, and the notify/suppress branch all work as intended.

## Files

- `config.py` — all settings (API base URL, token, monitored device, quiet hours)
- `ring_client.py` — the real Ring API calls (list devices, device status, event clip)
- `decision.py` — the core rules engine (quiet hours + device filter). This is
  also where the AI Agent 1 (perception) / Agent 2 (decision) steps would plug
  in later — marked with `NOTE:` comments.
- `webhook_server.py` — receives events, runs them through `decision.py`, and
  "sends" a notification (currently just prints/logs it)
- `mock_ring_server.py` — local stand-in for Ring's real API (delete when going live)
- `simulate_event.py` — fires test events at the webhook server, standing in
  for the Ring Developers Playground's live event simulation feature
- `.env` — your configuration (currently set to mock values)

## How to run it yourself (same as what was just demonstrated)

**Option A — one command:**
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
chmod +x run_demo.sh
./run_demo.sh
```
This starts both servers, fires all three test scenarios, prints the results, and shuts everything down cleanly.

**Option B — manual, three terminals (useful while actively developing):**
```bash
pip install -r requirements.txt
cp .env.example .env

# Terminal 1
python mock_ring_server.py

# Terminal 2
python webhook_server.py

# Terminal 3 — fire test events
python simulate_event.py night        # should notify
python simulate_event.py day          # should suppress
python simulate_event.py other-door   # should suppress

# Check the log
curl http://localhost:5000/log
```

## How to go live against the real Ring Developers Playground

1. Go to `developer.amazon.com/ring`, open the **Ring Developers Playground**,
   click **Generate Token** (valid ~30 min).
2. Copy `.env.example` to `.env` if you haven't already, then edit `.env`:
   ```
   RING_API_BASE=https://api.amazonvision.com
   RING_ACCESS_TOKEN=<paste your real token here>
   ```
3. Run `python ring_client.py` — you should see your *real* Ring devices
   printed instead of the two mock ones.
4. Set `MONITORED_DEVICE_ID` in `.env` to the real device ID that came back.
5. For real events to reach your webhook, you need a public HTTPS URL. During
   development, run `ngrok http 5000` and register the ngrok URL + `/webhook`
   as your app's webhook endpoint in the Ring Developer Portal.
6. In the Playground, use the live event simulation feature (Motion/Package/
   Vehicle) to fire a real simulated event at your real webhook — same
   end-to-end flow you just saw locally, now against Ring's actual sandbox.

**Never commit your real `.env` file or paste your real token anywhere public.**

## What's next (not built yet)

- Real push delivery (Firebase Cloud Messaging) instead of print statements
- SQLite/Postgres instead of the in-memory event log
- The AI pipeline: Agent 1 (Bedrock vision — is a person present, describe
  the scene) and Agent 2 (decide notify/suppress/escalate using that
  description) — see the `NOTE:` markers in `decision.py` for where this goes
- A simple dashboard frontend for the `/log` data
- Dismiss/escalate buttons on the notification itself
# ring-demo
