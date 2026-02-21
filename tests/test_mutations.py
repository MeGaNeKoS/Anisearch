"""Tests for mutation builders and auth token support."""

import unittest
from unittest.mock import MagicMock, patch

from Anisearch import Anilist
from Anisearch.builders.base import BaseMutationBuilder
from Anisearch.builders.mutations import (
    SaveMediaListEntryMutation, UpdateMediaListEntriesMutation,
    DeleteMediaListEntryMutation, DeleteCustomListMutation,
    SaveTextActivityMutation, SaveMessageActivityMutation,
    SaveListActivityMutation, DeleteActivityMutation,
    SaveActivityReplyMutation, DeleteActivityReplyMutation,
    ToggleFollowMutation, ToggleFavouriteMutation,
    UpdateFavouriteOrderMutation, ToggleLikeMutation,
    SaveReviewMutation, DeleteReviewMutation, RateReviewMutation,
    SaveRecommendationMutation,
    SaveThreadMutation, DeleteThreadMutation,
    ToggleThreadSubscriptionMutation, SaveThreadCommentMutation,
    DeleteThreadCommentMutation,
    UpdateUserMutation, UpdateAniChartSettingsMutation,
    UpdateAniChartHighlightsMutation,
)


class TestBaseMutationBuilderCompile(unittest.TestCase):
    """Test that BaseMutationBuilder._compile() produces correct mutation syntax."""

    def test_compile_produces_mutation_keyword(self):
        m = SaveMediaListEntryMutation(None, None, {"mediaId": 1, "status": "CURRENT"})
        query, variables = m._compile()
        self.assertTrue(query.strip().startswith("mutation"))

    def test_compile_includes_mutation_name(self):
        m = SaveMediaListEntryMutation(None, None, {"mediaId": 1})
        query, _ = m._compile()
        self.assertIn("SaveMediaListEntry", query)

    def test_compile_variable_declarations(self):
        m = SaveMediaListEntryMutation(None, None, {"mediaId": 1, "status": "CURRENT"})
        query, variables = m._compile()
        self.assertIn("$mediaId: Int", query)
        self.assertIn("$status: MediaListStatus", query)
        self.assertEqual(variables, {"mediaId": 1, "status": "CURRENT"})

    def test_compile_argument_passthrough(self):
        m = SaveMediaListEntryMutation(None, None, {"mediaId": 1})
        query, _ = m._compile()
        self.assertIn("mediaId: $mediaId", query)

    def test_compile_default_fields(self):
        m = SaveMediaListEntryMutation(None, None, {"mediaId": 1})
        query, _ = m._compile()
        self.assertIn("id", query)
        self.assertIn("status", query)

    def test_compile_no_args(self):
        m = SaveMediaListEntryMutation(None, None, {})
        query, variables = m._compile()
        self.assertIn("mutation", query)
        self.assertEqual(variables, {})

    def test_compile_filters_none_values(self):
        m = SaveMediaListEntryMutation(None, None, {"mediaId": 1, "score": None})
        query, variables = m._compile()
        self.assertNotIn("score", query)
        self.assertEqual(variables, {"mediaId": 1})


class TestFieldsCustomization(unittest.TestCase):
    """Test .fields() override."""

    def test_fields_override(self):
        m = SaveMediaListEntryMutation(None, None, {"mediaId": 1})
        m.fields("id", "status", "progress", "score")
        query, _ = m._compile()
        self.assertIn("progress", query)
        self.assertIn("score", query)

    def test_fields_returns_self(self):
        m = SaveMediaListEntryMutation(None, None, {})
        result = m.fields("id")
        self.assertIs(result, m)

    def test_default_fields_used_when_no_override(self):
        m = DeleteMediaListEntryMutation(None, None, {"id": 1})
        query, _ = m._compile()
        self.assertIn("deleted", query)


