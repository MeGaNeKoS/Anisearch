class AnilistError(Exception):
    """Base exception for Anisearch."""


class RateLimitError(AnilistError):
    """Raised on HTTP 429."""

    def __init__(self, retry_after=60):
        self.retry_after = retry_after
        super().__init__(f"Rate limited. Retry after {retry_after}s")


class ServerError(AnilistError):
    """Raised on HTTP 5xx."""

    def __init__(self, status_code, body=""):
        self.status_code = status_code
        self.body = body
        super().__init__(f"Server error {status_code}")


class GraphQLError(AnilistError):
    """Raised when the response body contains GraphQL errors."""

    def __init__(self, errors):
        self.errors = errors
        messages = "; ".join(e.get("message", "") for e in errors)
        super().__init__(f"GraphQL errors: {messages}")


class ConnectionError(AnilistError):
    """Raised on network failure."""

    def __init__(self, original):
        self.original = original
        super().__init__(str(original))
