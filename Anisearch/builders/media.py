"""Media query builder — complete coverage of AniList Media type (55 fields)."""

from Anisearch.builders.base import BaseBuilder, _format_arg_value


class MediaBuilder(BaseBuilder):
    _graphql_type = "Media"

    # --- Scalar fields (22) ---

    def id(self):
        self._add_scalar("id")
        return self

    def id_mal(self):
        self._add_scalar("idMal")
        return self

    def type(self):
        self._add_scalar("type")
        return self

    def format(self):
        self._add_scalar("format")
        return self

    def status(self):
        self._add_scalar("status(version: 2)")
        return self

    def description(self, as_html=False):
        if as_html:
            self._add_scalar("description(asHtml: true)")
        else:
            self._add_scalar("description")
        return self

    def season(self):
        self._add_scalar("season")
        return self

    def season_year(self):
        self._add_scalar("seasonYear")
        return self

    def season_int(self):
        self._add_scalar("seasonInt")
        return self

    def episodes(self):
        self._add_scalar("episodes")
        return self

    def duration(self):
        self._add_scalar("duration")
        return self

    def chapters(self):
        self._add_scalar("chapters")
        return self

    def volumes(self):
        self._add_scalar("volumes")
        return self

    def country_of_origin(self):
        self._add_scalar("countryOfOrigin")
        return self

    def is_licensed(self):
        self._add_scalar("isLicensed")
        return self

    def source(self):
        self._add_scalar("source(version: 3)")
        return self

    def hashtag(self):
        self._add_scalar("hashtag")
        return self

    def updated_at(self):
        self._add_scalar("updatedAt")
        return self

    def banner_image(self):
        self._add_scalar("bannerImage")
        return self

    def genres(self):
        self._add_scalar("genres")
        return self

    def synonyms(self):
        self._add_scalar("synonyms")
        return self

    def average_score(self):
        self._add_scalar("averageScore")
        return self

    def mean_score(self):
        self._add_scalar("meanScore")
        return self

    def popularity(self):
        self._add_scalar("popularity")
        return self

    def is_locked(self):
        self._add_scalar("isLocked")
        return self

    def trending(self):
        self._add_scalar("trending")
        return self

    def favourites(self):
        self._add_scalar("favourites")
        return self

    def is_favourite(self):
        self._add_scalar("isFavourite")
        return self

    def is_favourite_blocked(self):
        self._add_scalar("isFavouriteBlocked")
        return self

    def is_adult(self):
        self._add_scalar("isAdult")
        return self

    def site_url(self):
        self._add_scalar("siteUrl")
        return self

    def auto_create_forum_thread(self):
        self._add_scalar("autoCreateForumThread")
        return self

    def is_recommendation_blocked(self):
        self._add_scalar("isRecommendationBlocked")
        return self

    def is_review_blocked(self):
        self._add_scalar("isReviewBlocked")
        return self

    def mod_notes(self):
        self._add_scalar("modNotes")
        return self

    # --- Object fields (sub-selections) ---

    def title(self, *fields):
        """Sub-fields: "romaji", "english", "native", "userPreferred"."""
        self._add_object("title", fields, defaults=("romaji", "english", "native", "userPreferred"))
        return self

    def cover_image(self, *fields):
        """Sub-fields: "extraLarge", "large", "medium", "color"."""
        self._add_object("coverImage", fields, defaults=("extraLarge", "large", "color"))
        return self

    def start_date(self, *fields):
        self._add_object("startDate", fields, defaults=("year", "month", "day"))
        return self

    def end_date(self, *fields):
        self._add_object("endDate", fields, defaults=("year", "month", "day"))
        return self

    def trailer(self, *fields):
        """Sub-fields: "id", "site", "thumbnail"."""
        self._add_object("trailer", fields, defaults=("id", "site", "thumbnail"))
        return self

    def next_airing_episode(self, *fields):
        """Sub-fields: "id", "airingAt", "timeUntilAiring", "episode", "mediaId"."""
        self._add_object("nextAiringEpisode", fields,
                         defaults=("airingAt", "timeUntilAiring", "episode"))
        return self

    def tags(self, *fields):
        """Sub-fields: "id", "name", "description", "category", "rank",
        "isGeneralSpoiler", "isMediaSpoiler", "isAdult", "userId"."""
        self._add_object("tags", fields,
                         defaults=("id", "name", "description", "category", "rank",
                                   "isGeneralSpoiler", "isMediaSpoiler", "isAdult"))
        return self

    def external_links(self, *fields):
        """Sub-fields: "id", "url", "site", "siteId", "type", "language",
        "color", "icon", "notes", "isDisabled"."""
        self._add_object("externalLinks", fields,
                         defaults=("id", "url", "site", "type", "language", "color", "icon", "notes", "isDisabled"))
        return self

    def streaming_episodes(self, *fields):
        """Sub-fields: "title", "thumbnail", "url", "site"."""
        self._add_object("streamingEpisodes", fields,
                         defaults=("title", "thumbnail", "url", "site"))
        return self

    def rankings(self, *fields):
        """Sub-fields: "id", "rank", "type", "format", "year", "season", "allTime", "context"."""
        self._add_object("rankings", fields,
                         defaults=("id", "rank", "type", "format", "year", "season", "allTime", "context"))
        return self

    def media_list_entry(self, *fields):
        """Sub-fields: any MediaList fields like "id", "status", "score", "progress", etc."""
        self._add_object("mediaListEntry", fields, defaults=("id", "status", "score"))
        return self

    def stats(self, *, fields=None):
        """MediaStats with statusDistribution and scoreDistribution."""
        self._fields.append(
            "stats { statusDistribution { status amount } scoreDistribution { score amount } }"
        )
        return self

    # --- Connection fields (args + sub-builder via lambda) ---

    def characters(self, *, sort=None, role=None, page=None, per_page=None, fields=None):
        """Character connection. Args: sort, role, page, perPage.
        fields: lambda c: c.name("full").image("large")"""
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

    def staff(self, *, sort=None, page=None, per_page=None, fields=None):
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

    def studios(self, *, sort=None, is_main=None, fields=None):
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

    def relations(self, *, fields=None):
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

    def reviews(self, *, limit=None, sort=None, page=None, per_page=None, fields=None):
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

    def recommendations(self, *, sort=None, page=None, per_page=None, fields=None):
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

    def airing_schedule(self, *, not_yet_aired=None, page=None, per_page=None, fields=None):
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

    def trends(self, *, sort=None, releasing=None, page=None, per_page=None, fields=None):
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
