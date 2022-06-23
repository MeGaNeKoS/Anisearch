import json
from typing import Union

import requests


class AnilistSearch:
    def __init__(self, settings):
        self.settings = settings
        self.DEFAULT_QUERY = {"anime": """
                query ($query: String, $page: Int, $perpage: Int) {
                    Page (page: $page, perPage: $perpage) {
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
                query ($query: String, $page: Int, $perpage: Int) {
                    Page (page: $page, perPage: $perpage) {
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
                query ($query: String, $page: Int, $perpage: Int) {
                    Page (page: $page, perPage: $perpage) {
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
                query ($query: String, $page: Int, $perpage: Int) {
                    Page (page: $page, perPage: $perpage) {
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
                query ($query: String, $page: Int, $perpage: Int) {
                    Page (page: $page, perPage: $perpage) {
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
            """}

    def request(self, term, page, per_page, query_string, *, num_retries=10) -> Union[dict, None]:
        variables = {"query": term, "page": page, "perpage": per_page}
        r = requests.post(self.settings['apiurl'],
                          headers=self.settings['header'],
                          json={'query': query_string, 'variables': variables})
        if r.status_code == 429:
            # it hit too many request limit
            import time

            for _ in range(num_retries):
                time.sleep(int(r.headers["Retry-After"]))
                r = requests.post(self.settings['apiurl'],
                                  headers=self.settings['header'],
                                  json={'query': query_string, 'variables': variables})
                if r.status_code != 429:
                    break
        jsd = r.text

        try:
            jsd = json.loads(jsd)
        except ValueError:
            return None
        else:
            return jsd

    def character(self, term: str, page: int = 1, per_page: int = 10, query_string: str = None, *args, **kwargs) -> Union[dict, None]:
        """
        Search for a character by term.
        Results are paginated by default. We need to specifies which page we wanted.
        Per page specifies how many per page to request. 10 is just the example from the API docs.
        
        :param str term: Name to search by
        :param int page: Which page are we requesting? Starts at 1.
        :param int per_page: How many results per page are we requesting? default to 10.
        :param str query_string: What info you interested to?
        :return: Json object with returned results.
        :rtype: Json object with returned results.
        """
        if query_string is None:
            query_string = self.DEFAULT_QUERY["character"]

        return self.request(term, page, per_page, query_string, *args, **kwargs)

    def anime(self, term: str, page: int = 1, per_page: int = 10, query_string: str = None, *args, **kwargs) -> Union[dict, None]:
        """
        Search for an anime by term.
        Results are paginated by default. We need to specifies which page we wanted.
        Per page specifies how many per page to request. 10 is just the example from the API docs.
        
        :param str term: Name to search by
        :param int page: Which page are we requesting? starts at 1.
        :param int per_page : How many results per page? defaults to 10.
        :param str query_string: What info you interested to?
        :param str query_string: What info you interested to?
        :return: List of dictionaries which are anime objects or None
        :rtype: list of dict or NoneType
        """
        if query_string is None:
            query_string = self.DEFAULT_QUERY['anime']
        return self.request(term, page, per_page, query_string, *args, **kwargs)

    def manga(self, term: str, page: int = 1, per_page: int = 10, query_string: str = None, *args, **kwargs) -> Union[dict, None]:
        """
        Search for a manga by term.
        Results are paginated by default. We need to specifies which page we wanted.
        Per page specifies how many per page to request. 10 is just the example from the API docs.
        
        :param str term: Name to search by
        :param int page: Which page are we requesting? Starts at 1.
        :param int per_page: How many results per page? defaults to 10.
        :param str query_string: What info you interested to?
        :return: List of dictionaries which are manga objects or None
        :rtype: list of dict or NoneType
        """
        if query_string is None:
            query_string = self.DEFAULT_QUERY['manga']
        return self.request(term, page, per_page, query_string, *args, **kwargs)

    def staff(self, term: str, page: int = 1, per_page: int = 10, query_string: str = None, *args, **kwargs) -> Union[dict, None]:
        """
        Search for staff by term. Staff means actors, directors, etc.
        Results are paginated by default. We need to specifies which page we wanted.
        Per page specifies how many per page to request. 10 is just the example from the API docs.
        
        :param str term: Name to search by
        :param int page: What page are we requesting? Starts at 1.
        :param int per_page: How many results per page? Defaults to 10.
        :param str query_string: What info you interested to?
        :return: List of dictionaries which are staff objects or None
        :rtype: list of dict or NoneType
        """
        if query_string is None:
            query_string = self.DEFAULT_QUERY['staff']
        return self.request(term, page, per_page, query_string, *args, **kwargs)

    def studio(self, term: str, page: int = 1, per_page: int = 10, query_string: str = None, *args, **kwargs) -> Union[dict, None]:
        """
        Search for a studio by term.
        Results are paginated by default. We need to specifies which page we wanted.
        Per page specifies how many per page to request. 10 is just the example from the API docs.
        
        :param str term: Name to search by
        :param int page: What page are we requesting? starts at 1.
        :param int per_page: How many results per page? defaults to 10.
        :param str query_string: What info you interested to?
        :return: List of dictionaries which are studio objects or None
        :rtype: list of dict or NoneType
        """
        if query_string is None:
            query_string = self.DEFAULT_QUERY['studio']
        return self.request(term, page, per_page, query_string, *args, **kwargs)
