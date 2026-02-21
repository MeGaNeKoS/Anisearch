import asyncio
import json
import logging
from typing import Union

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


class AsyncConnection:
    logger = logging.getLogger(__name__)

    def __init__(self, setting=None, retry=None):
        self.settings = setting or SETTINGS
        self._retry = retry
        self._session = None

    async def _get_session(self):
        if self._session is None:
            try:
                import aiohttp
            except ImportError:
                raise ImportError(
                    "aiohttp is required for async support. "
                    "Install it with: pip install anisearch[async]"
                )
            self._session = aiohttp.ClientSession()
        return self._session

    async def close(self):
        if self._session is not None:
            await self._session.close()
            self._session = None

    async def request(self,
                      variables: dict,
                      query_string: str,
                      **kwargs) -> Union[dict, None]:
        self.logger.debug('Async requesting Anilist API')
        variables = {k: v for k, v in variables.items() if v is not None}

        strategy = self._retry
        max_attempts = (strategy.max_retries + 1) if strategy else 1

        session = await self._get_session()
        result = None

        for attempt in range(max_attempts):
            try:
                async with session.post(
                    self.settings['api_url'],
                    headers=self.settings['header'],
                    json={'query': query_string, 'variables': variables},
                    timeout=__import__('aiohttp').ClientTimeout(total=10)
                ) as resp:
                    status = resp.status
                    text = await resp.text()
                    headers = resp.headers
            except Exception as e:
                self.logger.warning(f'ConnectionError: {attempt + 1}/{max_attempts}')
                if strategy and strategy.handle_connection_error(e, attempt):
                    continue
                raise AnilistConnectionError(e)

            if status == 429:
                retry_after = int(headers.get('Retry-After', 60))
                if strategy:
                    if attempt < strategy.max_retries:
                        if strategy.on_rate_limit == "raise":
                            raise RateLimitError(retry_after)
                        if callable(strategy.on_rate_limit):
                            if strategy.on_rate_limit({"retry_after": retry_after}, attempt):
                                await asyncio.sleep(min(retry_after, strategy.max_wait))
                                continue
                            raise RateLimitError(retry_after)
                        # "wait"
                        await asyncio.sleep(min(retry_after, strategy.max_wait))
                        continue
                raise RateLimitError(retry_after)

            if status >= 500:
                self.logger.error(f'Anilist API returned {status}')
                if strategy and strategy.handle_server_error(status, attempt):
                    continue
                raise ServerError(status, text)

            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return {
                    "errors": [{"message": "Failed to convert to JSON", "status": status}],
                    "data": {"Media": []}
                }

        return {
            "errors": [{"message": f"failed after {max_attempts} retries"}],
            "data": {"Media": []}
        }
