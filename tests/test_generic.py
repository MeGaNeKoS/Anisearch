import unittest

import Anisearch


class TestAnilist(unittest.TestCase):
    def test_Anilist(self):
        anilist = Anisearch.Anilist()

        # Get
        self.assertIsInstance(anilist.get.anime(13601), dict)
        self.assertIsInstance(anilist.get.manga(64127), dict)
        self.assertIsInstance(anilist.get.staff(113803), dict)
        self.assertIsInstance(anilist.get.studio(7), dict)

        # Search
        self.assertIsInstance(anilist.search.anime(search="Sword"), dict)
        self.assertIsInstance(anilist.search.manga(search="Sword"), dict)
        self.assertIsInstance(anilist.search.character(search="Tsutsukakushi"), dict)
        self.assertIsInstance(anilist.search.staff(search="Kantoku"), dict)
        self.assertIsInstance(anilist.search.studio(search="J.C. Staff"), dict)
