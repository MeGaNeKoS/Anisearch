from typing import Union, List

from Anisearch.datatype import MEDIA_SORT, MEDIA_TYPE


class AnilistGet:
    DEFAULT_QUERY = {
        "anime": """
query media($id: Int, $isAdult: Boolean) {
  Media(id: $id, type: ANIME, isAdult: $isAdult) {
    id
    title {
      userPreferred
      romaji
      english
      native
    }
    coverImage {
      extraLarge
      large
    }
    bannerImage
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
    description
    season
    seasonYear
    type
    format
    status(version: 2)
    episodes
    duration
    chapters
    volumes
    genres
    synonyms
    source(version: 3)
    isAdult
    isLocked
    meanScore
    averageScore
    popularity
    favourites
    isFavouriteBlocked
    hashtag
    countryOfOrigin
    isLicensed
    isFavourite
    isRecommendationBlocked
    isFavouriteBlocked
    isReviewBlocked
    nextAiringEpisode {
      airingAt
      timeUntilAiring
      episode
    }
    relations {
      edges {
        id
        relationType(version: 2)
        node {
          id
          title {
            userPreferred
          }
          format
          type
          status(version: 2)
          bannerImage
          coverImage {
            large
          }
        }
      }
    }
    characterPreview: characters(perPage: 6, sort: [ROLE, RELEVANCE, ID]) {
      edges {
        id
        role
        name
        voiceActors(language: JAPANESE, sort: [RELEVANCE, ID]) {
          id
          name {
            userPreferred
          }
          language: languageV2
          image {
            large
          }
        }
        node {
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
    staffPreview: staff(perPage: 8, sort: [RELEVANCE, ID]) {
      edges {
        id
        role
        node {
          id
          name {
            userPreferred
          }
          language: languageV2
          image {
            large
          }
        }
      }
    }
    studios {
      edges {
        isMain
        node {
          id
          name
        }
      }
    }
    reviewPreview: reviews(perPage: 2, sort: [RATING_DESC, ID]) {
      pageInfo {
        total
      }
      nodes {
        id
        summary
        rating
        ratingAmount
        user {
          id
          name
          avatar {
            large
          }
        }
      }
    }
    recommendations(perPage: 7, sort: [RATING_DESC, ID]) {
      pageInfo {
        total
      }
      nodes {
        id
        rating
        userRating
        mediaRecommendation {
          id
          title {
            userPreferred
          }
          format
          type
          status(version: 2)
          bannerImage
          coverImage {
            large
          }
        }
        user {
          id
          name
          avatar {
            large
          }
        }
      }
    }
    externalLinks {
      id
      site
      url
      type
      language
      color
      icon
      notes
      isDisabled
    }
    streamingEpisodes {
      site
      title
      thumbnail
      url
    }
    trailer {
      id
      site
    }
    rankings {
      id
      rank
      type
      format
      year
      season
      allTime
      context
    }
    tags {
      id
      name
      description
      rank
      isMediaSpoiler
      isGeneralSpoiler
      userId
    }
    mediaListEntry {
      id
      status
      score
    }
    stats {
      statusDistribution {
        status
        amount
      }
      scoreDistribution {
        score
        amount
      }
    }
  }
}
            """,
        "manga": """
query media($id: Int, $isAdult: Boolean) {
  Media(id: $id, type: MANGA, isAdult: $isAdult) {
    id
    title {
      userPreferred
      romaji
      english
      native
    }
    coverImage {
      extraLarge
      large
    }
    bannerImage
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
    description
    season
    seasonYear
    type
    format
    status(version: 2)
    episodes
    duration
    chapters
    volumes
    genres
    synonyms
    source(version: 3)
    isAdult
    isLocked
    meanScore
    averageScore
    popularity
    favourites
    isFavouriteBlocked
    hashtag
    countryOfOrigin
    isLicensed
    isFavourite
    isRecommendationBlocked
    isFavouriteBlocked
    isReviewBlocked
    nextAiringEpisode {
      airingAt
      timeUntilAiring
      episode
    }
    relations {
      edges {
        id
        relationType(version: 2)
        node {
          id
          title {
            userPreferred
          }
          format
          type
          status(version: 2)
          bannerImage
          coverImage {
            large
          }
        }
      }
    }
    characterPreview: characters(perPage: 6, sort: [ROLE, RELEVANCE, ID]) {
      edges {
        id
        role
        name
        voiceActors(language: JAPANESE, sort: [RELEVANCE, ID]) {
          id
          name {
            userPreferred
          }
          language: languageV2
          image {
            large
          }
        }
        node {
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
    staffPreview: staff(perPage: 8, sort: [RELEVANCE, ID]) {
      edges {
        id
        role
        node {
          id
          name {
            userPreferred
          }
          language: languageV2
          image {
            large
          }
        }
      }
    }
    studios {
      edges {
        isMain
        node {
          id
          name
        }
      }
    }
    reviewPreview: reviews(perPage: 2, sort: [RATING_DESC, ID]) {
      pageInfo {
        total
      }
      nodes {
        id
        summary
        rating
        ratingAmount
        user {
          id
          name
          avatar {
            large
          }
        }
      }
    }
    recommendations(perPage: 7, sort: [RATING_DESC, ID]) {
      pageInfo {
        total
      }
      nodes {
        id
        rating
        userRating
        mediaRecommendation {
          id
          title {
            userPreferred
          }
          format
          type
          status(version: 2)
          bannerImage
          coverImage {
            large
          }
        }
        user {
          id
          name
          avatar {
            large
          }
        }
      }
    }
    externalLinks {
      id
      site
      url
      type
      language
      color
      icon
      notes
      isDisabled
    }
    streamingEpisodes {
      site
      title
      thumbnail
      url
    }
    trailer {
      id
      site
    }
    rankings {
      id
      rank
      type
      format
      year
      season
      allTime
      context
    }
    tags {
      id
      name
      description
      rank
      isMediaSpoiler
      isGeneralSpoiler
      userId
    }
    mediaListEntry {
      id
      status
      score
    }
    stats {
      statusDistribution {
        status
        amount
      }
      scoreDistribution {
        score
        amount
      }
    }
  }
}
            """,
        "staff": """
query staff(
  $id: Int
  $sort: [MediaSort]
  $characterPage: Int
  $staffPage: Int
  $onList: Boolean
  $type: MediaType
  $withCharacterRoles: Boolean = false
  $withStaffRoles: Boolean = false
) {
  Staff(id: $id) {
    id
    name {
      first
      middle
      last
      full
      native
      userPreferred
      alternative
    }
    image {
      large
    }
    description
    favourites
    isFavourite
    isFavouriteBlocked
    age
    gender
    yearsActive
    homeTown
    bloodType
    primaryOccupations
    dateOfBirth {
      year
      month
      day
    }
    dateOfDeath {
      year
      month
      day
    }
    language: languageV2
    characterMedia(page: $characterPage, sort: $sort, onList: $onList)
      @include(if: $withCharacterRoles) {
      pageInfo {
        total
        perPage
        currentPage
        lastPage
        hasNextPage
      }
      edges {
        characterRole
        characterName
        node {
          id
          type
          bannerImage
          isAdult
          title {
            userPreferred
          }
          coverImage {
            large
          }
          startDate {
            year
          }
          mediaListEntry {
            id
            status
          }
        }
        characters {
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
    staffMedia(page: $staffPage, type: $type, sort: $sort, onList: $onList)
      @include(if: $withStaffRoles) {
      pageInfo {
        total
        perPage
        currentPage
        lastPage
        hasNextPage
      }
      edges {
        staffRole
        node {
          id
          type
          isAdult
          title {
            userPreferred
          }
          coverImage {
            large
          }
          mediaListEntry {
            id
            status
          }
        }
      }
    }
  }
}

            """,
        "studio": """
query ($id: Int, $page: Int, $sort: [MediaSort], $onList: Boolean) {
  Studio(id: $id) {
    id
    name
    isAnimationStudio
    favourites
    isFavourite
    media(page: $page, sort: $sort, onList: $onList) {
      pageInfo {
        total
        perPage
        currentPage
        lastPage
        hasNextPage
      }
      edges {
        isMainStudio
        node {
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
          mediaListEntry {
            id
            status
          }
          nextAiringEpisode {
            airingAt
            timeUntilAiring
            episode
          }
        }
      }
    }
  }
}
            """,
        "character": """
query character(
  $id: Int
  $page: Int
  $sort: [MediaSort]
  $onList: Boolean
  $withRoles: Boolean = false
) {
  Character(id: $id) {
    id
    name {
      first
      middle
      last
      full
      native
      userPreferred
      alternative
      alternativeSpoiler
    }
    image {
      large
    }
    favourites
    isFavourite
    isFavouriteBlocked
    description
    age
    gender
    bloodType
    dateOfBirth {
      year
      month
      day
    }
    media(page: $page, sort: $sort, onList: $onList) @include(if: $withRoles) {
      pageInfo {
        total
        perPage
        currentPage
        lastPage
        hasNextPage
      }
      edges {
        id
        characterRole
        voiceActorRoles(sort: [RELEVANCE, ID]) {
          roleNotes
          voiceActor {
            id
            name {
              userPreferred
            }
            image {
              large
            }
            language: languageV2
          }
        }
        node {
          id
          type
          isAdult
          bannerImage
          title {
            userPreferred
          }
          coverImage {
            large
          }
          startDate {
            year
          }
          mediaListEntry {
            id
            status
          }
        }
      }
    }
  }
}

            """
    }

    def __init__(self, request: callable):
        """
        :param request: callable that takes a query and returns a json
        """
        self.request = request

    def anime(self, item_id: int, is_adult=False, *args, **kwargs) -> Union[dict, None]:
        """
        The function to retrieve an anime's details.

        :param int item_id: the anime's ID
        :param bool is_adult: whether the anime is adult or not
        :return: List of dictionaries which are anime objects or None
        """

        variables = {
            "id": item_id,
            "isAdult": is_adult
        }
        return self.request(variables, AnilistGet.DEFAULT_QUERY["anime"], *args, **kwargs)

    def character(self,
                  item_id: int,
                  page: int = None,
                  *args,
                  sort: List[MEDIA_SORT] = None,
                  on_list=None,
                  with_roles=False,
                  **kwargs) -> dict:
        """
        The function to retrieve a character's details.

        :param int item_id: the anime's ID
        :param int page: the page number
        :param list[MEDIA_SORT] sort: the sort order
        :param bool on_list: whether the anime is on the user's list or not
        :param bool with_roles: whether to include the character's roles or not
        :return: List of dictionaries which are character objects or None
        """
        variables = {
            "id": item_id,
            "page": page,
            "sort": sort,
            "onList": on_list,
            "withRoles": with_roles
        }

        return self.request(variables, AnilistGet.DEFAULT_QUERY["character"], *args, **kwargs)

    def manga(self,
              item_id: int,
              is_adult=False,
              *args, **kwargs) -> Union[dict, None]:
        """
        The function to retrieve a character's details.

        :param int item_id: the anime's ID
        :param bool is_adult: whether the anime is adult or not
        :return: List of dictionaries which are character objects or None
        """
        variables = {
            "id": item_id,
            "isAdult": is_adult
        }
        return self.request(variables, AnilistGet.DEFAULT_QUERY["manga"], *args, **kwargs)

    def staff(self,
              item_id: int,
              *args,
              sort: List[MEDIA_SORT] = None,
              character_page=None,
              staff_page=None,
              on_list=None,
              media_type: MEDIA_TYPE = None,
              with_character_roles=False,
              with_staff_roles=False,
              **kwargs) -> Union[dict, None]:
        """
        The function to retrieve a character's details.

        :param int item_id: the anime's ID
        :param List[MEDIA_SORT] sort: the sort order for the character's media
        :param character_page: the page of characters
        :param staff_page: the page of staff
        :param on_list: whether the media is on the user's list or not
        :param MediaType media_type: the type of media
        :param with_character_roles: whether to include character roles or not
        :param with_staff_roles: whether to include staff roles or not
        :return: List of dictionaries which are character objects or None
        """
        variables = {
            "id": item_id,
            "sort": sort,
            "characterPage": character_page,
            "staffPage": staff_page,
            "onList": on_list,
            "type": media_type,
            "withCharacterRoles": with_character_roles,
            "withStaffRoles": with_staff_roles
        }
        return self.request(variables, AnilistGet.DEFAULT_QUERY["staff"], *args, **kwargs)

    def studio(self,
               item_id: int,
               page: int = None,
               *args,
               sort: List[MEDIA_SORT] = None,
               on_list: bool = None,
               **kwargs) -> Union[dict, None]:
        """

        The function to retrieve a character's details.

        :param int item_id: the anime's ID
        :param int page: the page of characters
        :param List[MEDIA_SORT] sort: the sort order for the character's media
        :param bool on_list: whether the media is on the user's list or not\
        :return: List of dictionaries which are character objects or None
        """
        variables = {
            "id": item_id,
            "page": page,
            "sort": sort,
            "onList": on_list
        }
        return self.request(variables, AnilistGet.DEFAULT_QUERY["studio"], *args, **kwargs)

    def custom_query(self, variables: dict, query_string: str, *args, **kwargs) -> Union[dict, None]:
        """
        The function to retrieve custom query.

        :param str query_string: the query string
        :param dict variables: the variables
        :return: List of dictionaries objects or None
        """

        return self.request(variables, query_string, *args, **kwargs)
