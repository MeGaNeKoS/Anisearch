from typing import Union


class AnilistSearch:
    def __init__(self, settings, *, request_func):
        self.settings = settings
        self.DEFAULT_QUERY = {
            "anime": """
                query ($query: String, $page: Int, $perPage: Int) {
                    Page (page: $page, perPage: $perPage) {
                        pageInfo {
                            total
                            currentPage
                            lastPage
                            hasNextPage
                        }
                        media (search: $query, type: ANIME) {
                            id
                            title {
                                romaji
                                english
                            }
                            synonyms
                            countryOfOrigin
                            format
                            status
                            episodes
                            duration
                            season
                            seasonYear
                            isAdult
                            genres
                            averageScore
                            meanScore
                            hashtag
                            bannerImage                            
                            description
                            }
                    }
                }
            """,
            "manga": """
                query ($query: String, $page: Int, $perPage: Int) {
                    Page (page: $page, perPage: $perPage) {
                        pageInfo {
                            total
                            currentPage
                            lastPage
                            hasNextPage
                        }
                        media (search: $query, type: MANGA) {
                            id
                            title {
                                romaji
                                english
                            }
                            coverImage {
                                large
                            }
                            averageScore
                            popularity
                            chapters
                            volumes
                            season
                            hashtag
                            isAdult
                        }
                    }
                }
            """,
            "staff": """
                query ($query: String, $page: Int, $perPage: Int) {
                    Page (page: $page, perPage: $perPage) {
                        pageInfo {
                            total
                            currentPage
                            lastPage
                            hasNextPage
                        }
                        staff (search: $query) {
                            id
                            name {
                                first
                                last
                            }
                            image {
                                large
                            }
                        }
                    }
                }
            """,
            "studio": """
                query ($query: String, $page: Int, $perPage: Int) {
                    Page (page: $page, perPage: $perPage) {
                        pageInfo {
                            total
                            currentPage
                            lastPage
                            hasNextPage
                        }
                        studios (search: $query) {
                            id
                            name
                        }
                    }
                }
            """,
            "character": """
                query ($query: String, $page: Int, $perPage: Int) {
                    Page (page: $page, perPage: $perPage) {
                        pageInfo {
                            total
                            currentPage
                            lastPage
                            hasNextPage
                        }
                        characters (search: $query) {
                            id
                            name {
                                first
                                last
                            }
                            image {
                                large
                            }
                        }
                    }
                }
            """
        }

        self._request = request_func

    def anime(self,
              term: str,
              page: int = 1,
              per_page: int = 10,
              *args, **kwargs) -> Union[dict, None]:
        """
        Search for an anime by term.
        Results are paginated by default. We need to specify which page we wanted.
        Per page specifies how many per page to request. 10 is just the example from the API docs.

        :param str term: Name to search by
        :param int page: Which page are we requesting? starts at 1.
        :param int per_page : How many results per page? defaults to 10.
        :return: List of dictionaries which are anime objects or None
        """

        variables = {"query": term, "page": page, "perPage": per_page}
        return self._request(variables, self.DEFAULT_QUERY['anime'], *args, **kwargs)

    def character(self,
                  term: str,
                  page: int = 1,
                  per_page: int = 10,
                  *args, **kwargs) -> Union[dict, None]:
        """
        Search for a character by term.
        Results are paginated by default. We need to specifies which page we wanted.
        Per page specifies how many per page to request. 10 is just the example from the API docs.

        :param str term: Name to search by
        :param int page: Which page are we requesting? Starts at 1.
        :param int per_page: How many results per page are we requesting? default to 10.
        :return: Json object with returned results.
        :rtype: Json object with returned results.
        """

        variables = {"query": term, "page": page, "perPage": per_page}
        return self._request(variables, self.DEFAULT_QUERY['character'], *args, **kwargs)

    def manga(self,
              term: str,
              page: int = 1,
              per_page: int = 10,
              *args, **kwargs) -> Union[dict, None]:
        """
        Search for a manga by term.
        Results are paginated by default. We need to specifies which page we wanted.
        Per page specifies how many per page to request. 10 is just the example from the API docs.

        :param str term: Name to search by
        :param int page: Which page are we requesting? Starts at 1.
        :param int per_page: How many results per page? defaults to 10.

        :return: List of dictionaries which are manga objects or None
        :rtype: list of dict or NoneType
        """
        variables = {"query": term, "page": page, "perPage": per_page}
        return self._request(variables, self.DEFAULT_QUERY['manga'], *args, **kwargs)

    def staff(self,
              term: str,
              page: int = 1,
              per_page: int = 10,
              *args, **kwargs) -> Union[dict, None]:
        """
        Search for staff by term. Staff means actors, directors, etc.
        Results are paginated by default. We need to specifies which page we wanted.
        Per page specifies how many per page to request. 10 is just the example from the API docs.

        :param str term: Name to search by
        :param int page: What page are we requesting? Starts at 1.
        :param int per_page: How many results per page? Defaults to 10.
        :return: List of dictionaries which are staff objects or None
        """

        variables = {"query": term, "page": page, "perPage": per_page}
        return self._request(variables, self.DEFAULT_QUERY['staff'], *args, **kwargs)

    def studio(self,
               term: str,
               page: int = 1,
               per_page: int = 10,
               *args, **kwargs) -> Union[dict, None]:
        """
        Search for a studio by term.
        Results are paginated by default. We need to specifies which page we wanted.
        Per page specifies how many per page to request. 10 is just the example from the API docs.

        :param str term: Name to search by
        :param int page: What page are we requesting? starts at 1.
        :param int per_page: How many results per page? defaults to 10.
        :return: List of dictionaries which are studio objects or None
        """

        variables = {"query": term, "page": page, "perPage": per_page}
        return self._request(variables, self.DEFAULT_QUERY['studio'], *args, **kwargs)

    def custom_query(self,
                     variables: dict,
                     query_string: str,
                     *args, **kwargs) -> Union[dict, None]:
        """
        Search for a custom query.
        :param str query_string: Search query
        :param dict variables: Variables to pass to the query.
        :return: Json object with returned results or None.
        """

        return self._request(variables, query_string, *args, **kwargs)