class TestAllMutationClasses(unittest.TestCase):
    """Test that each mutation class compiles with correct name and args."""

    def _assert_compiles(self, cls, args, mutation_name, expected_fields=None):
        m = cls(None, None, args)
        query, variables = m._compile()
        self.assertIn(f"mutation", query)
        self.assertIn(mutation_name, query)
        for key in args:
            self.assertIn(f"${key}", query)
            self.assertIn(f"{key}: ${key}", query)
        if expected_fields:
            for f in expected_fields:
                self.assertIn(f, query)

    def test_save_media_list_entry(self):
        self._assert_compiles(SaveMediaListEntryMutation,
                              {"mediaId": 1, "status": "CURRENT"},
                              "SaveMediaListEntry", ["id", "status"])

    def test_update_media_list_entries(self):
        self._assert_compiles(UpdateMediaListEntriesMutation,
                              {"ids": [1, 2], "status": "COMPLETED"},
                              "UpdateMediaListEntries")

    def test_delete_media_list_entry(self):
        self._assert_compiles(DeleteMediaListEntryMutation,
                              {"id": 123}, "DeleteMediaListEntry", ["deleted"])

    def test_delete_custom_list(self):
        self._assert_compiles(DeleteCustomListMutation,
                              {"customList": "test", "type": "ANIME"},
                              "DeleteCustomList")

    def test_save_text_activity(self):
        self._assert_compiles(SaveTextActivityMutation,
                              {"text": "hello"}, "SaveTextActivity")

    def test_save_message_activity(self):
        self._assert_compiles(SaveMessageActivityMutation,
                              {"message": "hi", "recipientId": 1},
                              "SaveMessageActivity")

    def test_save_list_activity(self):
        self._assert_compiles(SaveListActivityMutation,
                              {"id": 1}, "SaveListActivity")

    def test_delete_activity(self):
        self._assert_compiles(DeleteActivityMutation,
                              {"id": 1}, "DeleteActivity", ["deleted"])

    def test_save_activity_reply(self):
        self._assert_compiles(SaveActivityReplyMutation,
                              {"activityId": 1, "text": "reply"},
                              "SaveActivityReply")

    def test_delete_activity_reply(self):
        self._assert_compiles(DeleteActivityReplyMutation,
                              {"id": 1}, "DeleteActivity", ["deleted"])

    def test_toggle_follow(self):
        self._assert_compiles(ToggleFollowMutation,
                              {"userId": 1}, "ToggleFollow")

    def test_toggle_favourite(self):
        self._assert_compiles(ToggleFavouriteMutation,
                              {"animeId": 1}, "ToggleFavourite")

    def test_update_favourite_order(self):
        self._assert_compiles(UpdateFavouriteOrderMutation,
                              {"animeIds": [1, 2]}, "UpdateFavouriteOrder")

    def test_toggle_like(self):
        self._assert_compiles(ToggleLikeMutation,
                              {"id": 1, "type": "ACTIVITY"}, "ToggleLikeV2")

    def test_save_review(self):
        self._assert_compiles(SaveReviewMutation,
                              {"mediaId": 1, "body": "great", "summary": "good", "score": 8},
                              "SaveReview")

    def test_delete_review(self):
        self._assert_compiles(DeleteReviewMutation,
                              {"id": 1}, "DeleteReview", ["deleted"])

    def test_rate_review(self):
        self._assert_compiles(RateReviewMutation,
                              {"reviewId": 1, "rating": "UP_VOTE"}, "RateReview")

    def test_save_recommendation(self):
        self._assert_compiles(SaveRecommendationMutation,
                              {"mediaId": 1, "mediaRecommendationId": 2, "rating": "RATE_UP"},
                              "SaveRecommendation")

    def test_save_thread(self):
        self._assert_compiles(SaveThreadMutation,
                              {"title": "Test", "body": "Content"}, "SaveThread")

    def test_delete_thread(self):
        self._assert_compiles(DeleteThreadMutation,
                              {"id": 1}, "DeleteThread", ["deleted"])

    def test_toggle_thread_subscription(self):
        self._assert_compiles(ToggleThreadSubscriptionMutation,
                              {"threadId": 1, "subscribe": True},
                              "ToggleThreadSubscription")

    def test_save_thread_comment(self):
        self._assert_compiles(SaveThreadCommentMutation,
                              {"threadId": 1, "comment": "nice"},
                              "SaveThreadComment")

    def test_delete_thread_comment(self):
        self._assert_compiles(DeleteThreadCommentMutation,
                              {"id": 1}, "DeleteThreadComment", ["deleted"])

    def test_update_user(self):
        self._assert_compiles(UpdateUserMutation,
                              {"about": "hello"}, "UpdateUser")

    def test_update_ani_chart_settings(self):
        self._assert_compiles(UpdateAniChartSettingsMutation,
                              {"titleLanguage": "ROMAJI"}, "UpdateAniChartSettings")

    def test_update_ani_chart_highlights(self):
        self._assert_compiles(UpdateAniChartHighlightsMutation,
                              {"highlights": []}, "UpdateAniChartHighlights")


