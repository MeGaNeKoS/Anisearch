"""Unit tests for typed response models."""

import unittest
from unittest.mock import MagicMock

from Anisearch.models import (
    Media, MediaTitle, MediaCoverImage, MediaTrailer, MediaTag,
    MediaExternalLink, MediaStreamingEpisode, MediaRank, MediaList, MediaStats,
    StatusDistribution, ScoreDistribution, ReviewNode, RecommendationNode,
    Character, CharacterName, CharacterImage,
    Staff, StaffName, StaffImage,
    Studio,
    FuzzyDate, PageInfo, PageResult,
    AiringScheduleNode, MediaTrendNode,
    CharacterEdge, StaffEdge, StudioEdge, MediaRelationEdge,
    DeleteResult, MediaListEntry, TextActivity, MessageActivity,
    ListActivity, ActivityReply, UserFollowResult, FavouritesResult,
    ReviewResult, RecommendationResult, ThreadResult, ThreadCommentResult,
    ToggleLikeResult, UserResult,
)
from Anisearch.builders.media import MediaBuilder
from Anisearch.builders.character import CharacterBuilder
from Anisearch.builders.staff import StaffBuilder
from Anisearch.builders.studio import StudioBuilder


# ============================================================
# Shared types
# ============================================================

class TestFuzzyDate(unittest.TestCase):
    def test_full(self):
        d = FuzzyDate.from_dict({"year": 2020, "month": 1, "day": 15})
        self.assertEqual(d.year, 2020)
        self.assertEqual(d.month, 1)
        self.assertEqual(d.day, 15)

    def test_partial(self):
        d = FuzzyDate.from_dict({"year": 2020})
        self.assertEqual(d.year, 2020)
        self.assertIsNone(d.month)

    def test_none(self):
        self.assertIsNone(FuzzyDate.from_dict(None))

    def test_non_dict(self):
        self.assertIsNone(FuzzyDate.from_dict("string"))


class TestPageInfo(unittest.TestCase):
    def test_full(self):
        p = PageInfo.from_dict({
            "total": 100, "perPage": 10, "currentPage": 1,
            "lastPage": 10, "hasNextPage": True,
        })
        self.assertEqual(p.total, 100)
        self.assertTrue(p.has_next_page)
        self.assertEqual(p.per_page, 10)

    def test_none(self):
        self.assertIsNone(PageInfo.from_dict(None))


class TestPageResult(unittest.TestCase):
    def test_media_page(self):
        data = {
            "pageInfo": {"total": 50, "hasNextPage": True},
            "media": [
                {"id": 1, "title": {"romaji": "Test"}},
                {"id": 2},
            ],
        }
        page = PageResult.from_dict(data, Media, "media")
        self.assertTrue(page.page_info.has_next_page)
        self.assertEqual(len(page.items), 2)
        self.assertIsInstance(page.items[0], Media)
        self.assertEqual(page.items[0].id, 1)
        self.assertEqual(page.items[0].title.romaji, "Test")

    def test_character_page(self):
        data = {
            "pageInfo": {"total": 5},
            "characters": [{"id": 10, "name": {"full": "Eren"}}],
        }
        page = PageResult.from_dict(data, Character, "characters")
        self.assertEqual(page.items[0].name.full, "Eren")

    def test_none(self):
        self.assertIsNone(PageResult.from_dict(None))


class TestAiringScheduleNode(unittest.TestCase):
    def test_full(self):
        n = AiringScheduleNode.from_dict({
            "id": 1, "airingAt": 123456, "timeUntilAiring": 100,
            "episode": 5, "mediaId": 42,
        })
        self.assertEqual(n.episode, 5)
        self.assertEqual(n.media_id, 42)

    def test_none(self):
        self.assertIsNone(AiringScheduleNode.from_dict(None))


class TestMediaTrendNode(unittest.TestCase):
    def test_full(self):
        n = MediaTrendNode.from_dict({
            "mediaId": 1, "trending": 50, "averageScore": 80,
            "popularity": 1000, "releasing": True, "episode": 3,
        })
        self.assertEqual(n.trending, 50)
        self.assertTrue(n.releasing)

    def test_none(self):
        self.assertIsNone(MediaTrendNode.from_dict(None))


# ============================================================
# Media types
# ============================================================

