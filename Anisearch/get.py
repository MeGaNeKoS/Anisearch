from typing import Union


class AnilistGet:
    def __init__(self, settings, *, request_func):
        self.settings = settings
        self.DEFAULT_QUERY = {
            "anime": """
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
            """
        }

        self._request = request_func

    def anime(self, item_id: int, *args, **kwargs) -> Union[dict, None]:
        """
        The function to retrieve an anime's details.

        :param int item_id: the anime's ID
        :return: List of dictionaries which are anime objects or None
        """

        variables = {"id": item_id}
        return self._request(variables, self.DEFAULT_QUERY["anime"], *args, **kwargs)

    def character(self, item_id: int, *args, **kwargs) -> Union[dict, None]:
        """
        The function to retrieve a character's details.

        :param int item_id: the anime's ID
        :return: List of dictionaries which are character objects or None
        """
        variables = {"id": item_id}
        return self._request(variables, self.DEFAULT_QUERY["character"], *args, **kwargs)

    def manga(self, item_id: int, *args, **kwargs) -> Union[dict, None]:
        """
        The function to retrieve an anime's details.

        :param int item_id: the anime's ID
        :return: List of dictionaries which are manga objects or None
        """

        variables = {"id": item_id}
        return self._request(variables, self.DEFAULT_QUERY["manga"], *args, **kwargs)

    def staff(self, item_id: int, *args, **kwargs) -> Union[dict, None]:
        """
        The function to retrieve a manga's details.
        :param int item_id: the anime's ID
        :return: List of dictionaries which are staff objects or None
        """

        variables = {"id": item_id}
        return self._request(variables, self.DEFAULT_QUERY["staff"], *args, **kwargs)

    def studio(self, item_id: int, *args, **kwargs) -> Union[dict, None]:
        """
        The function to retrieve a studio's details.

        :param int item_id: the anime's ID
        :return: List of dictionaries which are studio objects or None
        """

        variables = {"id": item_id}
        return self._request(variables, self.DEFAULT_QUERY["studio"], *args, **kwargs)

    def custom_query(self, variables: dict, query_string: str, *args, **kwargs) -> Union[dict, None]:
        """
        The function to retrieve custom query.

        :param str query_string: the query string
        :param dict variables: the variables
        :return: List of dictionaries objects or None
        """

        return self._request(variables, query_string, *args, **kwargs)
