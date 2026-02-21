import unittest

import Anisearch
from Anisearch.models import Media, Staff, Studio, Character, PageResult


class TestAnilist(unittest.TestCase):
    def test_Anilist(self):
        anilist = Anisearch.Anilist()

        # Get by ID
        self.assertIsInstance(anilist.media(id=13601, type="ANIME").title().genres().episodes().execute(), Media)
        self.assertIsInstance(anilist.media(id=64127, type="MANGA").title().genres().chapters().execute(), Media)
        self.assertIsInstance(anilist.staff(id=113803).name("full").primary_occupations().execute(), Staff)
        self.assertIsInstance(anilist.studio(id=7).name().media(fields=lambda m: m.title("romaji")).execute(), Studio)

        # Search
        self.assertIsInstance(anilist.media(search="Sword", type="ANIME").title().page(1, per_page=10).execute(), PageResult)
        self.assertIsInstance(anilist.media(search="Sword", type="MANGA").title().page(1, per_page=10).execute(), PageResult)
        self.assertIsInstance(anilist.character(search="Tsutsukakushi").name("full").page(1, per_page=10).execute(), PageResult)
        self.assertIsInstance(anilist.staff(search="Kantoku").name("full").page(1, per_page=10).execute(), PageResult)
        self.assertIsInstance(anilist.studio(search="J.C. Staff").name().page(1, per_page=10).execute(), PageResult)