class TestMediaTitle(unittest.TestCase):
    def test_full(self):
        t = MediaTitle.from_dict({"romaji": "Shingeki", "english": "Attack on Titan", "native": "進撃", "userPreferred": "Shingeki"})
        self.assertEqual(t.romaji, "Shingeki")
        self.assertEqual(t.english, "Attack on Titan")
        self.assertEqual(t.user_preferred, "Shingeki")

    def test_partial(self):
        t = MediaTitle.from_dict({"romaji": "Shingeki"})
        self.assertIsNone(t.english)

    def test_none(self):
        self.assertIsNone(MediaTitle.from_dict(None))


class TestMediaCoverImage(unittest.TestCase):
    def test_full(self):
        c = MediaCoverImage.from_dict({"extraLarge": "url1", "large": "url2", "medium": "url3", "color": "#fff"})
        self.assertEqual(c.extra_large, "url1")
        self.assertEqual(c.color, "#fff")


class TestMediaTrailer(unittest.TestCase):
    def test_full(self):
        t = MediaTrailer.from_dict({"id": "abc", "site": "youtube", "thumbnail": "thumb"})
        self.assertEqual(t.site, "youtube")


class TestMediaTag(unittest.TestCase):
    def test_full(self):
        t = MediaTag.from_dict({"id": 1, "name": "Action", "rank": 90, "isAdult": False})
        self.assertEqual(t.name, "Action")
        self.assertEqual(t.rank, 90)
        self.assertFalse(t.is_adult)


class TestMediaExternalLink(unittest.TestCase):
    def test_full(self):
        e = MediaExternalLink.from_dict({"url": "https://example.com", "site": "Crunchyroll"})
        self.assertEqual(e.site, "Crunchyroll")


class TestMediaStreamingEpisode(unittest.TestCase):
    def test_full(self):
        s = MediaStreamingEpisode.from_dict({"title": "Ep 1", "url": "url", "site": "CR"})
        self.assertEqual(s.title, "Ep 1")


class TestMediaRank(unittest.TestCase):
    def test_full(self):
        r = MediaRank.from_dict({"id": 1, "rank": 5, "type": "RATED", "allTime": True})
        self.assertEqual(r.rank, 5)
        self.assertTrue(r.all_time)


class TestMediaList(unittest.TestCase):
    def test_full(self):
        m = MediaList.from_dict({"id": 1, "status": "WATCHING", "score": 8.5, "progress": 12})
        self.assertEqual(m.status, "WATCHING")
        self.assertEqual(m.score, 8.5)


class TestMediaStats(unittest.TestCase):
    def test_full(self):
        s = MediaStats.from_dict({
            "statusDistribution": [{"status": "WATCHING", "amount": 100}],
            "scoreDistribution": [{"score": 80, "amount": 50}],
        })
        self.assertEqual(len(s.status_distribution), 1)
        self.assertEqual(s.status_distribution[0].status, "WATCHING")
        self.assertEqual(s.score_distribution[0].score, 80)


class TestReviewNode(unittest.TestCase):
    def test_full(self):
        r = ReviewNode.from_dict({"id": 1, "summary": "Great", "rating": 90, "score": 9})
        self.assertEqual(r.summary, "Great")


class TestRecommendationNode(unittest.TestCase):
    def test_with_media(self):
        r = RecommendationNode.from_dict({
            "id": 1, "rating": 5,
            "mediaRecommendation": {"id": 42, "title": {"romaji": "Rec"}},
        })
        self.assertEqual(r.rating, 5)
        self.assertIsInstance(r.media_recommendation, Media)
        self.assertEqual(r.media_recommendation.id, 42)

    def test_without_media(self):
        r = RecommendationNode.from_dict({"id": 1, "rating": 3})
        self.assertIsNone(r.media_recommendation)


