import os


def load_private_key(path: str) -> bytes:
    """
    Load private key from file.
    Returns None if not found.
    """

    if not os.path.exists(path):
        return None

    with open(path, "rb") as f:
        return f.read()


def save_private_key(path: str, private_key: bytes):
    """
    Save private key to file with restricted permissions.
    """

    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    with open(path, "wb") as f:
        f.write(private_key)

    try:
        os.chmod(path, 0o600)  # owner read/write only (Unix)
    except Exception:
        pass
