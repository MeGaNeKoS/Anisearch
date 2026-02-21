import json
import logging
import pickle
import time
from typing import Union

import requests

from Anisearch.errors import RateLimitError, ServerError, GraphQLError
from Anisearch.errors import ConnectionError as AnilistConnectionError
from Anisearch.retry import RetryStrategy

SETTINGS = {
    'header': {
        'Content-Type': 'application/json',
        'User-Agent': 'Anisearch (github.com/MeGaNeKoS/Anisearch)',
        'Accept': 'application/json'},
    'api_url': 'https://graphql.anilist.co'
}


class Connection:
    logger = logging.getLogger(__name__)

    def __init__(self, setting=None, custom_param=None, retry=None):
        self.settings = setting or SETTINGS
        self.custom_param = custom_param or {}
        self.session = requests.Session()
        # retry=<unset sentinel> means use default; None means no retries
        self._retry = retry

    def request(self,
                variables: dict,
                query_string: str,
                *, num_retries=None,
                backoff_in_seconds=1,
                max_wait=60,
                **kwargs) -> Union[dict, None]:
        self.logger.debug('Requesting Anilist API')
        self.logger.debug(f'Variables: {variables}')
        self.logger.debug(f'Query: {query_string}')

        variables = {k: v for k, v in variables.items() if v is not None}

        strategy = self._retry
        if num_retries is not None and strategy is None:
            # Legacy call with explicit num_retries but no strategy — create a temporary one
            strategy = RetryStrategy(max_retries=num_retries, max_wait=max_wait,
                                     backoff_base=backoff_in_seconds)

        max_attempts = (strategy.max_retries + 1) if strategy else (num_retries or 1)

        result = None
        for attempt in range(max_attempts):
            try:
                result = self.session.post(
                    self.settings['api_url'],
                    headers=self.settings['header'],
                    json={'query': query_string, 'variables': variables},
                    timeout=10,
                    **self.custom_param, **kwargs)
            except requests.exceptions.ConnectionError as e:
                self.logger.warning(f'ConnectionError: {attempt + 1}/{max_attempts}')
                if strategy and strategy.handle_connection_error(e, attempt):
                    continue
                if not strategy:
                    raise AnilistConnectionError(e)
                raise AnilistConnectionError(e)

            self.logger.debug(f'Response: {result.text}')

            if result.status_code == 429:
                retry_after = int(result.headers.get('Retry-After', 60))
                if strategy and strategy.handle_rate_limit(retry_after, attempt):
                    continue
                raise RateLimitError(retry_after)

            if result.status_code >= 500:
                self.logger.error(f'Anilist API returned {result.status_code} status code')
                if strategy and strategy.handle_server_error(result.status_code, attempt):
                    continue
                raise ServerError(result.status_code, result.text)

            try:
                data = result.json()
            except json.decoder.JSONDecodeError as e:
                Connection.logger.error(f"{str(e)}:\n{result.status_code} {result.text}")
                if self.logger.level == logging.DEBUG:
                    with open(f'Anisearch-connection-{time.asctime()}-{attempt}.pkl', 'wb') as f:
                        pickle.dump(result, f)
                return {
                    "errors": [
                        {
                            "message": "Failed to convert to JSON",
                            "status": result.status_code,
                            "locations": [{"line": e.lineno, "column": e.colno}]
                        }
                    ],
                    "data": {"Media": []}
                }
            except Exception as e:
                Connection.logger.error(f"{str(e)}:\n{result.status_code} {result.text}")
                raise

            return data

        Connection.logger.error(f"failed to get {variables} after hit max {max_attempts} retries")
        if Connection.logger.level == logging.DEBUG and result:
            with open(f'Anisearch-connection-{time.time_ns()}.pkl', 'wb') as f:
                pickle.dump(result, f)
        return {
            "errors": [
                {"message": f"failed to get {variables} after hit max {max_attempts} retries"}
            ],
            "data": {"Media": []}
        }