class TestMedia(unittest.TestCase):
    def test_full_media(self):
        data = {
            "id": 1, "idMal": 1, "type": "ANIME", "format": "TV",
            "status": "FINISHED", "episodes": 25, "averageScore": 84,
            "title": {"romaji": "Cowboy Bebop", "english": "Cowboy Bebop"},
            "coverImage": {"large": "url"},
            "startDate": {"year": 1998, "month": 4, "day": 3},
            "tags": [{"id": 1, "name": "Action"}],
            "genres": ["Action", "Sci-Fi"],
        }
        m = Media.from_dict(data)
        self.assertEqual(m.id, 1)
        self.assertEqual(m.type, "ANIME")
        self.assertEqual(m.episodes, 25)
        self.assertEqual(m.title.romaji, "Cowboy Bebop")
        self.assertEqual(m.title.english, "Cowboy Bebop")
        self.assertEqual(m.cover_image.large, "url")
        self.assertEqual(m.start_date.year, 1998)
        self.assertEqual(len(m.tags), 1)
        self.assertEqual(m.tags[0].name, "Action")
        self.assertEqual(m.genres, ["Action", "Sci-Fi"])

    def test_partial_media(self):
        m = Media.from_dict({"id": 1})
        self.assertEqual(m.id, 1)
        self.assertIsNone(m.title)
        self.assertIsNone(m.episodes)

    def test_none(self):
        self.assertIsNone(Media.from_dict(None))

    def test_with_characters(self):
        data = {
            "id": 1,
            "characters": {
                "edges": [
                    {"id": 10, "role": "MAIN", "node": {"id": 5, "name": {"full": "Spike"}}},
                ],
            },
        }
        m = Media.from_dict(data)
        self.assertEqual(len(m.characters), 1)
        self.assertIsInstance(m.characters[0], CharacterEdge)
        self.assertEqual(m.characters[0].role, "MAIN")
        self.assertEqual(m.characters[0].node.name.full, "Spike")

    def test_with_relations(self):
        data = {
            "id": 1,
            "relations": {
                "edges": [
                    {"id": 2, "relationType": "SEQUEL", "node": {"id": 3, "title": {"romaji": "Part 2"}}},
                ],
            },
        }
        m = Media.from_dict(data)
        self.assertEqual(m.relations[0].relation_type, "SEQUEL")
        self.assertIsInstance(m.relations[0].node, Media)

    def test_with_reviews_nodes(self):
        data = {
            "id": 1,
            "reviews": {"nodes": [{"id": 100, "summary": "Good"}]},
        }
        m = Media.from_dict(data)
        self.assertEqual(len(m.reviews), 1)
        self.assertEqual(m.reviews[0].summary, "Good")


# ============================================================
# Character types
# ============================================================

class TestCharacterName(unittest.TestCase):
    def test_full(self):
        n = CharacterName.from_dict({
            "first": "Eren", "middle": None, "last": "Yeager",
            "full": "Eren Yeager", "native": "エレン", "userPreferred": "Eren Yeager",
        })
        self.assertEqual(n.full, "Eren Yeager")
        self.assertEqual(n.user_preferred, "Eren Yeager")

    def test_none(self):
        self.assertIsNone(CharacterName.from_dict(None))


class TestCharacterImage(unittest.TestCase):
    def test_full(self):
        i = CharacterImage.from_dict({"large": "url1", "medium": "url2"})
        self.assertEqual(i.large, "url1")


class TestCharacter(unittest.TestCase):
    def test_full(self):
        data = {
            "id": 5, "gender": "Male", "age": "15",
            "name": {"full": "Eren Yeager"},
            "image": {"large": "url"},
            "dateOfBirth": {"year": 835, "month": 3, "day": 30},
        }
        c = Character.from_dict(data)
        self.assertEqual(c.id, 5)
        self.assertEqual(c.gender, "Male")
        self.assertEqual(c.name.full, "Eren Yeager")
        self.assertEqual(c.image.large, "url")
        self.assertEqual(c.date_of_birth.year, 835)

    def test_none(self):
        self.assertIsNone(Character.from_dict(None))


# ============================================================
# Staff types
# ============================================================

class TestStaffName(unittest.TestCase):
    def test_full(self):
        n = StaffName.from_dict({"full": "Hiroyuki Sawano", "native": "澤野弘之"})
        self.assertEqual(n.full, "Hiroyuki Sawano")


class TestStaffImage(unittest.TestCase):
    def test_full(self):
        i = StaffImage.from_dict({"large": "url"})
        self.assertEqual(i.large, "url")


class TestStaff(unittest.TestCase):
    def test_full(self):
        data = {
            "id": 100, "languageV2": "Japanese",
            "name": {"full": "Test Staff"},
            "primaryOccupations": ["Voice Actor"],
            "dateOfBirth": {"year": 1980},
        }
        s = Staff.from_dict(data)
        self.assertEqual(s.id, 100)
        self.assertEqual(s.language_v2, "Japanese")
        self.assertEqual(s.name.full, "Test Staff")
        self.assertEqual(s.primary_occupations, ["Voice Actor"])

    def test_none(self):
        self.assertIsNone(Staff.from_dict(None))


