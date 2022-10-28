from typing import Union, List

from Anisearch.datatype import (MEDIA_FORMAT, MEDIA_STATUS, MEDIA_SOURCE, MEDIA_SEASON, MEDIA_SORT,
                                CHARACTER_SORT, STAFF_SORT, STUDIO_SORT)


class AnilistSearch:
    DEFAULT_QUERY = {
        "anime": """
query (
  $page: Int = 1
  $perPage: Int = 10
  $id: Int
  $isAdult: Boolean = false
  $search: String
  $format: [MediaFormat]
  $status: MediaStatus
  $countryOfOrigin: CountryCode
  $source: MediaSource
  $season: MediaSeason
  $seasonYear: Int
  $year: String
  $onList: Boolean
  $yearLesser: FuzzyDateInt
  $yearGreater: FuzzyDateInt
  $episodeLesser: Int
  $episodeGreater: Int
  $durationLesser: Int
  $durationGreater: Int
  $chapterLesser: Int
  $chapterGreater: Int
  $volumeLesser: Int
  $volumeGreater: Int
  $licensedBy: [Int]
  $isLicensed: Boolean
  $genres: [String]
  $excludedGenres: [String]
  $tags: [String]
  $excludedTags: [String]
  $minimumTagRank: Int
  $sort: [MediaSort] = [POPULARITY_DESC, SCORE_DESC]
) {
  Page(page: $page, perPage: $perPage) {
    pageInfo {
      total
      perPage
      currentPage
      lastPage
      hasNextPage
    }
    media(
      id: $id
      type: ANIME
      season: $season
      format_in: $format
      status: $status
      countryOfOrigin: $countryOfOrigin
      source: $source
      search: $search
      onList: $onList
      seasonYear: $seasonYear
      startDate_like: $year
      startDate_lesser: $yearLesser
      startDate_greater: $yearGreater
      episodes_lesser: $episodeLesser
      episodes_greater: $episodeGreater
      duration_lesser: $durationLesser
      duration_greater: $durationGreater
      chapters_lesser: $chapterLesser
      chapters_greater: $chapterGreater
      volumes_lesser: $volumeLesser
      volumes_greater: $volumeGreater
      licensedById_in: $licensedBy
      isLicensed: $isLicensed
      genre_in: $genres
      genre_not_in: $excludedGenres
      tag_in: $tags
      tag_not_in: $excludedTags
      minimumTagRank: $minimumTagRank
      sort: $sort
      isAdult: $isAdult
    ) {
      id
      title {
        userPreferred
      }
      coverImage {
        extraLarge
        large
        color
      }
      startDate {
        year
        month
        day
      }
      endDate {
        year
        month
        day
      }
      bannerImage
      season
      seasonYear
      description
      type
      format
      status(version: 2)
      episodes
      duration
      chapters
      volumes
      genres
      isAdult
      averageScore
      popularity
      nextAiringEpisode {
        airingAt
        timeUntilAiring
        episode
      }
      mediaListEntry {
        id
        status
      }
      studios(isMain: true) {
        edges {
          isMain
          node {
            id
            name
          }
        }
      }
    }
  }
}
            """,
        "manga": """
query (
  $page: Int = 1
  $id: Int
  $isAdult: Boolean = false
  $search: String
  $format: [MediaFormat]
  $status: MediaStatus
  $countryOfOrigin: CountryCode
  $source: MediaSource
  $season: MediaSeason
  $seasonYear: Int
  $year: String
  $onList: Boolean
  $yearLesser: FuzzyDateInt
  $yearGreater: FuzzyDateInt
  $episodeLesser: Int
  $episodeGreater: Int
  $durationLesser: Int
  $durationGreater: Int
  $chapterLesser: Int
  $chapterGreater: Int
  $volumeLesser: Int
  $volumeGreater: Int
  $licensedBy: [Int]
  $isLicensed: Boolean
  $genres: [String]
  $excludedGenres: [String]
  $tags: [String]
  $excludedTags: [String]
  $minimumTagRank: Int
  $sort: [MediaSort] = [POPULARITY_DESC, SCORE_DESC]
) {
  Page(page: $page, perPage: 20) {
    pageInfo {
      total
      perPage
      currentPage
      lastPage
      hasNextPage
    }
    media(
      id: $id
      type: MANGA
      season: $season
      format_in: $format
      status: $status
      countryOfOrigin: $countryOfOrigin
      source: $source
      search: $search
      onList: $onList
      seasonYear: $seasonYear
      startDate_like: $year
      startDate_lesser: $yearLesser
      startDate_greater: $yearGreater
      episodes_lesser: $episodeLesser
      episodes_greater: $episodeGreater
      duration_lesser: $durationLesser
      duration_greater: $durationGreater
      chapters_lesser: $chapterLesser
      chapters_greater: $chapterGreater
      volumes_lesser: $volumeLesser
      volumes_greater: $volumeGreater
      licensedById_in: $licensedBy
      isLicensed: $isLicensed
      genre_in: $genres
      genre_not_in: $excludedGenres
      tag_in: $tags
      tag_not_in: $excludedTags
      minimumTagRank: $minimumTagRank
      sort: $sort
      isAdult: $isAdult
    ) {
      id
      title {
        userPreferred
      }
      coverImage {
        extraLarge
        large
        color
      }
      startDate {
        year
        month
        day
      }
      endDate {
        year
        month
        day
      }
      bannerImage
      season
      seasonYear
      description
      type
      format
      status(version: 2)
      episodes
      duration
      chapters
      volumes
      genres
      isAdult
      averageScore
      popularity
      nextAiringEpisode {
        airingAt
        timeUntilAiring
        episode
      }
      mediaListEntry {
        id
        status
      }
      studios(isMain: true) {
        edges {
          isMain
          node {
            id
            name
          }
        }
      }
    }
  }
}
            """,
        "staff": """
query (
  $page: Int = 1
  $id: Int
  $search: String
  $isBirthday: Boolean
  $sort: [StaffSort] = [FAVOURITES_DESC]
) {
  Page(page: $page, perPage: 20) {
    pageInfo {
      total
      perPage
      currentPage
      lastPage
      hasNextPage
    }
    staff(id: $id, search: $search, isBirthday: $isBirthday, sort: $sort) {
      id
      name {
        userPreferred
      }
      image {
        large
      }
    }
  }
}
            """,
        "studio": """
query (
  $page: Int = 1
  $id: Int
  $search: String
  $sort: [StudioSort] = [SEARCH_MATCH]
) {
  Page(page: $page, perPage: 20) {
    pageInfo {
      total
      perPage
      currentPage
      lastPage
      hasNextPage
    }
    studios(id: $id, search: $search, sort: $sort) {
      id
      name
    }
  }
}
            """,
        "character": """
query (
  $page: Int = 1
  $id: Int
  $search: String
  $isBirthday: Boolean
  $sort: [CharacterSort] = [FAVOURITES_DESC]
) {
  Page(page: $page, perPage: 20) {
    pageInfo {
      total
      perPage
      currentPage
      lastPage
      hasNextPage
    }
    characters(id: $id, search: $search, isBirthday: $isBirthday, sort: $sort) {
      id
      name {
        userPreferred
      }
      image {
        large
      }
    }
  }
}
            """
    }

    def __init__(self, request: callable):
        self.request = request

    def anime(self,
              search: str = None,
              page: int = 1,
              per_page: int = 10,
              is_adult: bool = False,
              *args,
              anime_id: int = None,
              media_format: List[MEDIA_FORMAT] = None,
              status: MEDIA_STATUS = None,
              country_of_origin=None,
              source: MEDIA_SOURCE = None,
              season: MEDIA_SEASON = None,
              season_year: int = None,
              year: str = None,
              on_list: bool = None,
              year_lesser: int = None,
              year_greater: int = None,
              episode_lesser: int = None,
              episode_greater: int = None,
              duration_lesser: int = None,
              duration_greater: int = None,
              chapter_lesser: int = None,
              chapter_greater: int = None,
              volume_lesser: int = None,
              volume_greater: int = None,
              licensed_by: List[int] = None,
              is_licensed: bool = None,
              genres: List[str] = None,
              excluded_genres: List[str] = None,
              tags: List[str] = None,
              excluded_tags: List[str] = None,
              minimum_tag_rank: int = None,
              sort: List[MEDIA_SORT] = None,
              **kwargs) -> Union[dict, None]:
        """
        Search for an anime by term.
        Results are paginated by default. We need to specify which page we wanted.
        Per page specifies how many per page to request. 10 is just the example from the API docs.

        :param search: Search term
        :param page: Page number to request
        :param per_page: Number of results per page
        :param is_adult: Whether the anime is adult or not
        :param anime_id: ID of the anime
        :param media_format: Format of the anime
        :param status: Status of the anime
        :param country_of_origin: Country of origin
        :param source: Source of the anime
        :param season: Season of the anime
        :param season_year: Year of the season
        :param year: Year of the anime
        :param on_list: Whether the anime is on the list or not
        :param year_lesser: Year lesser than
        :param year_greater: Year greater than
        :param episode_lesser: Episode lesser than
        :param episode_greater: Episode greater than
        :param duration_lesser: Duration lesser than
        :param duration_greater: Duration greater than
        :param chapter_lesser: Chapter lesser than
        :param chapter_greater: Chapter greater than
        :param volume_lesser: Volume lesser than
        :param volume_greater: Volume greater than
        :param licensed_by: Licensed by
        :param is_licensed: Whether the anime is licensed or not
        :param genres: Genres of the anime
        :param excluded_genres: Excluded genres of the anime
        :param tags: Tags of the anime
        :param excluded_tags: Excluded tags of the anime
        :param minimum_tag_rank: Minimum tag rank
        :param sort: Sort by
        :return: List of dictionaries which are anime objects or None
        """

        variables = {
            "page": page,
            "perPage": per_page,
            "id": anime_id,
            "isAdult": is_adult,
            "search": search,
            "format": media_format,
            "status": status,
            "countryOfOrigin": country_of_origin,
            "source": source,
            "season": season,
            "seasonYear": season_year,
            "year": year,
            "onList": on_list,
            "yearLesser": year_lesser,
            "yearGreater": year_greater,
            "episodeLesser": episode_lesser,
            "episodeGreater": episode_greater,
            "durationLesser": duration_lesser,
            "durationGreater": duration_greater,
            "chapterLesser": chapter_lesser,
            "chapterGreater": chapter_greater,
            "volumeLesser": volume_lesser,
            "volumeGreater": volume_greater,
            "licensedBy": licensed_by,
            "isLicensed": is_licensed,
            "genres": genres,
            "excludedGenres": excluded_genres,
            "tags": tags,
            "excludedTags": excluded_tags,
            "minimumTagRank": minimum_tag_rank,
            "sort": sort
        }

        return self.request(variables, AnilistSearch.DEFAULT_QUERY['anime'], *args, **kwargs)

    def character(self,
                  search: str = None,
                  page: int = 1,
                  per_page: int = 10,
                  *args,
                  character_id: int = None,
                  is_birthday: bool = None,
                  sort: List[CHARACTER_SORT] = None,
                  **kwargs) -> Union[dict, None]:
        """
        Search for a character by term.
        Results are paginated by default. We need to specify which page we wanted.
        Per page specifies how many per page to request. 10 is just the example from the API docs.

        :param str search: Search term
        :param int page: Page number to request
        :param int per_page: Number of results per page
        :param int character_id: ID of the character
        :param bool is_birthday: Whether the character has a birthday or not
        :param List[CHARACTER_SORT] sort: Sort by
        :return: List of dictionaries which are character objects or None
        """

        variables = {
            "page": page,
            "perPage": per_page,
            "id": character_id,
            "search": search,
            "isBirthday": is_birthday,
            "sort": sort
        }
        return self.request(variables, AnilistSearch.DEFAULT_QUERY['character'], *args, **kwargs)

    def manga(self,
              search: str = None,
              page: int = 1,
              per_page: int = 10,
              is_adult: bool = False,
              *args,
              manga_id: int = None,
              media_format: List[MEDIA_FORMAT] = None,
              status: MEDIA_STATUS = None,
              country_of_origin=None,
              source: MEDIA_SOURCE = None,
              season: MEDIA_SEASON = None,
              season_year: int = None,
              year: str = None,
              on_list: bool = None,
              year_lesser: int = None,
              year_greater: int = None,
              episode_lesser: int = None,
              episode_greater: int = None,
              duration_lesser: int = None,
              duration_greater: int = None,
              chapter_lesser: int = None,
              chapter_greater: int = None,
              volume_lesser: int = None,
              volume_greater: int = None,
              licensed_by: List[int] = None,
              is_licensed: bool = None,
              genres: List[str] = None,
              excluded_genres: List[str] = None,
              tags: List[str] = None,
              excluded_tags: List[str] = None,
              minimum_tag_rank: int = None,
              sort: List[MEDIA_SORT] = None,
              **kwargs) -> Union[dict, None]:
        """
        Search for a manga by term.
        Results are paginated by default. We need to specifies which page we wanted.
        Per page specifies how many per page to request. 10 is just the example from the API docs.


        :param str search: Search term
        :param int page: Page number to request
        :param int per_page: Number of results per page
        :param bool is_adult: Whether the manga is adult or not
        :param int manga_id: ID of the manga
        :param str media_format: Format of the manga
        :param str status: Status of the manga
        :param str country_of_origin: Country of origin
        :param str source: Source of the manga
        :param str season: Season of the manga
        :param int season_year: Year of the season
        :param int year: Year of the manga
        :param bool on_list: Whether the manga is on the list or not
        :param int year_lesser: Year lesser than
        :param int year_greater: Year greater than
        :param int episode_lesser: Episode lesser than
        :param int episode_greater: Episode greater than
        :param int duration_lesser: Duration lesser than
        :param int duration_greater: Duration greater than
        :param int chapter_lesser: Chapter lesser than
        :param int chapter_greater: Chapter greater than
        :param int volume_lesser: Volume lesser than
        :param int volume_greater: Volume greater than
        :param str licensed_by: Licensed by
        :param bool is_licensed: Whether the manga is licensed or not
        :param str genres: Genres of the manga
        :param str excluded_genres: Excluded genres of the manga
        :param str tags: Tags of the manga
        :param str excluded_tags: Excluded tags of the manga
        :param int minimum_tag_rank: Minimum tag rank
        :param str sort: Sort by

        :return: List of dictionaries which are manga objects or None
        """

        variables = {
            "page": page,
            "perPage": per_page,
            "id": manga_id,
            "isAdult": is_adult,
            "search": search,
            "format": media_format,
            "status": status,
            "countryOfOrigin": country_of_origin,
            "source": source,
            "season": season,
            "seasonYear": season_year,
            "year": year,
            "onList": on_list,
            "yearLesser": year_lesser,
            "yearGreater": year_greater,
            "episodeLesser": episode_lesser,
            "episodeGreater": episode_greater,
            "durationLesser": duration_lesser,
            "durationGreater": duration_greater,
            "chapterLesser": chapter_lesser,
            "chapterGreater": chapter_greater,
            "volumeLesser": volume_lesser,
            "volumeGreater": volume_greater,
            "licensedBy": licensed_by,
            "isLicensed": is_licensed,
            "genres": genres,
            "excludedGenres": excluded_genres,
            "tags": tags,
            "excludedTags": excluded_tags,
            "minimumTagRank": minimum_tag_rank,
            "sort": sort
        }
        return self.request(variables, AnilistSearch.DEFAULT_QUERY['manga'], *args, **kwargs)

    def staff(self,
              search: str = None,
              page: int = 1,
              per_page: int = 10,
              *args,
              staff_id: int = None,
              sort: List[STAFF_SORT] = None,
              **kwargs) -> Union[dict, None]:
        """
        Search for staff by term. Staff means actors, directors, etc.
        Results are paginated by default. We need to specify which page we wanted.
        Per page specifies how many per page to request. 10 is just the example from the API docs.

        :param str search: Search term
        :param int page: Page number to request
        :param int per_page: Number of results per page
        :param int staff_id: ID of the staff
        :param str sort: Sort by
        :return: List of dictionaries which are staff objects or None
        """

        variables = {
            "page": page,
            "perPage": per_page,
            "id": staff_id,
            "search": search,
            "sort": sort
        }
        return self.request(variables, AnilistSearch.DEFAULT_QUERY['staff'], *args, **kwargs)

    def studio(self,
               search: str = None,
               page: int = 1,
               per_page: int = 10,
               *args,
               studio_id: int = None,
               sort: List[STUDIO_SORT] = None,
               **kwargs) -> Union[dict, None]:
        """
        Search for a studio by term.
        Results are paginated by default. We need to specify which page we wanted.
        Per page specifies how many per page to request. 10 is just the example from the API docs.

        :param str search: Search term
        :param int page: Page number to request
        :param int per_page: Number of results per page
        :param int studio_id: ID of the studio
        :param str sort: Sort by
        :return: List of dictionaries which are studio objects or None
        """

        variables = {
            "page": page,
            "perPage": per_page,
            "id": studio_id,
            "search": search,
            "sort": sort
        }
        return self.request(variables, AnilistSearch.DEFAULT_QUERY['studio'], *args, **kwargs)

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

        return self.request(variables, query_string, *args, **kwargs)
