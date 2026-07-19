import time
import uuid


def generate_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex}"


def generate_timestamp() -> int:
    return int(time.time())