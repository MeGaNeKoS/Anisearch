"""Unit tests for the declarative GraphQL builder system."""

import unittest
from unittest.mock import patch, MagicMock

from Anisearch import Anilist, Fragment
from Anisearch.builders.media import MediaBuilder
from Anisearch.builders.character import CharacterBuilder
from Anisearch.builders.staff import StaffBuilder
from Anisearch.builders.studio import StudioBuilder
from Anisearch.builders.page import PageBuilder
from Anisearch.builders.base import _format_arg_value, _infer_type, _root_to_collection
from Anisearch.retry import RetryStrategy
from Anisearch.errors import (
    AnilistError, RateLimitError, ServerError, GraphQLError,
    ConnectionError as AnilistConnectionError,
)
from Anisearch.models import Media, Character, Staff, Studio, PageResult


def _make_builder(cls, root_field, root_args=None):
    """Create a builder without a real connection for testing compilation."""
    return cls(None, None, root_field, root_args or {})


# ============================================================
# MediaBuilder — Scalar fields
# ============================================================

class TestMediaScalarFields(unittest.TestCase):
    def _build(self, fn):
        b = _make_builder(MediaBuilder, "Media", {"id": 1})
        fn(b)
        query, _ = b._compile()
        return query

    def test_id(self):
        self.assertIn("id", self._build(lambda b: b.id()))

    def test_id_mal(self):
        self.assertIn("idMal", self._build(lambda b: b.id_mal()))

    def test_type(self):
        self.assertIn("type", self._build(lambda b: b.type()))

    def test_format(self):
        self.assertIn("format", self._build(lambda b: b.format()))

    def test_status_version(self):
        self.assertIn("status(version: 2)", self._build(lambda b: b.status()))

    def test_description(self):
        self.assertIn("description", self._build(lambda b: b.description()))

    def test_description_as_html(self):
        self.assertIn("description(asHtml: true)", self._build(lambda b: b.description(as_html=True)))

    def test_season(self):
        self.assertIn("season", self._build(lambda b: b.season()))

    def test_season_year(self):
        self.assertIn("seasonYear", self._build(lambda b: b.season_year()))

    def test_season_int(self):
        self.assertIn("seasonInt", self._build(lambda b: b.season_int()))

    def test_episodes(self):
        self.assertIn("episodes", self._build(lambda b: b.episodes()))

    def test_duration(self):
        self.assertIn("duration", self._build(lambda b: b.duration()))

    def test_chapters(self):
        self.assertIn("chapters", self._build(lambda b: b.chapters()))

    def test_volumes(self):
        self.assertIn("volumes", self._build(lambda b: b.volumes()))

    def test_country_of_origin(self):
        self.assertIn("countryOfOrigin", self._build(lambda b: b.country_of_origin()))

    def test_is_licensed(self):
        self.assertIn("isLicensed", self._build(lambda b: b.is_licensed()))

    def test_source(self):
        self.assertIn("source(version: 3)", self._build(lambda b: b.source()))

    def test_hashtag(self):
        self.assertIn("hashtag", self._build(lambda b: b.hashtag()))

    def test_updated_at(self):
        self.assertIn("updatedAt", self._build(lambda b: b.updated_at()))

    def test_banner_image(self):
        self.assertIn("bannerImage", self._build(lambda b: b.banner_image()))

    def test_genres(self):
        self.assertIn("genres", self._build(lambda b: b.genres()))

    def test_synonyms(self):
        self.assertIn("synonyms", self._build(lambda b: b.synonyms()))

    def test_average_score(self):
        self.assertIn("averageScore", self._build(lambda b: b.average_score()))

    def test_mean_score(self):
        self.assertIn("meanScore", self._build(lambda b: b.mean_score()))

    def test_popularity(self):
        self.assertIn("popularity", self._build(lambda b: b.popularity()))

    def test_is_locked(self):
        self.assertIn("isLocked", self._build(lambda b: b.is_locked()))

    def test_trending(self):
        self.assertIn("trending", self._build(lambda b: b.trending()))

    def test_favourites(self):
        self.assertIn("favourites", self._build(lambda b: b.favourites()))

    def test_is_favourite(self):
        self.assertIn("isFavourite", self._build(lambda b: b.is_favourite()))

    def test_is_favourite_blocked(self):
        self.assertIn("isFavouriteBlocked", self._build(lambda b: b.is_favourite_blocked()))

    def test_is_adult(self):
        self.assertIn("isAdult", self._build(lambda b: b.is_adult()))

    def test_site_url(self):
        self.assertIn("siteUrl", self._build(lambda b: b.site_url()))

    def test_auto_create_forum_thread(self):
        self.assertIn("autoCreateForumThread", self._build(lambda b: b.auto_create_forum_thread()))

    def test_is_recommendation_blocked(self):
        self.assertIn("isRecommendationBlocked", self._build(lambda b: b.is_recommendation_blocked()))

    def test_is_review_blocked(self):
        self.assertIn("isReviewBlocked", self._build(lambda b: b.is_review_blocked()))

    def test_mod_notes(self):
        self.assertIn("modNotes", self._build(lambda b: b.mod_notes()))


