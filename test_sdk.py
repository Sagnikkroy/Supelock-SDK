from supelock.actor import Actor
from supelock.crypto import verify_signature
from supelock.storage import load_private_key
from supelock.crypto import generate_keypair
import base64
import json

# Step 1: Create actor
actor = Actor("test-agent")

# Step 2: Create token
token = actor.create_intent_token(
    method="POST",
    url="https://example.com/orders",
    intent={"action": "create_order"},
    expires_in=60
)

print("Generated Token:\n", token)

# Step 3: Manually verify signature locally

private_key = load_private_key(actor.key_path)

# Recreate public key
from nacl.signing import SigningKey
signing_key = SigningKey(private_key)
public_key = signing_key.verify_key.encode()

payload = verify_signature(public_key, token)

print("\nDecoded Payload:\n", json.dumps(payload, indent=2))
