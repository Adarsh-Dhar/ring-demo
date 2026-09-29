"""
The "brain" of Wander Watch - v1, rules-only (no AI yet).

Given an incoming Ring event, decide: suppress it, or notify a caregiver.
This is intentionally simple and dependency-free so it's easy to reason
about and test. The AI person-detection / description step (Agent 1 / Agent 2
from our earlier design) would slot in right where NOTES below mark it.
"""
from datetime import datetime, time


def _parse_hhmm(s: str) -> time:
    h, m = map(int, s.split(":"))
    return time(hour=h, minute=m)


def is_within_quiet_hours(event_time: datetime, start_str: str, end_str: str) -> bool:
    """
    Handles overnight windows correctly, e.g. 21:30 -> 06:30 (crosses midnight).
    """
    start = _parse_hhmm(start_str)
    end = _parse_hhmm(end_str)
    t = event_time.time()

    if start <= end:
        # Window does not cross midnight, e.g. 09:00 -> 17:00
        return start <= t <= end
    else:
        # Window crosses midnight, e.g. 21:30 -> 06:30
        return t >= start or t <= end


def should_notify(event: dict, monitored_device_id: str, quiet_start: str, quiet_end: str) -> dict:
    """
    event is expected to look like:
    {
        "id": "evt_123",
        "device_id": "front-door-cam-001",
        "type": "motion" | "door_open" | "ring",
        "timestamp": "2026-09-29T03:14:00"
    }

    Returns a decision dict explaining what happened and why - useful for
    logging and for your demo video ("here's why it did/didn't fire").
    """
    event_time = datetime.fromisoformat(event["timestamp"])

    if event["device_id"] != monitored_device_id:
        return {"notify": False, "reason": "event is not on the monitored device"}

    if not is_within_quiet_hours(event_time, quiet_start, quiet_end):
        return {"notify": False, "reason": "event occurred outside quiet hours"}

    # --- NOTE: this is where Agent 1 (perception) would run ---
    # clip = ring_client.get_event_clip_url(event["id"])
    # perception = call_bedrock_vision(clip)  # -> {"person_present": bool, "description": str}
    # if not perception["person_present"]:
    #     return {"notify": False, "reason": "no person detected in clip (AI filter)"}

    # --- NOTE: this is where Agent 2 (decision) could add extra context ---
    # e.g. suppress repeat events within N minutes, check recent dismissals, etc.

    return {
        "notify": True,
        "reason": "door event on monitored device during quiet hours",
        "event": event,
    }