# ============================================================
# Studio types
# ============================================================

class TestStudio(unittest.TestCase):
    def test_full(self):
        s = Studio.from_dict({
            "id": 7, "name": "J.C.Staff",
            "isAnimationStudio": True, "siteUrl": "url",
        })
        self.assertEqual(s.name, "J.C.Staff")
        self.assertTrue(s.is_animation_studio)

    def test_none(self):
        self.assertIsNone(Studio.from_dict(None))


# ============================================================
# Connection/edge types
# ============================================================

class TestCharacterEdge(unittest.TestCase):
    def test_full(self):
        e = CharacterEdge.from_dict({
            "id": 1, "role": "MAIN",
            "node": {"id": 5, "name": {"full": "Eren"}},
        })
        self.assertEqual(e.role, "MAIN")
        self.assertIsInstance(e.node, Character)
        self.assertEqual(e.node.name.full, "Eren")


class TestStaffEdge(unittest.TestCase):
    def test_full(self):
        e = StaffEdge.from_dict({
            "id": 1, "role": "Director",
            "node": {"id": 100, "name": {"full": "Director Name"}},
        })
        self.assertEqual(e.role, "Director")
        self.assertIsInstance(e.node, Staff)


class TestStudioEdge(unittest.TestCase):
    def test_full(self):
        e = StudioEdge.from_dict({
            "isMain": True,
            "node": {"id": 7, "name": "MAPPA"},
        })
        self.assertTrue(e.is_main)
        self.assertIsInstance(e.node, Studio)


class TestMediaRelationEdge(unittest.TestCase):
    def test_full(self):
        e = MediaRelationEdge.from_dict({
            "id": 1, "relationType": "SEQUEL",
            "node": {"id": 2, "title": {"romaji": "Part 2"}},
        })
        self.assertEqual(e.relation_type, "SEQUEL")
        self.assertIsInstance(e.node, Media)


# ============================================================
# Mutation types
# ============================================================

class TestDeleteResult(unittest.TestCase):
    def test_full(self):
        d = DeleteResult.from_dict({"deleted": True})
        self.assertTrue(d.deleted)

    def test_none(self):
        self.assertIsNone(DeleteResult.from_dict(None))


class TestMediaListEntry(unittest.TestCase):
    def test_full(self):
        e = MediaListEntry.from_dict({
            "id": 1, "status": "WATCHING", "score": 8.0, "progress": 5,
            "startedAt": {"year": 2024, "month": 1},
        })
        self.assertEqual(e.status, "WATCHING")
        self.assertEqual(e.started_at.year, 2024)


class TestTextActivity(unittest.TestCase):
    def test_full(self):
        a = TextActivity.from_dict({"id": 1, "type": "TEXT", "text": "Hello"})
        self.assertEqual(a.text, "Hello")


class TestMessageActivity(unittest.TestCase):
    def test_full(self):
        a = MessageActivity.from_dict({"id": 1, "type": "MESSAGE", "message": "Hi", "recipientId": 5})
        self.assertEqual(a.recipient_id, 5)


class TestActivityReply(unittest.TestCase):
    def test_full(self):
        a = ActivityReply.from_dict({"id": 1, "text": "Reply", "activityId": 10})
        self.assertEqual(a.activity_id, 10)


class TestUserFollowResult(unittest.TestCase):
    def test_full(self):
        u = UserFollowResult.from_dict({"id": 1, "name": "user", "isFollowing": True})
        self.assertTrue(u.is_following)


class TestFavouritesResult(unittest.TestCase):
    def test_full(self):
        f = FavouritesResult.from_dict({"anime": {"nodes": [{"id": 1}]}})
        self.assertIsNotNone(f.anime)


class TestReviewResult(unittest.TestCase):
    def test_full(self):
        r = ReviewResult.from_dict({"id": 1, "summary": "Good", "body": "text", "score": 8})
        self.assertEqual(r.summary, "Good")


class TestRecommendationResultModel(unittest.TestCase):
    def test_full(self):
        r = RecommendationResult.from_dict({"id": 1, "rating": 5})
        self.assertEqual(r.rating, 5)


class TestThreadResult(unittest.TestCase):
    def test_full(self):
        t = ThreadResult.from_dict({"id": 1, "title": "Thread", "isSubscribed": True})
        self.assertTrue(t.is_subscribed)