# ============================================================
# MediaBuilder — Object fields (sub-selections)
# ============================================================

class TestMediaObjectFields(unittest.TestCase):
    def _build(self, fn):
        b = _make_builder(MediaBuilder, "Media", {"id": 1})
        fn(b)
        query, _ = b._compile()
        return query

    def test_title_defaults(self):
        q = self._build(lambda b: b.title())
        self.assertIn("title { romaji english native userPreferred }", q)

    def test_title_selective(self):
        q = self._build(lambda b: b.title("romaji", "english"))
        self.assertIn("title { romaji english }", q)

    def test_cover_image_defaults(self):
        q = self._build(lambda b: b.cover_image())
        self.assertIn("coverImage { extraLarge large color }", q)

    def test_cover_image_selective(self):
        q = self._build(lambda b: b.cover_image("medium"))
        self.assertIn("coverImage { medium }", q)

    def test_start_date_defaults(self):
        q = self._build(lambda b: b.start_date())
        self.assertIn("startDate { year month day }", q)

    def test_start_date_selective(self):
        q = self._build(lambda b: b.start_date("year"))
        self.assertIn("startDate { year }", q)

    def test_end_date_defaults(self):
        q = self._build(lambda b: b.end_date())
        self.assertIn("endDate { year month day }", q)

    def test_trailer_defaults(self):
        q = self._build(lambda b: b.trailer())
        self.assertIn("trailer { id site thumbnail }", q)

    def test_trailer_selective(self):
        q = self._build(lambda b: b.trailer("site"))
        self.assertIn("trailer { site }", q)

    def test_next_airing_episode_defaults(self):
        q = self._build(lambda b: b.next_airing_episode())
        self.assertIn("nextAiringEpisode { airingAt timeUntilAiring episode }", q)

    def test_next_airing_episode_selective(self):
        q = self._build(lambda b: b.next_airing_episode("episode", "mediaId"))
        self.assertIn("nextAiringEpisode { episode mediaId }", q)

    def test_tags_defaults(self):
        q = self._build(lambda b: b.tags())
        self.assertIn("tags {", q)
        self.assertIn("id", q)
        self.assertIn("name", q)

    def test_tags_selective(self):
        q = self._build(lambda b: b.tags("id", "name", "rank"))
        self.assertIn("tags { id name rank }", q)

    def test_external_links_defaults(self):
        q = self._build(lambda b: b.external_links())
        self.assertIn("externalLinks {", q)

    def test_external_links_selective(self):
        q = self._build(lambda b: b.external_links("url", "site"))
        self.assertIn("externalLinks { url site }", q)

    def test_streaming_episodes_defaults(self):
        q = self._build(lambda b: b.streaming_episodes())
        self.assertIn("streamingEpisodes { title thumbnail url site }", q)

    def test_rankings_defaults(self):
        q = self._build(lambda b: b.rankings())
        self.assertIn("rankings {", q)

    def test_rankings_selective(self):
        q = self._build(lambda b: b.rankings("rank", "type"))
        self.assertIn("rankings { rank type }", q)

    def test_media_list_entry_defaults(self):
        q = self._build(lambda b: b.media_list_entry())
        self.assertIn("mediaListEntry { id status score }", q)

    def test_media_list_entry_selective(self):
        q = self._build(lambda b: b.media_list_entry("progress", "score"))
        self.assertIn("mediaListEntry { progress score }", q)

    def test_stats(self):
        q = self._build(lambda b: b.stats())
        self.assertIn("stats {", q)
        self.assertIn("statusDistribution", q)
        self.assertIn("scoreDistribution", q)


# ============================================================
# MediaBuilder — Connection fields
# ============================================================

