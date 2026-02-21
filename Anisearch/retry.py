import random
import time


class RetryStrategy:
    """Pluggable retry strategy for API requests.

    Args:
        max_retries: Maximum number of retry attempts.
        on_rate_limit: "wait" to sleep and retry, "raise" to raise immediately,
            or a callable(error_info, attempt) -> bool.
        on_server_error: "backoff" to exponential backoff, "raise" to raise,
            or a callable(error_info, attempt) -> bool.
        on_connection_error: "backoff" to exponential backoff, "raise" to raise,
            or a callable(error_info, attempt) -> bool.
        max_wait: Maximum seconds to wait between retries.
        backoff_base: Base seconds for exponential backoff.
    """

    def __init__(self, max_retries=3, on_rate_limit="wait", on_server_error="backoff",
                 on_connection_error="backoff", max_wait=60, backoff_base=1):
        self.max_retries = max_retries
        self.on_rate_limit = on_rate_limit
        self.on_server_error = on_server_error
        self.on_connection_error = on_connection_error
        self.max_wait = max_wait
        self.backoff_base = backoff_base

    def _backoff_sleep(self, attempt):
        sleep = (self.backoff_base + random.uniform(0, 1)) * 2 ** attempt
        time.sleep(min(sleep, self.max_wait))

    def handle_rate_limit(self, retry_after, attempt):
        """Return True to retry, False to stop."""
        if attempt >= self.max_retries:
            return False
        if callable(self.on_rate_limit):
            return self.on_rate_limit({"retry_after": retry_after}, attempt)
        if self.on_rate_limit == "raise":
            return False
        # "wait"
        time.sleep(min(retry_after, self.max_wait))
        return True

    def handle_server_error(self, status_code, attempt):
        if attempt >= self.max_retries:
            return False
        if callable(self.on_server_error):
            return self.on_server_error({"status_code": status_code}, attempt)
        if self.on_server_error == "raise":
            return False
        # "backoff"
        self._backoff_sleep(attempt)
        return True

    def handle_connection_error(self, error, attempt):
        if attempt >= self.max_retries:
            return False
        if callable(self.on_connection_error):
            return self.on_connection_error({"error": error}, attempt)
        if self.on_connection_error == "raise":
            return False
        # "backoff"
        self._backoff_sleep(attempt)
        return True
