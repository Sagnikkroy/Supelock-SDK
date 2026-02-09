class SupelockError(Exception):
    """Base Supelock exception"""
    pass


class InvalidIntent(SupelockError):
    pass


class ExpiredToken(SupelockError):
    pass


class VerificationFailed(SupelockError):
    pass
