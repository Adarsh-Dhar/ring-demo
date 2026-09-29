"""
Stands in for the real Ring Developers Playground's "live view event
simulation" feature (which fires Motion/Package/Vehicle events at your app).

Usage:
    python simulate_event.py night     # fires a motion event at 3:14 AM -> should notify
    python simulate_event.py day       # fires a motion event at 2:00 PM -> should be suppressed
    python simulate_event.py other-door  # fires event on a non-monitored device -> suppressed
"""
import sys
import requests
from datetime import datetime

WEBHOOK_URL = "http://localhost:5000/webhook"

SCENARIOS = {
    "night": {
        "id": "evt_001",
        "device_id": "front-door-cam-001",
        "type": "motion",
        "timestamp": datetime(2026, 9, 29, 3, 14, 0).isoformat(),
    },
    "day": {
        "id": "evt_002",
        "device_id": "front-door-cam-001",
        "type": "motion",
        "timestamp": datetime(2026, 9, 29, 14, 0, 0).isoformat(),
    },
    "other-door": {
        "id": "evt_003",
        "device_id": "backyard-cam-002",
        "type": "motion",
        "timestamp": datetime(2026, 9, 29, 3, 20, 0).isoformat(),
    },
}

if __name__ == "__main__":
    scenario = sys.argv[1] if len(sys.argv) > 1 else "night"
    if scenario not in SCENARIOS:
        print(f"Unknown scenario '{scenario}'. Choose from: {list(SCENARIOS.keys())}")
        sys.exit(1)

    event = SCENARIOS[scenario]
    print(f"🎬 Simulating event: {scenario} -> {event}")
    resp = requests.post(WEBHOOK_URL, json=event, timeout=5)
    print(f"Server responded: {resp.status_code} {resp.json()}")