class TestThreadCommentResult(unittest.TestCase):
    def test_full(self):
        t = ThreadCommentResult.from_dict({"id": 1, "comment": "text"})
        self.assertEqual(t.comment, "text")


class TestToggleLikeResult(unittest.TestCase):
    def test_full(self):
        t = ToggleLikeResult.from_dict({"id": 1, "type": "THREAD"})
        self.assertEqual(t.type, "THREAD")


class TestUserResult(unittest.TestCase):
    def test_full(self):
        u = UserResult.from_dict({"id": 1, "name": "TestUser"})
        self.assertEqual(u.name, "TestUser")


# ============================================================
# Builder execute → typed response integration
# ============================================================

class TestExecuteTypedResponse(unittest.TestCase):
    def test_media_execute_returns_media(self):
        raw = {"data": {"Media": {"id": 1, "title": {"romaji": "Test", "english": "Test EN"}, "episodes": 12}}}
        mock_request = MagicMock(return_value=raw)
        b = MediaBuilder(mock_request, None, "Media", {"id": 1})
        b.id().title("romaji", "english").episodes()
        result = b.execute()
        self.assertIsInstance(result, Media)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.title.romaji, "Test")
        self.assertEqual(result.episodes, 12)

    def test_character_execute_returns_character(self):
        raw = {"data": {"Character": {"id": 5, "name": {"full": "Eren"}}}}
        mock_request = MagicMock(return_value=raw)
        b = CharacterBuilder(mock_request, None, "Character", {"id": 5})
        b.id().name("full")
        result = b.execute()
        self.assertIsInstance(result, Character)
        self.assertEqual(result.name.full, "Eren")

    def test_staff_execute_returns_staff(self):
        raw = {"data": {"Staff": {"id": 100, "name": {"full": "Sawano"}}}}
        mock_request = MagicMock(return_value=raw)
        b = StaffBuilder(mock_request, None, "Staff", {"id": 100})
        b.id().name("full")
        result = b.execute()
        self.assertIsInstance(result, Staff)
        self.assertEqual(result.name.full, "Sawano")

    def test_studio_execute_returns_studio(self):
        raw = {"data": {"Studio": {"id": 7, "name": "MAPPA"}}}
        mock_request = MagicMock(return_value=raw)
        b = StudioBuilder(mock_request, None, "Studio", {"id": 7})
        b.id().name()
        result = b.execute()
        self.assertIsInstance(result, Studio)
        self.assertEqual(result.name, "MAPPA")

    def test_paginated_media_returns_page_result(self):
        raw = {"data": {"Page": {
            "pageInfo": {"total": 100, "hasNextPage": True, "currentPage": 1},
            "media": [{"id": 1, "title": {"romaji": "A"}}, {"id": 2}],
        }}}
        mock_request = MagicMock(return_value=raw)
        b = MediaBuilder(mock_request, None, "Media", {"type": "ANIME"})
        b.id().title("romaji").page(1, 10)
        result = b.execute()
        self.assertIsInstance(result, PageResult)
        self.assertTrue(result.page_info.has_next_page)
        self.assertEqual(len(result.items), 2)
        self.assertIsInstance(result.items[0], Media)
        self.assertEqual(result.items[0].title.romaji, "A")

    def test_mutation_execute_returns_typed(self):
        from Anisearch.builders.mutations import SaveMediaListEntryMutation
        raw = {"data": {"SaveMediaListEntry": {"id": 1, "status": "WATCHING"}}}
        mock_request = MagicMock(return_value=raw)
        b = SaveMediaListEntryMutation(mock_request, None, {"mediaId": 1, "status": "WATCHING"})
        result = b.execute()
        self.assertIsInstance(result, MediaListEntry)
        self.assertEqual(result.status, "WATCHING")

    def test_delete_mutation_returns_typed(self):
        from Anisearch.builders.mutations import DeleteMediaListEntryMutation
        raw = {"data": {"DeleteMediaListEntry": {"deleted": True}}}
        mock_request = MagicMock(return_value=raw)
        b = DeleteMediaListEntryMutation(mock_request, None, {"id": 1})
        result = b.execute()
        self.assertIsInstance(result, DeleteResult)
        self.assertTrue(result.deleted)


if __name__ == "__main__":
    unittest.main()
