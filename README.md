# 🛡 Supelock SDK

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-alpha-orange.svg)
![Crypto](https://img.shields.io/badge/crypto-Ed25519-purple.svg)

Supelock SDK gives automation and agents a **cryptographic identity** and a way to attach **signed intent** to every HTTP request.

It allows websites to verify:
- Who is acting
- What they intend to do
- Whether the declaration was tampered with

---

Today, websites only see requests.

They don't know:
- If the request is from legitimate automation
- What the actor intended
- Whether the action matches expectations

Supelock introduces **verifiable intent**.

Instead of guessing behavior, servers can verify signed declarations.

---

## What the SDK Does

The Supelock SDK:

- Generates an Ed25519 keypair
- Stores the private key locally
- Builds a canonical intent payload
- Cryptographically signs the payload
- Attaches the signed token to outgoing requests

That’s it. No magic. No black box scoring.

---

## Installation

```bash
pip install supelock

```
## How to use 
```bash
from supelock import Actor

actor = Actor("ci-bot-1")

response = actor.request(
    method="POST",
    url="https://api.example.com/orders",
    intent={
        "action": "create_order",
        "max_amount": 5000
    },
    json={"amount": 3000}
)

print(response.status_code)
```

The SDK automatically:

*Signs the intent
*Attaches headers
*Sends the request