class TestMediaConnectionFields(unittest.TestCase):
    def _build(self, fn):
        b = _make_builder(MediaBuilder, "Media", {"id": 1})
        fn(b)
        query, _ = b._compile()
        return query

    def test_characters_with_args(self):
        q = self._build(lambda b: b.characters(
            sort=["FAVOURITES_DESC"], role="MAIN", page=1, per_page=5,
            fields=lambda c: c.name("full").image("large")
        ))
        self.assertIn("characters(", q)
        self.assertIn("sort: [FAVOURITES_DESC]", q)
        self.assertIn("role: MAIN", q)
        self.assertIn("name { full }", q)
        self.assertIn("image { large }", q)

    def test_characters_without_fields(self):
        q = self._build(lambda b: b.characters())
        self.assertIn("characters", q)

    def test_staff_connection(self):
        q = self._build(lambda b: b.staff(
            sort=["FAVOURITES_DESC"], page=1, per_page=3,
            fields=lambda s: s.name("full")
        ))
        self.assertIn("staff(", q)
        self.assertIn("name { full }", q)

    def test_studios_connection(self):
        q = self._build(lambda b: b.studios(
            sort=["NAME"], is_main=True,
            fields=lambda s: s.name()
        ))
        self.assertIn("studios(", q)
        self.assertIn("isMain: true", q)
        self.assertIn("name", q)

    def test_relations_default(self):
        q = self._build(lambda b: b.relations())
        self.assertIn("relations {", q)
        self.assertIn("relationType(version: 2)", q)

    def test_relations_custom(self):
        q = self._build(lambda b: b.relations(fields=lambda m: m.title("romaji").genres()))
        self.assertIn("relations {", q)
        self.assertIn("title { romaji }", q)
        self.assertIn("genres", q)

    def test_reviews(self):
        q = self._build(lambda b: b.reviews(limit=5, sort=["RATING_DESC"], page=1, per_page=3))
        self.assertIn("reviews(", q)
        self.assertIn("limit: 5", q)
        self.assertIn("sort: [RATING_DESC]", q)

    def test_reviews_no_args(self):
        q = self._build(lambda b: b.reviews())
        self.assertIn("reviews", q)
        self.assertIn("nodes", q)

    def test_recommendations(self):
        q = self._build(lambda b: b.recommendations(sort=["RATING_DESC"], page=1, per_page=5))
        self.assertIn("recommendations(", q)
        self.assertIn("sort: [RATING_DESC]", q)
        self.assertIn("mediaRecommendation", q)

    def test_recommendations_no_args(self):
        q = self._build(lambda b: b.recommendations())
        self.assertIn("recommendations", q)

    def test_airing_schedule(self):
        q = self._build(lambda b: b.airing_schedule(not_yet_aired=True, page=1, per_page=10))
        self.assertIn("airingSchedule(", q)
        self.assertIn("notYetAired: true", q)

    def test_airing_schedule_no_args(self):
        q = self._build(lambda b: b.airing_schedule())
        self.assertIn("airingSchedule", q)

    def test_trends(self):
        q = self._build(lambda b: b.trends(sort=["TRENDING_DESC"], releasing=True, page=1, per_page=5))
        self.assertIn("trends(", q)
        self.assertIn("sort: [TRENDING_DESC]", q)
        self.assertIn("releasing: true", q)

    def test_trends_no_args(self):
        q = self._build(lambda b: b.trends())
        self.assertIn("trends", q)


# ============================================================
# MediaBuilder — Compile & Paginate
# ============================================================

class TestMediaBuilderCompile(unittest.TestCase):
    def test_simple_fields(self):
        b = _make_builder(MediaBuilder, "Media", {"id": 13601})
        b.title("romaji", "english").genres().episodes()
        query, variables = b._compile()

        self.assertIn("Media(id: $id)", query)
        self.assertIn("title { romaji english }", query)
        self.assertIn("genres", query)
        self.assertIn("episodes", query)
        self.assertEqual(variables, {"id": 13601})

    def test_paginated_query(self):
        b = _make_builder(MediaBuilder, "Media", {"search": "Psycho-Pass", "type": "ANIME"})
        b.title("romaji").average_score().page(1, per_page=10)
        query, variables = b._compile()

        self.assertIn("Page(page: $page, perPage: $perPage)", query)
        self.assertIn("media(", query)
        self.assertIn("pageInfo", query)
        self.assertIn("averageScore", query)
        self.assertEqual(variables["page"], 1)
        self.assertEqual(variables["perPage"], 10)
        self.assertEqual(variables["search"], "Psycho-Pass")

    def test_nested_characters(self):
        b = _make_builder(MediaBuilder, "Media", {"id": 13601})
        b.title("romaji").characters(
            per_page=5, sort=["FAVOURITES_DESC"],
            fields=lambda c: c.name("full").image("large")
        )
        query, _ = b._compile()

        self.assertIn("characters(sort: [FAVOURITES_DESC], perPage: 5)", query)
        self.assertIn("name { full }", query)
        self.assertIn("image { large }", query)

    def test_no_fields_defaults_to_id(self):
        b = _make_builder(MediaBuilder, "Media", {"id": 1})
        query, _ = b._compile()
        self.assertIn("id", query)

    def test_no_args_no_variables(self):
        b = _make_builder(MediaBuilder, "Media", {})
        b.id()
        query, variables = b._compile()
        self.assertEqual(variables, {})
        self.assertIn("Media", query)
        # No variable declarations
        self.assertNotIn("$", query)

    def test_chaining_returns_self(self):
        b = _make_builder(MediaBuilder, "Media", {"id": 1})
        result = b.id().title("romaji").genres().episodes()
        self.assertIs(result, b)


