"""Media query builder — complete coverage of AniList Media type (55 fields)."""

from __future__ import annotations

import sys
from typing import Callable, List, Optional

if sys.version_info >= (3, 11):
    from typing import Literal
else:
    from typing_extensions import Literal

from Anisearch.builders.base import BaseBuilder, _format_arg_value
from Anisearch.enums import (
    CHARACTER_ROLE, CHARACTER_SORT, MEDIA_SORT, MEDIA_TREND_SORT,
    RECOMMENDATION_SORT, REVIEW_SORT, STAFF_SORT, STUDIO_SORT,
)


class MediaBuilder(BaseBuilder):
    _graphql_type = "Media"

    @property
    def _response_model(self):
        from Anisearch.models.media import Media
        return Media

    # --- Scalar fields ---

    def id(self) -> MediaBuilder:
        """Select the ``id`` field."""
        self._add_scalar("id")
        return self

    def id_mal(self) -> MediaBuilder:
        """Select the ``idMal`` (MyAnimeList ID) field."""
        self._add_scalar("idMal")
        return self

    def type(self) -> MediaBuilder:
        """Select the ``type`` field (ANIME or MANGA)."""
        self._add_scalar("type")
        return self

    def format(self) -> MediaBuilder:
        """Select the ``format`` field (TV, MOVIE, OVA, etc.)."""
        self._add_scalar("format")
        return self

    def status(self) -> MediaBuilder:
        """Select the ``status`` field (FINISHED, RELEASING, etc.)."""
        self._add_scalar("status(version: 2)")
        return self

    def description(self, as_html: bool = False) -> MediaBuilder:
        """Select the ``description`` field. Set ``as_html=True`` for HTML formatting."""
        if as_html:
            self._add_scalar("description(asHtml: true)")
        else:
            self._add_scalar("description")
        return self

    def season(self) -> MediaBuilder:
        """Select the ``season`` field (WINTER, SPRING, SUMMER, FALL)."""
        self._add_scalar("season")
        return self

    def season_year(self) -> MediaBuilder:
        """Select the ``seasonYear`` field."""
        self._add_scalar("seasonYear")
        return self

    def season_int(self) -> MediaBuilder:
        """Select the ``seasonInt`` field."""
        self._add_scalar("seasonInt")
        return self

    def episodes(self) -> MediaBuilder:
        """Select the ``episodes`` field."""
        self._add_scalar("episodes")
        return self

    def duration(self) -> MediaBuilder:
        """Select the ``duration`` field (minutes per episode)."""
        self._add_scalar("duration")
        return self

    def chapters(self) -> MediaBuilder:
        """Select the ``chapters`` field (manga only)."""
        self._add_scalar("chapters")
        return self

    def volumes(self) -> MediaBuilder:
        """Select the ``volumes`` field (manga only)."""
        self._add_scalar("volumes")
        return self

    def country_of_origin(self) -> MediaBuilder:
        """Select the ``countryOfOrigin`` field (ISO 3166-1 alpha-2)."""
        self._add_scalar("countryOfOrigin")
        return self

    def is_licensed(self) -> MediaBuilder:
        """Select the ``isLicensed`` field."""
        self._add_scalar("isLicensed")
        return self

    def source(self) -> MediaBuilder:
        """Select the ``source`` field (ORIGINAL, MANGA, LIGHT_NOVEL, etc.)."""
        self._add_scalar("source(version: 3)")
        return self

    def hashtag(self) -> MediaBuilder:
        """Select the ``hashtag`` field."""
        self._add_scalar("hashtag")
        return self

    def updated_at(self) -> MediaBuilder:
        """Select the ``updatedAt`` field (unix timestamp)."""
        self._add_scalar("updatedAt")
        return self

    def banner_image(self) -> MediaBuilder:
        """Select the ``bannerImage`` field (URL)."""
        self._add_scalar("bannerImage")
        return self

    def genres(self) -> MediaBuilder:
        """Select the ``genres`` field (list of strings)."""
        self._add_scalar("genres")
        return self

    def synonyms(self) -> MediaBuilder:
        """Select the ``synonyms`` field (alternative titles)."""
        self._add_scalar("synonyms")
        return self

    def average_score(self) -> MediaBuilder:
        """Select the ``averageScore`` field (0-100)."""
        self._add_scalar("averageScore")
        return self

    def mean_score(self) -> MediaBuilder:
        """Select the ``meanScore`` field (0-100)."""
        self._add_scalar("meanScore")
        return self

    def popularity(self) -> MediaBuilder:
        """Select the ``popularity`` field."""
        self._add_scalar("popularity")
        return self

    def is_locked(self) -> MediaBuilder:
        """Select the ``isLocked`` field."""
        self._add_scalar("isLocked")
        return self

    def trending(self) -> MediaBuilder:
        """Select the ``trending`` field."""
        self._add_scalar("trending")
        return self

    def favourites(self) -> MediaBuilder:
        """Select the ``favourites`` field."""
        self._add_scalar("favourites")
        return self

    def is_favourite(self) -> MediaBuilder:
        """Select the ``isFavourite`` field (requires auth)."""
        self._add_scalar("isFavourite")
        return self

    def is_favourite_blocked(self) -> MediaBuilder:
        """Select the ``isFavouriteBlocked`` field."""
        self._add_scalar("isFavouriteBlocked")
        return self

    def is_adult(self) -> MediaBuilder:
        """Select the ``isAdult`` field."""
        self._add_scalar("isAdult")
        return self

    def site_url(self) -> MediaBuilder:
        """Select the ``siteUrl`` field (AniList URL)."""
        self._add_scalar("siteUrl")
        return self

    def auto_create_forum_thread(self) -> MediaBuilder:
        """Select the ``autoCreateForumThread`` field."""
        self._add_scalar("autoCreateForumThread")
        return self

    def is_recommendation_blocked(self) -> MediaBuilder:
        """Select the ``isRecommendationBlocked`` field."""
        self._add_scalar("isRecommendationBlocked")
        return self

    def is_review_blocked(self) -> MediaBuilder:
        """Select the ``isReviewBlocked`` field."""
        self._add_scalar("isReviewBlocked")
        return self

    def mod_notes(self) -> MediaBuilder:
        """Select the ``modNotes`` field (mod only)."""
        self._add_scalar("modNotes")
        return self

    # --- Object fields (sub-selections) ---

    def title(
        self, *fields: Literal["romaji", "english", "native", "userPreferred"]
    ) -> MediaBuilder:
        """Select title sub-fields. Defaults to all if none specified."""
        self._add_object("title", fields, defaults=("romaji", "english", "native", "userPreferred"))
        return self

    def cover_image(
        self, *fields: Literal["extraLarge", "large", "medium", "color"]
    ) -> MediaBuilder:
        """Select cover image sub-fields. Defaults to ``extraLarge``, ``large``, ``color``."""
        self._add_object("coverImage", fields, defaults=("extraLarge", "large", "color"))
        return self

    def start_date(
        self, *fields: Literal["year", "month", "day"]
    ) -> MediaBuilder:
        """Select start date sub-fields. Defaults to all."""
        self._add_object("startDate", fields, defaults=("year", "month", "day"))
        return self

    def end_date(
        self, *fields: Literal["year", "month", "day"]
    ) -> MediaBuilder:
        """Select end date sub-fields. Defaults to all."""
        self._add_object("endDate", fields, defaults=("year", "month", "day"))
        return self

    def trailer(
        self, *fields: Literal["id", "site", "thumbnail"]
    ) -> MediaBuilder:
        """Select trailer sub-fields. Defaults to all."""
        self._add_object("trailer", fields, defaults=("id", "site", "thumbnail"))
        return self

    def next_airing_episode(
        self, *fields: Literal["id", "airingAt", "timeUntilAiring", "episode", "mediaId"]
    ) -> MediaBuilder:
        """Select next airing episode sub-fields. Defaults to ``airingAt``, ``timeUntilAiring``, ``episode``."""
        self._add_object("nextAiringEpisode", fields,
                         defaults=("airingAt", "timeUntilAiring", "episode"))
        return self

    def tags(
        self,
        *fields: Literal[
            "id", "name", "description", "category", "rank",
            "isGeneralSpoiler", "isMediaSpoiler", "isAdult", "userId"
        ]
    ) -> MediaBuilder:
        """Select tag sub-fields. Defaults to all except ``userId``."""
        self._add_object("tags", fields,
                         defaults=("id", "name", "description", "category", "rank",
                                   "isGeneralSpoiler", "isMediaSpoiler", "isAdult"))
        return self

    def external_links(
        self,
        *fields: Literal[
            "id", "url", "site", "siteId", "type", "language",
            "color", "icon", "notes", "isDisabled"
        ]
    ) -> MediaBuilder:
        """Select external link sub-fields. Defaults to all."""
        self._add_object("externalLinks", fields,
                         defaults=("id", "url", "site", "type", "language", "color", "icon", "notes", "isDisabled"))
        return self

    def streaming_episodes(
        self, *fields: Literal["title", "thumbnail", "url", "site"]
    ) -> MediaBuilder:
        """Select streaming episode sub-fields. Defaults to all."""
        self._add_object("streamingEpisodes", fields,
                         defaults=("title", "thumbnail", "url", "site"))
        return self

    def rankings(
        self,
        *fields: Literal[
            "id", "rank", "type", "format", "year", "season", "allTime", "context"
        ]
    ) -> MediaBuilder:
        """Select ranking sub-fields. Defaults to all."""
        self._add_object("rankings", fields,
                         defaults=("id", "rank", "type", "format", "year", "season", "allTime", "context"))
        return self

    def media_list_entry(
        self,
        *fields: Literal[
            "id", "status", "score", "progress", "progressVolumes",
            "repeat", "priority", "private", "notes", "startedAt", "completedAt"
        ]
    ) -> MediaBuilder:
        """Select media list entry sub-fields (requires auth). Defaults to ``id``, ``status``, ``score``."""
        self._add_object("mediaListEntry", fields, defaults=("id", "status", "score"))
        return self

    def stats(self, *, fields: Optional[Callable] = None) -> MediaBuilder:
        """Select stats (``statusDistribution`` and ``scoreDistribution``)."""
        self._fields.append(
            "stats { statusDistribution { status amount } scoreDistribution { score amount } }"
        )
        return self

    # --- Connection fields (args + sub-builder via lambda) ---

    def characters(
        self,
        *,
        sort: Optional[List[CHARACTER_SORT]] = None,
        role: Optional[CHARACTER_ROLE] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        fields: Optional[Callable] = None,
    ) -> MediaBuilder:
        """Nested character connection within this media.

        Note: ``page``/``per_page`` paginate the *characters inside this media*,
        not the top-level query. Use ``.page()`` to paginate media results.
        """
        from Anisearch.builders.character import CharacterBuilder
        args = {}
        if sort is not None:
            args["sort"] = sort
        if role is not None:
            args["role"] = role
        if page is not None:
            args["page"] = page
        if per_page is not None:
            args["perPage"] = per_page
        self._add_connection("characters", args=args, fields_fn=fields,
                             node_type=CharacterBuilder,
                             edge_fields=["id", "role"])
        return self

    def staff(
        self,
        *,
        sort: Optional[List[STAFF_SORT]] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        fields: Optional[Callable] = None,
    ) -> MediaBuilder:
        """Nested staff connection within this media.

        Note: ``page``/``per_page`` paginate the *staff inside this media*,
        not the top-level query. Use ``.page()`` to paginate media results.
        """
        from Anisearch.builders.staff import StaffBuilder
        args = {}
        if sort is not None:
            args["sort"] = sort
        if page is not None:
            args["page"] = page
        if per_page is not None:
            args["perPage"] = per_page
        self._add_connection("staff", args=args, fields_fn=fields,
                             node_type=StaffBuilder,
                             edge_fields=["id", "role"])
        return self

    def studios(
        self,
        *,
        sort: Optional[List[STUDIO_SORT]] = None,
        is_main: Optional[bool] = None,
        fields: Optional[Callable] = None,
    ) -> MediaBuilder:
        from Anisearch.builders.studio import StudioBuilder
        args = {}
        if sort is not None:
            args["sort"] = sort
        if is_main is not None:
            args["isMain"] = is_main
        self._add_connection("studios", args=args, fields_fn=fields,
                             node_type=StudioBuilder,
                             edge_fields=["isMain"])
        return self

    def relations(self, *, fields: Optional[Callable] = None) -> MediaBuilder:
        """Media relations (prequels, sequels, etc.)."""
        if fields:
            sub = MediaBuilder(None, None, "", {})
            fields(sub)
            inner = " ".join(sub._collect_fields()) or "id"
            self._fields.append(
                f"relations {{ edges {{ id relationType(version: 2) node {{ {inner} }} }} }}"
            )
        else:
            self._fields.append(
                "relations { edges { id relationType(version: 2) "
                "node { id title { userPreferred } format type status(version: 2) } } }"
            )
        return self

    def reviews(
        self,
        *,
        limit: Optional[int] = None,
        sort: Optional[List[REVIEW_SORT]] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        fields: Optional[Callable] = None,
    ) -> MediaBuilder:
        """Nested reviews connection within this media.

        Note: ``page``/``per_page`` paginate the *reviews inside this media*,
        not the top-level query. Use ``.page()`` to paginate media results.
        """
        args = {}
        if limit is not None:
            args["limit"] = limit
        if sort is not None:
            args["sort"] = sort
        if page is not None:
            args["page"] = page
        if per_page is not None:
            args["perPage"] = per_page
        arg_str = _build_inline_args(args)
        self._fields.append(f"reviews{arg_str} {{ nodes {{ id summary rating ratingAmount }} }}")
        return self

    def recommendations(
        self,
        *,
        sort: Optional[List[RECOMMENDATION_SORT]] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        fields: Optional[Callable] = None,
    ) -> MediaBuilder:
        """Nested recommendations connection within this media.

        Note: ``page``/``per_page`` paginate the *recommendations inside this media*,
        not the top-level query. Use ``.page()`` to paginate media results.
        """
        args = {}
        if sort is not None:
            args["sort"] = sort
        if page is not None:
            args["page"] = page
        if per_page is not None:
            args["perPage"] = per_page
        arg_str = _build_inline_args(args)
        self._fields.append(
            f"recommendations{arg_str} {{ nodes {{ id rating "
            f"mediaRecommendation {{ id title {{ userPreferred }} }} }} }}"
        )
        return self

    def airing_schedule(
        self,
        *,
        not_yet_aired: Optional[bool] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        fields: Optional[Callable] = None,
    ) -> MediaBuilder:
        """Nested airing schedule connection within this media.

        Note: ``page``/``per_page`` paginate the *schedule inside this media*,
        not the top-level query. Use ``.page()`` to paginate media results.
        """
        args = {}
        if not_yet_aired is not None:
            args["notYetAired"] = not_yet_aired
        if page is not None:
            args["page"] = page
        if per_page is not None:
            args["perPage"] = per_page
        arg_str = _build_inline_args(args)
        self._fields.append(
            f"airingSchedule{arg_str} {{ nodes {{ id airingAt timeUntilAiring episode mediaId }} }}"
        )
        return self

    def trends(
        self,
        *,
        sort: Optional[List[MEDIA_TREND_SORT]] = None,
        releasing: Optional[bool] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        fields: Optional[Callable] = None,
    ) -> MediaBuilder:
        """Nested trends connection within this media.

        Note: ``page``/``per_page`` paginate the *trends inside this media*,
        not the top-level query. Use ``.page()`` to paginate media results.
        """
        args = {}
        if sort is not None:
            args["sort"] = sort
        if releasing is not None:
            args["releasing"] = releasing
        if page is not None:
            args["page"] = page
        if per_page is not None:
            args["perPage"] = per_page
        arg_str = _build_inline_args(args)
        self._fields.append(
            f"trends{arg_str} {{ nodes {{ mediaId date trending popularity inProgress episode }} }}"
        )
        return self


def _build_inline_args(args):
    """Build a parenthesized inline argument string from a dict."""
    if not args:
        return ""
    parts = [f"{k}: {_format_arg_value(v)}" for k, v in args.items() if v is not None]
    return f"({', '.join(parts)})" if parts else ""
