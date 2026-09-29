"""
Webhook receiver for Ring events.

In real usage, you register this endpoint's public HTTPS URL (via ngrok or
similar during dev) with your Ring app so Ring POSTs events here as they
happen. For now it works identically against our local mock event sender
(simulate_event.py).
"""
from flask import Flask, request, jsonify
from datetime import datetime
from decision import should_notify
from config import MONITORED_DEVICE_ID, QUIET_HOURS_START, QUIET_HOURS_END

app = Flask(__name__)

# In-memory event log for this demo. A real app would use a database.
EVENT_LOG = []


def send_notification(decision: dict):
    """
    Stand-in for the real push step (Firebase Cloud Messaging etc).
    For the demo, we just print + log what WOULD be sent to a caregiver's phone.
    """
    event = decision["event"]
    message = (
        f"\n🔔 NOTIFICATION SENT (silent push)\n"
        f"   Device: {event['device_id']}\n"
        f"   Time:   {event['timestamp']}\n"
        f"   Type:   {event['type']}\n"
        f"   -> Door opened during quiet hours. Tap to view clip / dismiss / escalate.\n"
    )
    print(message)


@app.route("/webhook", methods=["POST"])
def receive_event():
    event = request.get_json(force=True)
    print(f"\n📥 Incoming Ring event: {event}")

    decision = should_notify(
        event,
        monitored_device_id=MONITORED_DEVICE_ID,
        quiet_start=QUIET_HOURS_START,
        quiet_end=QUIET_HOURS_END,
    )

    log_entry = {
        "received_at": datetime.now().isoformat(),
        "event": event,
        "decision": decision,
    }
    EVENT_LOG.append(log_entry)

    if decision["notify"]:
        send_notification(decision)
    else:
        print(f"🔕 Suppressed: {decision['reason']}")

    return jsonify({"status": "received", "decision": decision}), 200


@app.route("/log", methods=["GET"])
def get_log():
    """Simple history view - this is the 'dashboard' data source."""
    return jsonify(EVENT_LOG), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    print(f"Wander Watch webhook server starting.")
    print(f"Monitoring device: {MONITORED_DEVICE_ID}")
    print(f"Quiet hours: {QUIET_HOURS_START} -> {QUIET_HOURS_END}")
    app.run(host="0.0.0.0", port=5000)
