import time
import uuid
from urllib.parse import urlparse


def build_intent_payload(
    actor_id: str,
    method: str,
    url: str,
    intent: dict,
    expires_in: int = 60,
) -> dict:
    """
    Builds canonical Supelock intent payload.
    """

    parsed = urlparse(url)

    now = int(time.time())

    payload = {
        "v": 1,  # token version
        "actor_id": actor_id,
        "method": method.upper(),
        "path": parsed.path,
        "intent": intent,
        "nonce": str(uuid.uuid4()),
        "iat": now,
        "exp": now + expires_in,
    }

    return payload
