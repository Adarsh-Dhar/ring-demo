"""
Config for Wander Watch.

Real usage: create a .env file (see .env.example) with your actual
Ring Developers Playground token, and point RING_API_BASE at the real API.
Nothing in here is hardcoded to the mock - swapping .env is all you need.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Ring API base URL. In real usage this is https://api.amazonvision.com
# For local testing without network access, this points at our mock server instead.
RING_API_BASE = os.getenv("RING_API_BASE", "http://localhost:5001")

# Your Ring Developers Playground access token (30-min TTL when real).
RING_ACCESS_TOKEN = os.getenv("RING_ACCESS_TOKEN", "mock-token-for-local-testing")

# The device ID you want to monitor (e.g. front door camera).
# In real usage, get this from GET /v1/devices first.
MONITORED_DEVICE_ID = os.getenv("MONITORED_DEVICE_ID", "front-door-cam-001")

# Quiet hours window: events on the monitored device outside these hours are ignored.
QUIET_HOURS_START = os.getenv("QUIET_HOURS_START", "21:30")  # 9:30 PM
QUIET_HOURS_END = os.getenv("QUIET_HOURS_END", "06:30")      # 6:30 AM

# Where the webhook server listens for incoming Ring events.
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST", "0.0.0.0")
WEBHOOK_PORT = int(os.getenv("WEBHOOK_PORT", "5000"))