# ============================================================
# CharacterBuilder
# ============================================================

class TestCharacterBuilderFields(unittest.TestCase):
    def _build(self, fn):
        b = _make_builder(CharacterBuilder, "Character", {"id": 5})
        fn(b)
        query, _ = b._compile()
        return query

    def test_id(self):
        self.assertIn("id", self._build(lambda b: b.id()))

    def test_description(self):
        self.assertIn("description", self._build(lambda b: b.description()))

    def test_description_as_html(self):
        self.assertIn("description(asHtml: true)", self._build(lambda b: b.description(as_html=True)))

    def test_gender(self):
        self.assertIn("gender", self._build(lambda b: b.gender()))

    def test_age(self):
        self.assertIn("age", self._build(lambda b: b.age()))

    def test_blood_type(self):
        self.assertIn("bloodType", self._build(lambda b: b.blood_type()))

    def test_is_favourite(self):
        self.assertIn("isFavourite", self._build(lambda b: b.is_favourite()))

    def test_is_favourite_blocked(self):
        self.assertIn("isFavouriteBlocked", self._build(lambda b: b.is_favourite_blocked()))

    def test_site_url(self):
        self.assertIn("siteUrl", self._build(lambda b: b.site_url()))

    def test_favourites(self):
        self.assertIn("favourites", self._build(lambda b: b.favourites()))

    def test_mod_notes(self):
        self.assertIn("modNotes", self._build(lambda b: b.mod_notes()))

    def test_name_defaults(self):
        q = self._build(lambda b: b.name())
        self.assertIn("name {", q)
        self.assertIn("full", q)
        self.assertIn("native", q)

    def test_name_selective(self):
        q = self._build(lambda b: b.name("full", "native"))
        self.assertIn("name { full native }", q)

    def test_image_defaults(self):
        q = self._build(lambda b: b.image())
        self.assertIn("image { large }", q)

    def test_image_selective(self):
        q = self._build(lambda b: b.image("large", "medium"))
        self.assertIn("image { large medium }", q)

    def test_date_of_birth_defaults(self):
        q = self._build(lambda b: b.date_of_birth())
        self.assertIn("dateOfBirth { year month day }", q)

    def test_date_of_birth_selective(self):
        q = self._build(lambda b: b.date_of_birth("year"))
        self.assertIn("dateOfBirth { year }", q)

    def test_media_connection(self):
        q = self._build(lambda b: b.media(
            sort=["POPULARITY_DESC"], type="ANIME", on_list=True, page=1, per_page=5,
            fields=lambda m: m.title("romaji")
        ))
        self.assertIn("media(", q)
        self.assertIn("title { romaji }", q)

    def test_character_compile(self):
        b = _make_builder(CharacterBuilder, "Character", {"id": 5})
        b.name("full", "native").media(fields=lambda m: m.title("romaji"))
        query, variables = b._compile()

        self.assertIn("Character(id: $id)", query)
        self.assertIn("name { full native }", query)
        self.assertIn("title { romaji }", query)
        self.assertEqual(variables, {"id": 5})


# ============================================================
# StaffBuilder
# ============================================================

