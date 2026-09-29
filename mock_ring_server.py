"""
A tiny local stand-in for the real Ring Developers Playground.

This exists ONLY because this sandbox can't reach api.amazonvision.com.
It mimics the shape of GET /v1/devices so ring_client.py can be tested
end-to-end. When you run this for real, delete/ignore this file and point
config.RING_API_BASE at https://api.amazonvision.com with your real token.
"""
from flask import Flask, jsonify

app = Flask(__name__)

FAKE_DEVICES = {
    "data": [
        {
            "id": "front-door-cam-001",
            "type": "doorbell",
            "name": "Front Door",
            "status": "online",
        },
        {
            "id": "backyard-cam-002",
            "type": "camera",
            "name": "Backyard",
            "status": "online",
        },
    ]
}


@app.route("/v1/devices", methods=["GET"])
def devices():
    return jsonify(FAKE_DEVICES), 200


@app.route("/v1/devices/<device_id>/status", methods=["GET"])
def device_status(device_id):
    return jsonify({"id": device_id, "status": "online"}), 200


@app.route("/v1/events/<event_id>/clip", methods=["GET"])
def event_clip(event_id):
    return jsonify({"event_id": event_id, "clip_url": f"https://mock.local/clips/{event_id}.mp4"}), 200


if __name__ == "__main__":
    print("Mock Ring API running on http://localhost:5001 (stand-in for api.amazonvision.com)")
    app.run(host="0.0.0.0", port=5001)