class TestAuthToken(unittest.TestCase):
    """Test auth token injection in headers."""

    def test_token_in_constructor(self):
        client = Anilist(token="test_token_123")
        self.assertEqual(
            client.settings['header']['Authorization'],
            'Bearer test_token_123'
        )

    def test_no_token_by_default(self):
        client = Anilist()
        self.assertNotIn('Authorization', client.settings['header'])

    def test_set_token(self):
        client = Anilist()
        client.set_token("my_token")
        self.assertEqual(
            client.settings['header']['Authorization'],
            'Bearer my_token'
        )

    def test_remove_token(self):
        client = Anilist(token="my_token")
        client.remove_token()
        self.assertNotIn('Authorization', client.settings['header'])

    def test_remove_token_when_none(self):
        client = Anilist()
        client.remove_token()  # Should not raise
        self.assertNotIn('Authorization', client.settings['header'])

    def test_set_token_updates_async_conn(self):
        client = Anilist(token="old")
        # Force async connection creation
        _ = client._get_async_request()
        client.set_token("new_token")
        self.assertEqual(
            client._async_conn.settings['header']['Authorization'],
            'Bearer new_token'
        )

    def test_remove_token_updates_async_conn(self):
        client = Anilist(token="old")
        _ = client._get_async_request()
        client.remove_token()
        self.assertNotIn('Authorization', client._async_conn.settings['header'])


class TestMutationExecute(unittest.TestCase):
    """Test execute with mocked request_fn."""

    def test_execute_calls_request(self):
        mock_request = MagicMock(return_value={"data": {"SaveMediaListEntry": {"id": 1}}})
        m = SaveMediaListEntryMutation(mock_request, None, {"mediaId": 1, "status": "CURRENT"})
        result = m.execute()

        mock_request.assert_called_once()
        args = mock_request.call_args
        variables = args[0][0]
        query = args[0][1]
        self.assertEqual(variables, {"mediaId": 1, "status": "CURRENT"})
        self.assertIn("mutation", query)
        self.assertIn("SaveMediaListEntry", query)
        from Anisearch.models import MediaListEntry
        self.assertIsInstance(result, MediaListEntry)
        self.assertEqual(result.id, 1)

    def test_execute_with_fields_override(self):
        mock_request = MagicMock(return_value={"data": {}})
        m = SaveMediaListEntryMutation(mock_request, None, {"mediaId": 1})
        m.fields("id", "progress").execute()

        query = mock_request.call_args[0][1]
        self.assertIn("progress", query)


class TestAnilistMutationFactories(unittest.TestCase):
    """Test that Anilist factory methods return correct mutation builder types."""

    def setUp(self):
        self.client = Anilist()

    def test_save_media_list_entry(self):
        m = self.client.save_media_list_entry(mediaId=1, status="CURRENT")
        self.assertIsInstance(m, SaveMediaListEntryMutation)

    def test_delete_media_list_entry(self):
        m = self.client.delete_media_list_entry(id=1)
        self.assertIsInstance(m, DeleteMediaListEntryMutation)

    def test_toggle_follow(self):
        m = self.client.toggle_follow(userId=1)
        self.assertIsInstance(m, ToggleFollowMutation)

    def test_toggle_favourite(self):
        m = self.client.toggle_favourite(animeId=1)
        self.assertIsInstance(m, ToggleFavouriteMutation)

    def test_save_text_activity(self):
        m = self.client.save_text_activity(text="hello")
        self.assertIsInstance(m, SaveTextActivityMutation)

    def test_save_thread(self):
        m = self.client.save_thread(title="Test", body="Body")
        self.assertIsInstance(m, SaveThreadMutation)

    def test_update_user(self):
        m = self.client.update_user(about="test")
        self.assertIsInstance(m, UpdateUserMutation)

    def test_factory_passes_args(self):
        m = self.client.save_media_list_entry(mediaId=42, status="COMPLETED")
        self.assertEqual(m._args, {"mediaId": 42, "status": "COMPLETED"})


if __name__ == "__main__":
    unittest.main()