class TestStaffBuilderFields(unittest.TestCase):
    def _build(self, fn):
        b = _make_builder(StaffBuilder, "Staff", {"id": 100})
        fn(b)
        query, _ = b._compile()
        return query

    def test_id(self):
        self.assertIn("id", self._build(lambda b: b.id()))

    def test_language_v2(self):
        self.assertIn("languageV2", self._build(lambda b: b.language_v2()))

    def test_language_alias(self):
        self.assertIn("languageV2", self._build(lambda b: b.language()))

    def test_description(self):
        self.assertIn("description", self._build(lambda b: b.description()))

    def test_description_as_html(self):
        self.assertIn("description(asHtml: true)", self._build(lambda b: b.description(as_html=True)))

    def test_primary_occupations(self):
        self.assertIn("primaryOccupations", self._build(lambda b: b.primary_occupations()))

    def test_gender(self):
        self.assertIn("gender", self._build(lambda b: b.gender()))

    def test_age(self):
        self.assertIn("age", self._build(lambda b: b.age()))

    def test_years_active(self):
        self.assertIn("yearsActive", self._build(lambda b: b.years_active()))

    def test_home_town(self):
        self.assertIn("homeTown", self._build(lambda b: b.home_town()))

    def test_blood_type(self):
        self.assertIn("bloodType", self._build(lambda b: b.blood_type()))

    def test_is_favourite(self):
        self.assertIn("isFavourite", self._build(lambda b: b.is_favourite()))

    def test_is_favourite_blocked(self):
        self.assertIn("isFavouriteBlocked", self._build(lambda b: b.is_favourite_blocked()))

    def test_site_url(self):
        self.assertIn("siteUrl", self._build(lambda b: b.site_url()))

    def test_favourites(self):
        self.assertIn("favourites", self._build(lambda b: b.favourites()))

    def test_submission_status(self):
        self.assertIn("submissionStatus", self._build(lambda b: b.submission_status()))

    def test_submission_notes(self):
        self.assertIn("submissionNotes", self._build(lambda b: b.submission_notes()))

    def test_mod_notes(self):
        self.assertIn("modNotes", self._build(lambda b: b.mod_notes()))

    def test_name_defaults(self):
        q = self._build(lambda b: b.name())
        self.assertIn("name {", q)

    def test_name_selective(self):
        q = self._build(lambda b: b.name("full"))
        self.assertIn("name { full }", q)

    def test_image_defaults(self):
        q = self._build(lambda b: b.image())
        self.assertIn("image { large }", q)

    def test_image_selective(self):
        q = self._build(lambda b: b.image("large", "medium"))
        self.assertIn("image { large medium }", q)

    def test_date_of_birth(self):
        q = self._build(lambda b: b.date_of_birth())
        self.assertIn("dateOfBirth { year month day }", q)

    def test_date_of_birth_selective(self):
        q = self._build(lambda b: b.date_of_birth("month"))
        self.assertIn("dateOfBirth { month }", q)

    def test_date_of_death(self):
        q = self._build(lambda b: b.date_of_death())
        self.assertIn("dateOfDeath { year month day }", q)

    def test_date_of_death_selective(self):
        q = self._build(lambda b: b.date_of_death("year", "month"))
        self.assertIn("dateOfDeath { year month }", q)

    def test_staff_media_connection(self):
        q = self._build(lambda b: b.staff_media(
            sort=["POPULARITY_DESC"], type="ANIME", on_list=True, page=1, per_page=5,
            fields=lambda m: m.title("romaji")
        ))
        self.assertIn("staffMedia(", q)
        self.assertIn("title { romaji }", q)

    def test_characters_connection(self):
        q = self._build(lambda b: b.characters(
            sort=["FAVOURITES_DESC"], page=1, per_page=3,
            fields=lambda c: c.name("full")
        ))
        self.assertIn("characters(", q)
        self.assertIn("name { full }", q)

    def test_character_media_connection(self):
        q = self._build(lambda b: b.character_media(
            sort=["POPULARITY_DESC"], on_list=False, page=1, per_page=5,
            fields=lambda m: m.title("romaji")
        ))
        self.assertIn("characterMedia(", q)
        self.assertIn("title { romaji }", q)

    def test_media_alias_delegates(self):
        """Staff.media() should delegate to staff_media()."""
        b = _make_builder(StaffBuilder, "Staff", {"id": 100})
        b.media(fields=lambda m: m.title("romaji"))
        query, _ = b._compile()
        self.assertIn("staffMedia", query)

    def test_staff_compile(self):
        b = _make_builder(StaffBuilder, "Staff", {"id": 113803})
        b.name("full").primary_occupations()
        query, variables = b._compile()

        self.assertIn("Staff(id: $id)", query)
        self.assertIn("name { full }", query)
        self.assertIn("primaryOccupations", query)


# ============================================================
# StudioBuilder
# ============================================================

class TestStudioBuilderFields(unittest.TestCase):
    def _build(self, fn):
        b = _make_builder(StudioBuilder, "Studio", {"id": 7})
        fn(b)
        query, _ = b._compile()
        return query

    def test_id(self):
        self.assertIn("id", self._build(lambda b: b.id()))

    def test_name(self):
        self.assertIn("name", self._build(lambda b: b.name()))

    def test_is_animation_studio(self):
        self.assertIn("isAnimationStudio", self._build(lambda b: b.is_animation_studio()))

    def test_site_url(self):
        self.assertIn("siteUrl", self._build(lambda b: b.site_url()))

    def test_is_favourite(self):
        self.assertIn("isFavourite", self._build(lambda b: b.is_favourite()))

    def test_favourites(self):
        self.assertIn("favourites", self._build(lambda b: b.favourites()))

    def test_media_connection(self):
        q = self._build(lambda b: b.media(
            sort=["NAME"], is_main=True, on_list=False, page=1, per_page=5,
            fields=lambda m: m.title("romaji")
        ))
        self.assertIn("media(", q)
        self.assertIn("isMain: true", q)
        self.assertIn("title { romaji }", q)

    def test_media_connection_no_args(self):
        q = self._build(lambda b: b.media())
        self.assertIn("media", q)

    def test_studio_compile(self):
        b = _make_builder(StudioBuilder, "Studio", {"id": 7})
        b.name().media(fields=lambda m: m.title("romaji"))
        query, variables = b._compile()

        self.assertIn("Studio(id: $id)", query)
        self.assertIn("name", query)
        self.assertIn("title { romaji }", query)


