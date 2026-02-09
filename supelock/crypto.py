import base64
import json
from nacl.signing import SigningKey, VerifyKey
from nacl.exceptions import BadSignatureError


def generate_keypair():
    """
    Generate Ed25519 keypair.
    Returns (private_key_bytes, public_key_bytes)
    """

    signing_key = SigningKey.generate()
    verify_key = signing_key.verify_key

    private_key = signing_key.encode()
    public_key = verify_key.encode()

    return private_key, public_key


def sign_payload(private_key: bytes, payload: dict) -> str:
    """
    Signs a dictionary payload.
    Returns base64 encoded signed blob.
    """

    signing_key = SigningKey(private_key)

    message = canonical_json(payload).encode()
    signed = signing_key.sign(message)

    return base64.b64encode(signed).decode()


def verify_signature(public_key: bytes, token: str) -> dict:
    """
    Verifies a signed token and returns payload dict.
    Raises if invalid.
    """

    verify_key = VerifyKey(public_key)

    signed = base64.b64decode(token)
    message = verify_key.verify(signed)

    return json.loads(message.decode())


def canonical_json(data: dict) -> str:
    """
    Deterministic JSON encoding.
    Ensures signature consistency.
    """

    import json
    return json.dumps(data, separators=(",", ":"), sort_keys=True)
