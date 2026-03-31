<div align="center">

# Supelock SDK

**Give your AI agent a cryptographic identity.**

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-alpha-orange.svg)]()
[![Crypto](https://img.shields.io/badge/crypto-Ed25519-purple.svg)]()

The Supelock SDK signs every HTTP request your agent makes with a declared intent. APIs that run the Supelock Middleware can verify who you are, what you intend to do, and give you better access than anonymous traffic.

[Quickstart](#quickstart) · [How it works](#how-it-works) · [API](#api) · [Contributing](#contributing)

</div>

---

## The problem

When your AI agent calls an external API, the server has no idea if you're a legitimate automation or a random scraper. Both look identical at the HTTP level. So either you get blocked, or you get the same throttled access as everyone else.

Supelock fixes this. Your agent signs every request with an Ed25519 key. APIs that run the middleware verify the signature and give your agent the access it deserves.

---

## Quickstart

```bash
pip install cryptography httpx
```

```python
from supelock.actor import Actor

# Create an actor — generates a keypair on first run, stores it locally
actor = Actor(
    actor_id="my-agent",
    registry_url="http://localhost:8001",
    label="My AI agent",
)

# Register with the registry (safe to call multiple times)
actor.register()

# Make a signed request
response = actor.request(
    method="GET",
    url="http://localhost:8000/api/data",
    intent={"action": "read_data"},
)

print(response.status_code)
print(response.headers.get("X-Supelock-Trust"))   # "high"
print(response.headers.get("X-Supelock-Policy"))  # "verified_agent"
```

---

## How it works

Every request gets two headers attached:

```
X-Supelock-Actor:  my-agent
X-Supelock-Intent: <base64-encoded Ed25519 signed payload>
```

The signed payload contains:

```json
{
  "actor_id": "my-agent",
  "method": "GET",
  "path": "/api/data",
  "intent": { "action": "read_data" },
  "nonce": "abc-123",
  "iat": 1743120000,
  "exp": 1743120300
}
```

The middleware fetches your public key from the Registry, verifies the signature, checks expiry and replay, and sets `trust_level=high`. You get better rate limits, more data, access to restricted paths — whatever the API owner configured.

---

## API

### `Actor(actor_id, ...)`

| Parameter | Default | Description |
|-----------|---------|-------------|
| `actor_id` | required | Unique identifier for your agent |
| `key_path` | `~/.supelock/private.key` | Where to store the private key |
| `registry_url` | `http://localhost:8001` | Supelock Registry URL |
| `label` | None | Human-readable name |
| `owner` | None | Team or org identifier |

### `actor.register()` → `bool`

Register with the Registry. Returns `True` on success or if already registered.

### `actor.request(method, url, intent, ...)` → `httpx.Response`

Make a signed HTTP request. Accepts all `httpx` kwargs.

### `actor.create_intent_token(method, url, intent)` → `str`

Build a signed token without making a request. Useful if you manage your own HTTP client.

---

## Security model

- Ed25519 signatures — same curve used by SSH, Signal, and Tor
- Private key never leaves your machine
- Every request signed individually — no session tokens to steal
- Nonce-based replay protection on the middleware side
- Tokens expire after 5 minutes by default

---

## Part of the Supelock ecosystem

| Repo | Role | Status |
|------|------|--------|
| **Supelock-SDK** | Agent identity + signing | ✅ This repo |
| [Supelock-Registry](https://github.com/Sagnikkroy/Supelock-Registry) | Public key storage | ✅ Built |
| [Supelock-Middleware](https://github.com/Sagnikkroy/Supelock-Middleware) | Verification + policy | ✅ Built |
| [Supelock-Dashboard](https://github.com/Sagnikkroy/Supelock-Dashboard) | Live monitoring UI | ✅ Built |

---

## Contributing

```bash
git clone https://github.com/Sagnikkroy/Supelock-SDK
cd Supelock-SDK
pip install cryptography httpx pytest
python test_sdk.py
```

Good first issues:
- [ ] Async support — `await actor.async_request(...)`
- [ ] Key rotation — generate new keypair and re-register
- [ ] JavaScript/TypeScript SDK port
- [ ] Token caching — reuse signed token within expiry window

---

## License

MIT