# ============================================================
# Fragment composition
# ============================================================

class TestFragmentComposition(unittest.TestCase):
    def test_media_fragment(self):
        basic = Fragment.media(lambda m: m.title("romaji", "english").genres().average_score())
        b = _make_builder(MediaBuilder, "Media", {"id": 13601})
        b.use(basic).episodes()
        query, _ = b._compile()

        self.assertIn("episodes", query)
        self.assertIn("title { romaji english }", query)
        self.assertIn("genres", query)
        self.assertIn("averageScore", query)

    def test_character_fragment(self):
        frag = Fragment.character(lambda c: c.name("full").image("large"))
        b = _make_builder(CharacterBuilder, "Character", {"id": 5})
        b.use(frag).age()
        query, _ = b._compile()

        self.assertIn("name { full }", query)
        self.assertIn("image { large }", query)
        self.assertIn("age", query)

    def test_staff_fragment(self):
        frag = Fragment.staff(lambda s: s.name("full").primary_occupations())
        b = _make_builder(StaffBuilder, "Staff", {"id": 100})
        b.use(frag).gender()
        query, _ = b._compile()

        self.assertIn("name { full }", query)
        self.assertIn("primaryOccupations", query)
        self.assertIn("gender", query)

    def test_studio_fragment(self):
        frag = Fragment.studio(lambda s: s.name().favourites())
        b = _make_builder(StudioBuilder, "Studio", {"id": 7})
        b.use(frag).is_animation_studio()
        query, _ = b._compile()

        self.assertIn("name", query)
        self.assertIn("favourites", query)
        self.assertIn("isAnimationStudio", query)

    def test_multiple_fragments(self):
        frag1 = Fragment.media(lambda m: m.title("romaji"))
        frag2 = Fragment.media(lambda m: m.genres().average_score())
        b = _make_builder(MediaBuilder, "Media", {"id": 1})
        b.use(frag1, frag2).episodes()
        query, _ = b._compile()

        self.assertIn("title { romaji }", query)
        self.assertIn("genres", query)
        self.assertIn("averageScore", query)
        self.assertIn("episodes", query)


# ============================================================
# PageBuilder
# ============================================================

class TestPageBuilder(unittest.TestCase):
    def test_page_builder_delegates(self):
        inner = _make_builder(MediaBuilder, "Media", {"search": "test"})
        inner.title("romaji")
        pb = PageBuilder(inner, page=2, per_page=25)
        query, variables = inner._compile()

        self.assertIn("Page(page: $page, perPage: $perPage)", query)
        self.assertEqual(variables["page"], 2)
        self.assertEqual(variables["perPage"], 25)

    def test_page_default_values(self):
        inner = _make_builder(MediaBuilder, "Media", {})
        inner.id()
        pb = PageBuilder(inner)
        query, variables = inner._compile()

        self.assertEqual(variables["page"], 1)
        self.assertEqual(variables["perPage"], 10)


# ============================================================
# Base builder utilities
# ============================================================

class TestFormatArgValue(unittest.TestCase):
    def test_bool_true(self):
        self.assertEqual(_format_arg_value(True), "true")

    def test_bool_false(self):
        self.assertEqual(_format_arg_value(False), "false")

    def test_int(self):
        self.assertEqual(_format_arg_value(42), "42")

    def test_string_quoted(self):
        self.assertEqual(_format_arg_value("hello"), '"hello"')

    def test_enum_unquoted(self):
        self.assertEqual(_format_arg_value("ANIME"), "ANIME")

    def test_list(self):
        self.assertEqual(_format_arg_value(["POPULARITY_DESC"]), "[POPULARITY_DESC]")

    def test_list_ints(self):
        self.assertEqual(_format_arg_value([1, 2]), "[1, 2]")

    def test_other_type(self):
        self.assertEqual(_format_arg_value(3.14), "3.14")


