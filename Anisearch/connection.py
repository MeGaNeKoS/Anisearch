import requests
import logging
import json

from typing import Union

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

    def request(self,
                variables: dict,
                query_string: str,
                *, num_retries=10) -> Union[dict, None]:

        r = requests.post(self.settings['api_url'],
                          headers=self.settings['header'],
                          json={'query': query_string, 'variables': variables},
                          **self.custom_param)

        if r.status_code == 429:
            # it hit too many request limit
            import time
            for _ in range(num_retries):
                time.sleep(int(r.headers.get('Retry-After', default=60)))
                r = requests.post(self.settings['api_url'],
                                  headers=self.settings['header'],
                                  json={'query': query_string, 'variables': variables},
                                  **self.custom_param)
                if r.status_code != 429:
                    break
            else:
                Connection.logger.error(f"failed to get {variables} after {num_retries} retries")
                if Connection.logger.level == logging.DEBUG:
                    import pickle
                    import time
                    with open(f'Anisearch-connection-{time.time_ns()}.pkl', 'wb') as f:
                        pickle.dump(r, f)
                return None

        jsd = r.text

        try:
            jsd = json.loads(jsd)
        except ValueError as e:
            Connection.logger.error(f"{str(e)}:\n{r.status_code} {jsd}")
            return None
        else:
            return jsd
