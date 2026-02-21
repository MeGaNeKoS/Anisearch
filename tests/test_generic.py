import unittest

import Anisearch


class TestAnilist(unittest.TestCase):
    def test_Anilist(self):
        anilist = Anisearch.Anilist()

        # Get by ID
        self.assertIsInstance(anilist.media(id=13601, type="ANIME").title().genres().episodes().execute(), dict)
        self.assertIsInstance(anilist.media(id=64127, type="MANGA").title().genres().chapters().execute(), dict)
        self.assertIsInstance(anilist.staff(id=113803).name("full").primary_occupations().execute(), dict)
        self.assertIsInstance(anilist.studio(id=7).name().media(fields=lambda m: m.title("romaji")).execute(), dict)

        # Search
        self.assertIsInstance(anilist.media(search="Sword", type="ANIME").title().page(1, per_page=10).execute(), dict)
        self.assertIsInstance(anilist.media(search="Sword", type="MANGA").title().page(1, per_page=10).execute(), dict)
        self.assertIsInstance(anilist.character(search="Tsutsukakushi").name("full").page(1, per_page=10).execute(), dict)
        self.assertIsInstance(anilist.staff(search="Kantoku").name("full").page(1, per_page=10).execute(), dict)
        self.assertIsInstance(anilist.studio(search="J.C. Staff").name().page(1, per_page=10).execute(), dict)
