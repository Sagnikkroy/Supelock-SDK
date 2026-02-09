import os
import base64
import httpx
from typing import Dict, Optional

from .crypto import generate_keypair, sign_payload
from .token import build_intent_payload
from .storage import load_private_key, save_private_key
from .exceptions import SupelockError


DEFAULT_KEY_PATH = os.path.expanduser("~/.supelock/private.key")


class Actor:
    """
    Supelock Actor

    Handles:
    - Key management
    - Intent signing
    - Request wrapping
    """

    def __init__(
        self,
        actor_id: str,
        key_path: Optional[str] = None,
        auto_generate: bool = True,
    ):
        self.actor_id = actor_id
        self.key_path = key_path or DEFAULT_KEY_PATH

        self._private_key = load_private_key(self.key_path)

        if not self._private_key:
            if not auto_generate:
                raise SupelockError("No private key found and auto_generate disabled.")
            self._generate_and_store_key()

    def _generate_and_store_key(self):
        private_key, public_key = generate_keypair()
        save_private_key(self.key_path, private_key)
        self._private_key = private_key

        # Encode public key safely
        encoded_pub = base64.b64encode(public_key).decode()

        print("Supelock keypair generated.")
        print(f"Actor ID: {self.actor_id}")
        print("Public Key (register this with website):")
        print(encoded_pub)

    def create_intent_token(
        self,
        method: str,
        url: str,
        intent: Dict,
        expires_in: int = 60,
    ) -> str:
        """
        Build and sign intent token.
        """

        payload = build_intent_payload(
            actor_id=self.actor_id,
            method=method,
            url=url,
            intent=intent,
            expires_in=expires_in,
        )

        signed_token = sign_payload(self._private_key, payload)
        return signed_token

    def request(
        self,
        method: str,
        url: str,
        intent: Dict,
        expires_in: int = 60,
        headers: Optional[Dict] = None,
        **kwargs,
    ):
        """
        Sends HTTP request with Supelock headers attached.
        """

        headers = headers.copy() if headers else {}

        token = self.create_intent_token(
            method=method,
            url=url,
            intent=intent,
            expires_in=expires_in,
        )

        headers.update({
            "X-Supelock-Actor": self.actor_id,
            "X-Supelock-Intent": token,
        })

        with httpx.Client() as client:
            response = client.request(
                method=method,
                url=url,
                headers=headers,
                **kwargs,
            )

        return response
