import json
import logging
import pickle
import random
import time
from typing import Union

import requests

SETTINGS = {
    'header': {
        'Content-Type': 'application/json',
        'User-Agent': 'Anisearch (github.com/MeGaNeKoS/Anisearch)',
        'Accept': 'application/json'},
    'api_url': 'https://graphql.anilist.co'
}


class Connection:
    logger = logging.getLogger(__name__)

    def __init__(self, setting=None, custom_param=None):
        self.settings = setting or SETTINGS
        self.custom_param = custom_param or {}
        self.session = requests.Session()

    def request(self,
                variables: dict,
                query_string: str,
                *, num_retries=10,
                backoff_in_seconds=1,
                max_wait=60,
                **kwargs) -> Union[dict, None]:
        self.logger.debug('Requesting Anilist API')
        self.logger.debug(f'Variables: {variables}')
        self.logger.debug(f'Query: {query_string}')

        variables = {k: v for k, v in variables.items() if v is not None}
        result = None
        for retry in range(num_retries):
            try:
                result = self.session.post(self.settings['api_url'],
                                           headers=self.settings['header'],
                                           json={'query': query_string, 'variables': variables},
                                           timeout=10,
                                           **self.custom_param, **kwargs)
            except requests.exceptions.ConnectionError:
                self.logger.warning(f'ConnectionError: {retry + 1}/{num_retries}')
                sleep = (backoff_in_seconds + random.uniform(0, 1)) * 2 ** retry
                time.sleep(sleep)
                continue
            self.logger.debug(f'Response: {result.text}')
            if result.status_code == 429:
                # it hit too many request limit
                time.sleep(int(result.headers.get('Retry-After', default=60)))
                continue
            elif result.status_code >= 500:
                # server error
                self.logger.error(f'Anilist API returned {result.status_code} status code')
                # backoff exponentially
                sleep = (backoff_in_seconds + random.uniform(0, 1)) * 2 ** retry
                time.sleep(min(sleep, max_wait))
                continue
            try:
                return result.json()
            except json.decoder.JSONDecodeError as e:
                Connection.logger.error(f"{str(e)}:\n{result.status_code} {result.text}")
                if self.logger.level == logging.DEBUG:
                    with open(f'Anisearch-connection-{time.asctime()}-{retry}.pkl', 'wb') as f:
                        pickle.dump(result, f)
                return {
                    "errors": [
                        {
                            "message": "Failed to convert to JSON",
                            "status": result.status_code,
                            "locations": [
                                {
                                    "line": e.lineno,
                                    "column": e.colno
                                }
                            ]
                        }
                    ],
                    "data": {"Media": []}
                }
            except Exception as e:
                Connection.logger.error(f"{str(e)}:\n{result.status_code} {result.text}")
                raise

        Connection.logger.error(f"failed to get {variables} after hit max {num_retries} retries")
        if Connection.logger.level == logging.DEBUG and result:
            with open(f'Anisearch-connection-{time.time_ns()}.pkl', 'wb') as f:
                pickle.dump(result, f)
        return {
            "errors": [
                {"message": f"failed to get {variables} after hit max {num_retries} retries"}
            ],
            "data": {"Media": []}
        }
