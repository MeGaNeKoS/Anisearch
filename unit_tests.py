import Anisearch
import unittest


class TestAnilist(unittest.TestCase):
    def test_Anilist(self):
        anilist = Anisearch.Anilist()

        # Get
        self.assertIsInstance(anilist.get.anime(13601), dict)
        self.assertIsInstance(anilist.get.manga(64127), dict)
        self.assertIsInstance(anilist.get.staff(113803), dict)
        self.assertIsInstance(anilist.get.studio(7), dict)

        # Search

        self.assertIsInstance(anilist.search.anime("Sword"), dict)
        self.assertIsInstance(anilist.search.manga("Sword"), dict)
        self.assertIsInstance(anilist.search.character("Tsutsukakushi"), dict)
        self.assertIsInstance(anilist.search.staff("Kantoku"), dict)
        self.assertIsInstance(anilist.search.studio("J.C. Staff"), dict)
