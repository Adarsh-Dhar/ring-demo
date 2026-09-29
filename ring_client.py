"""
Thin client around the Ring API.

These are the real endpoints per Ring's published API docs:
  GET /v1/devices                -> list devices you're authorized to see
  GET /v1/devices/{id}/status    -> check online/offline status
  GET /v1/events/{event_id}/clip -> fetch a media clip for an event (shape may vary;
                                     adjust the path once you have real API docs open)

Swapping config.RING_API_BASE from the mock server to
https://api.amazonvision.com is the only change needed to go live.
"""
import requests
from config import RING_API_BASE, RING_ACCESS_TOKEN


def _headers():
    return {
        "Authorization": f"Bearer {RING_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }


def list_devices():
    """GET /v1/devices - returns devices this token can access."""
    resp = requests.get(f"{RING_API_BASE}/v1/devices", headers=_headers(), timeout=10)
    resp.raise_for_status()
    return resp.json()


def get_device_status(device_id: str):
    """GET /v1/devices/{id}/status"""
    resp = requests.get(
        f"{RING_API_BASE}/v1/devices/{device_id}/status",
        headers=_headers(),
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()


def get_event_clip_url(event_id: str):
    """
    Fetch the clip reference for a given event.
    NOTE: verify the exact real endpoint shape in Ring's API docs when you
    swap to the live API - this mirrors the mock server's shape for now.
    """
    resp = requests.get(
        f"{RING_API_BASE}/v1/events/{event_id}/clip",
        headers=_headers(),
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    # Quick manual smoke test: run `python ring_client.py` to confirm connectivity.
    print("Devices visible to this token:")
    print(list_devices())
