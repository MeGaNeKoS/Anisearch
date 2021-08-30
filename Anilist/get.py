import json
from typing import Union

import requests


class AnilistGet:
    def __init__(self, settings):
        self.settings = settings
        self.DEFAULT_QUERY = {"anime": """
                query ($id: Int) {
                    Media(id: $id, type: ANIME) {
                        title {
                            romaji
                            english
                        }
                        bannerImage
                        format
                        status
                        episodes
                        duration
                        season
                        seasonYear
                        isAdult
                        genres
                        countryOfOrigin
                        description
                        averageScore
                        meanScore
                        synonyms
                    }
                }
            """,
                              "manga": """
                query ($id: Int) {
                    Media(id: $id, type: MANGA) {
                        title {
                            romaji
                            english
                        }
                        bannerImage
                        format
                        chapters
                        volumes
                        status
                        description
                        averageScore
                        meanScore
                        genres
                        synonyms
                    }
                }
            """,
                              "staff": """
                query ($id: Int) {
                    Staff(id: $id) {
                        name {
                            first
                            last
                            native
                        }
                        description
                        language
                    }
                }
            """,
                              "studio": """
                query ($id: Int) {
                    Studio(id: $id) {
                        name
                    }
                }
            """,
                              "character": """
                query ($id: Int) {
                    Character (id: $id) {
                        name {
                            first
                            last
                            native
                        }
                        description
                        image {
                            large
                        }
                    }
                }
            """}

    def request(self, item_id, query_string) -> Union[dict, None]:
        variables = {"id": item_id}
        r = requests.post(self.settings['apiurl'],
                          headers=self.settings['header'],
                          json={'query': query_string, 'variables': variables})
        jsd = r.text

        try:
            jsd = json.loads(jsd)
        except ValueError:
            return None
        else:
            return jsd

    def anime(self, item_id, query_string=None) -> Union[dict, None]:
        """
        The function to retrieve an anime's details.

        :param int item_id: the anime's ID
        :param str query_string: What info you interested to?
        :return: dict or None
        :rtype: dict or NoneType
        """
        if query_string is None:
            query_string = self.DEFAULT_QUERY["anime"]
        return self.request(item_id, query_string)

    def manga(self, item_id, query_string=None) -> Union[dict, None]:
        """
        The function to retrieve an anime's details.

        :param int item_id: the anime's ID
        :param str query_string: What info you interested to?
        :return: dict or None
        :rtype: dict or NoneType
        """
        if query_string is None:
            query_string = self.DEFAULT_QUERY["manga"]
        return self.request(item_id, query_string)

    def staff(self, item_id, query_string=None) -> Union[dict, None]:
        """
        The function to retrieve a manga's details.
        :param int item_id: the anime's ID
        :param str query_string: What info you interested to?
        :return: dict or None
        :rtype: dict or NoneType
        """
        if query_string is None:
            query_string = self.DEFAULT_QUERY["staff"]
        return self.request(item_id, query_string)

    def studio(self, item_id, query_string=None) -> Union[dict, None]:
        """
        The function to retrieve a studio's details.

        :param int item_id: the anime's ID
        :param str query_string: What info you interested to?
        :return: dict or None
        :rtype: dict or NoneType
        """
        if query_string is None:
            query_string = self.DEFAULT_QUERY["studio"]
        return self.request(item_id, query_string)

    def character(self, item_id, query_string=None) -> Union[dict, None]:
        """
        The function to retrieve a character's details.

        :param int item_id: the anime's ID
        :param str query_string: What info you interested to?
        :return: dict or None
        :rtype: dict or NoneType
        """
        if query_string is None:
            query_string = self.DEFAULT_QUERY["character"]
        return self.request(item_id, query_string)
