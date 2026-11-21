import json, time, pathlib

LOG = pathlib.Path(__file__).parent.parent / "data" / "events" / "events.jsonl"

def track(user_id: str, variant: str, event: str):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"ts": time.time(), "user_id": user_id,
                            "variant": variant, "event": event},
                           ensure_ascii=False) + "\n")
