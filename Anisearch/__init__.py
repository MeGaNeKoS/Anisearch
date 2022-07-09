import json
import logging
from typing import Union

import requests

from .get import AnilistGet
from .search import AnilistSearch

SETTINGS = {'header': {'Content-Type': 'application/json',
                       'User-Agent': 'Anisearch (github.com/MeGaNeKoS/Anisearch)',
                       'Accept': 'application/json'},
            'apiurl': 'https://graphql.anilist.co'}


class Anilist:
    """
        Initialize a new instance to the Anisearch API.
    """

    def __init__(self, log_level=logging.root.level):
        """

        """
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)

        self.logger.info('Initializing Anilist API')

        self.settings = SETTINGS
        self.search = AnilistSearch(self.settings, request_func=self.request)
        self.get = AnilistGet(self.settings, request_func=self.request)

    def request(self,
                variables: dict,
                query_string: str,
                *, num_retries=10) -> Union[dict, None]:
        r = requests.post(self.settings['apiurl'],
                          headers=self.settings['header'],
                          json={'query': query_string, 'variables': variables})

        if r.status_code == 429:
            # it hit too many request limit
            import time

            for _ in range(num_retries):
                time.sleep(int(r.headers.get('Retry-After', default=60)))
                r = requests.post(self.settings['apiurl'],
                                  headers=self.settings['header'],
                                  json={'query': query_string, 'variables': variables})
                if r.status_code != 429:
                    break
            else:
                self.logger.error(f"failed to get {variables} after {num_retries} retries")
                return None

        jsd = r.text

        try:
            jsd = json.loads(jsd)
        except ValueError as e:
            self.logger.error(f"{str(e)}:\n{jsd}")
            return None
        else:
            return jsd