class TestInferType(unittest.TestCase):
    def test_known_key(self):
        self.assertEqual(_infer_type("id", 1), "Int")
        self.assertEqual(_infer_type("search", "test"), "String")
        self.assertEqual(_infer_type("type", "ANIME"), "MediaType")
        self.assertEqual(_infer_type("isAdult", True), "Boolean")

    def test_sort_media(self):
        self.assertEqual(_infer_type("sort", ["ID"], "Media"), "[MediaSort]")

    def test_sort_character(self):
        self.assertEqual(_infer_type("sort", ["ID"], "Character"), "[CharacterSort]")

    def test_sort_staff(self):
        self.assertEqual(_infer_type("sort", ["ID"], "Staff"), "[StaffSort]")

    def test_sort_studio(self):
        self.assertEqual(_infer_type("sort", ["ID"], "Studio"), "[StudioSort]")

    def test_sort_unknown_entity(self):
        self.assertEqual(_infer_type("sort", ["ID"], "Unknown"), "[MediaSort]")

    def test_fallback_bool(self):
        self.assertEqual(_infer_type("unknownBool", True), "Boolean")

    def test_fallback_int(self):
        self.assertEqual(_infer_type("unknownInt", 5), "Int")

    def test_fallback_float(self):
        self.assertEqual(_infer_type("unknownFloat", 1.5), "Float")

    def test_fallback_string(self):
        self.assertEqual(_infer_type("unknownStr", "val"), "String")

    def test_fallback_list_int(self):
        self.assertEqual(_infer_type("unknownList", [1, 2]), "[Int]")

    def test_fallback_list_str(self):
        self.assertEqual(_infer_type("unknownList", ["a"]), "[String]")

    def test_fallback_empty_list(self):
        self.assertEqual(_infer_type("unknownList", []), "[String]")


class TestRootToCollection(unittest.TestCase):
    def test_media(self):
        self.assertEqual(_root_to_collection("Media"), "media")

    def test_character(self):
        self.assertEqual(_root_to_collection("Character"), "characters")

    def test_staff(self):
        self.assertEqual(_root_to_collection("Staff"), "staff")

    def test_studio(self):
        self.assertEqual(_root_to_collection("Studio"), "studios")

    def test_unknown(self):
        self.assertEqual(_root_to_collection("Foo"), "foo")


# ============================================================
# RetryStrategy
# ============================================================

class TestRetryStrategy(unittest.TestCase):
    def test_default_strategy(self):
        s = RetryStrategy()
        self.assertEqual(s.max_retries, 3)
        self.assertEqual(s.on_rate_limit, "wait")
        self.assertEqual(s.on_server_error, "backoff")
        self.assertEqual(s.on_connection_error, "backoff")
        self.assertEqual(s.max_wait, 60)
        self.assertEqual(s.backoff_base, 1)

    def test_raise_rate_limit(self):
        s = RetryStrategy(on_rate_limit="raise")
        self.assertFalse(s.handle_rate_limit(60, 0))

    def test_raise_server_error(self):
        s = RetryStrategy(on_server_error="raise")
        self.assertFalse(s.handle_server_error(500, 0))

    def test_raise_connection_error(self):
        s = RetryStrategy(on_connection_error="raise")
        self.assertFalse(s.handle_connection_error(Exception(), 0))

    def test_max_retries_exceeded(self):
        s = RetryStrategy(max_retries=2)
        self.assertFalse(s.handle_rate_limit(60, 2))
        self.assertFalse(s.handle_server_error(500, 2))
        self.assertFalse(s.handle_connection_error(Exception(), 2))

    @patch("Anisearch.retry.time.sleep")
    def test_wait_rate_limit(self, mock_sleep):
        s = RetryStrategy(on_rate_limit="wait", max_wait=30)
        result = s.handle_rate_limit(10, 0)
        self.assertTrue(result)
        mock_sleep.assert_called_once_with(10)

    @patch("Anisearch.retry.time.sleep")
    def test_wait_rate_limit_capped(self, mock_sleep):
        s = RetryStrategy(on_rate_limit="wait", max_wait=5)
        result = s.handle_rate_limit(60, 0)
        self.assertTrue(result)
        mock_sleep.assert_called_once_with(5)

    @patch("Anisearch.retry.time.sleep")
    def test_backoff_server_error(self, mock_sleep):
        s = RetryStrategy(on_server_error="backoff", max_retries=3)
        result = s.handle_server_error(500, 0)
        self.assertTrue(result)
        mock_sleep.assert_called_once()

    @patch("Anisearch.retry.time.sleep")
    def test_backoff_connection_error(self, mock_sleep):
        s = RetryStrategy(on_connection_error="backoff", max_retries=3)
        result = s.handle_connection_error(Exception("timeout"), 0)
        self.assertTrue(result)
        mock_sleep.assert_called_once()

    def test_callable_rate_limit(self):
        handler = MagicMock(return_value=True)
        s = RetryStrategy(on_rate_limit=handler)
        result = s.handle_rate_limit(60, 0)
        self.assertTrue(result)
        handler.assert_called_once_with({"retry_after": 60}, 0)

    def test_callable_server_error(self):
        handler = MagicMock(return_value=False)
        s = RetryStrategy(on_server_error=handler)
        result = s.handle_server_error(503, 1)
        self.assertFalse(result)
        handler.assert_called_once_with({"status_code": 503}, 1)

    def test_callable_connection_error(self):
        err = Exception("network")
        handler = MagicMock(return_value=True)
        s = RetryStrategy(on_connection_error=handler)
        result = s.handle_connection_error(err, 0)
        self.assertTrue(result)
        handler.assert_called_once_with({"error": err}, 0)

    def test_none_retry_disables(self):
        anilist = Anilist(retry=None)
        self.assertIsNone(anilist._retry)


