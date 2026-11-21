import hashlib, json, pathlib

FLAGS_PATH = pathlib.Path(__file__).parent.parent / "flags.json"

def get_variant(user_id: str, flag: str) -> str:
    """같은 user_id는 항상 같은 그룹(A/B)에 배정된다."""
    flags = json.loads(FLAGS_PATH.read_text(encoding="utf-8"))
    cfg = flags.get(flag, {})
    if not cfg.get("enabled"):
        return "A"
    bucket = int(hashlib.sha256(f"{flag}:{user_id}".encode()).hexdigest(), 16) % 100
    return "B" if bucket < cfg["rollout_percent"] else "A"
