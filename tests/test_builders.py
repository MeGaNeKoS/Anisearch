"""Unit tests for the declarative GraphQL builder system."""

import unittest

from Anisearch import Anilist, Fragment
from Anisearch.builders.media import MediaBuilder
from Anisearch.builders.character import CharacterBuilder
from Anisearch.builders.staff import StaffBuilder
from Anisearch.builders.studio import StudioBuilder
from Anisearch.retry import RetryStrategy


def _make_builder(cls, root_field, root_args=None):
    """Create a builder without a real connection for testing compilation."""
    return cls(None, None, root_field, root_args or {})


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

    def test_cover_image_defaults(self):
        b = _make_builder(MediaBuilder, "Media", {"id": 1})
        b.cover_image()
        query, _ = b._compile()
        self.assertIn("coverImage { extraLarge large color }", query)

    def test_status_with_version(self):
        b = _make_builder(MediaBuilder, "Media", {"id": 1})
        b.status()
        query, _ = b._compile()
        self.assertIn("status(version: 2)", query)


class TestCharacterBuilderCompile(unittest.TestCase):
    def test_character_fields(self):
        b = _make_builder(CharacterBuilder, "Character", {"id": 5})
        b.name("full", "native").media(fields=lambda m: m.title("romaji"))
        query, variables = b._compile()

        self.assertIn("Character(id: $id)", query)
        self.assertIn("name { full native }", query)
        self.assertIn("title { romaji }", query)
        self.assertEqual(variables, {"id": 5})


class TestStaffBuilderCompile(unittest.TestCase):
    def test_staff_fields(self):
        b = _make_builder(StaffBuilder, "Staff", {"id": 113803})
        b.name("full").primary_occupations()
        query, variables = b._compile()

        self.assertIn("Staff(id: $id)", query)
        self.assertIn("name { full }", query)
        self.assertIn("primaryOccupations", query)


class TestStudioBuilderCompile(unittest.TestCase):
    def test_studio_with_media(self):
        b = _make_builder(StudioBuilder, "Studio", {"id": 7})
        b.name().media(fields=lambda m: m.title("romaji"))
        query, variables = b._compile()

        self.assertIn("Studio(id: $id)", query)
        self.assertIn("name", query)
        self.assertIn("title { romaji }", query)


class TestFragmentComposition(unittest.TestCase):
    def test_fragment_merge(self):
        basic = Fragment.media(lambda m: m.title("romaji", "english").genres().average_score())
        b = _make_builder(MediaBuilder, "Media", {"id": 13601})
        b.use(basic).episodes()
        query, _ = b._compile()

        # episodes from direct call + title/genres/averageScore from fragment
        self.assertIn("episodes", query)
        self.assertIn("title { romaji english }", query)
        self.assertIn("genres", query)
        self.assertIn("averageScore", query)


class TestRetryStrategy(unittest.TestCase):
    def test_default_strategy(self):
        s = RetryStrategy()
        self.assertEqual(s.max_retries, 3)
        self.assertEqual(s.on_rate_limit, "wait")

    def test_raise_strategy(self):
        s = RetryStrategy(on_rate_limit="raise")
        # Should return False (don't retry)
        self.assertFalse(s.handle_rate_limit(60, 0))

    def test_max_retries_exceeded(self):
        s = RetryStrategy(max_retries=2)
        self.assertFalse(s.handle_rate_limit(60, 2))
        self.assertFalse(s.handle_server_error(500, 2))
        self.assertFalse(s.handle_connection_error(Exception(), 2))

    def test_none_retry_disables(self):
        # When retry=None, Anilist should not retry
        anilist = Anilist(retry=None)
        self.assertIsNone(anilist._retry)


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


if __name__ == "__main__":
    unittest.main()