# ============================================================
# Error classes
# ============================================================

class TestErrors(unittest.TestCase):
    def test_anilist_error_is_exception(self):
        with self.assertRaises(Exception):
            raise AnilistError("test")

    def test_rate_limit_error(self):
        e = RateLimitError(30)
        self.assertEqual(e.retry_after, 30)
        self.assertIn("30", str(e))
        self.assertIsInstance(e, AnilistError)

    def test_rate_limit_error_default(self):
        e = RateLimitError()
        self.assertEqual(e.retry_after, 60)

    def test_server_error(self):
        e = ServerError(502, "Bad Gateway")
        self.assertEqual(e.status_code, 502)
        self.assertEqual(e.body, "Bad Gateway")
        self.assertIn("502", str(e))
        self.assertIsInstance(e, AnilistError)

    def test_graphql_error(self):
        errors = [{"message": "Not Found"}, {"message": "Invalid query"}]
        e = GraphQLError(errors)
        self.assertEqual(e.errors, errors)
        self.assertIn("Not Found", str(e))
        self.assertIn("Invalid query", str(e))
        self.assertIsInstance(e, AnilistError)

    def test_connection_error(self):
        original = OSError("Connection refused")
        e = AnilistConnectionError(original)
        self.assertEqual(e.original, original)
        self.assertIn("Connection refused", str(e))
        self.assertIsInstance(e, AnilistError)


# ============================================================
# Anilist builder API
# ============================================================

class TestAnilistBuilderAPI(unittest.TestCase):
    def test_media_returns_builder(self):
        anilist = Anilist()
        builder = anilist.media(id=13601)
        self.assertIsInstance(builder, MediaBuilder)

    def test_character_returns_builder(self):
        anilist = Anilist()
        builder = anilist.character(id=5)
        self.assertIsInstance(builder, CharacterBuilder)

    def test_staff_returns_builder(self):
        anilist = Anilist()
        builder = anilist.staff(id=113803)
        self.assertIsInstance(builder, StaffBuilder)

    def test_studio_returns_builder(self):
        anilist = Anilist()
        builder = anilist.studio(id=7)
        self.assertIsInstance(builder, StudioBuilder)

    def test_media_kwargs_passed(self):
        anilist = Anilist()
        builder = anilist.media(id=1, type="ANIME")
        _, variables = builder._compile()
        self.assertEqual(variables["id"], 1)
        self.assertEqual(variables["type"], "ANIME")

    def test_version_importable(self):
        import Anisearch
        self.assertIsInstance(Anisearch.__version__, str)


# ============================================================
# Execute / execute_async without real connection
# ============================================================

class TestExecute(unittest.TestCase):
    def test_execute_calls_request_fn(self):
        mock_request = MagicMock(return_value={"data": {"Media": {"id": 1}}})
        b = MediaBuilder(mock_request, None, "Media", {"id": 1})
        b.id()
        result = b.execute()

        mock_request.assert_called_once()
        args = mock_request.call_args
        self.assertIn("Media(id: $id)", args[0][1])
        self.assertEqual(args[0][0], {"id": 1})
        self.assertIsInstance(result, Media)
        self.assertEqual(result.id, 1)

    def test_execute_async_raises_without_connection(self):
        b = MediaBuilder(None, None, "Media", {"id": 1})
        b.id()
        import asyncio
        with self.assertRaises(RuntimeError):
            asyncio.run(b.execute_async())

    def test_execute_async_calls_async_request_fn(self):
        import asyncio

        async def mock_async_request(variables, query, **kwargs):
            return {"data": {"Media": {"id": 1}}}

        b = MediaBuilder(None, lambda: mock_async_request, "Media", {"id": 1})
        b._async_request = lambda: mock_async_request

        # Test via Anilist to get proper async wiring
        mock_request = MagicMock(return_value={"data": {"Media": {"id": 1}}})
        b = MediaBuilder(mock_request, lambda: mock_async_request, "Media", {"id": 1})
        b.id()
        result = b.execute()
        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
