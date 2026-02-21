"""Mutation builder classes for all AniList GraphQL mutations."""

from __future__ import annotations

from Anisearch.builders.base import BaseMutationBuilder


def _model(mod_attr):
    """Create a property that lazily imports a model class from Anisearch.models.mutations."""
    @property
    def _response_model(self):
        from Anisearch.models import mutations as m
        return getattr(m, mod_attr)
    return _response_model


# ── Media List ────────────────────────────────────────────────────────────────

class SaveMediaListEntryMutation(BaseMutationBuilder):
    _mutation_name = "SaveMediaListEntry"
    _default_fields = ["id", "status"]
    _response_model = _model("MediaListEntry")
    _arg_types = {
        "id": "Int",
        "mediaId": "Int",
        "status": "MediaListStatus",
        "score": "Float",
        "scoreRaw": "Int",
        "progress": "Int",
        "progressVolumes": "Int",
        "repeat": "Int",
        "priority": "Int",
        "private": "Boolean",
        "notes": "String",
        "hiddenFromStatusLists": "Boolean",
        "customLists": "[String]",
        "advancedScores": "[Float]",
        "startedAt": "FuzzyDateInput",
        "completedAt": "FuzzyDateInput",
    }


class UpdateMediaListEntriesMutation(BaseMutationBuilder):
    _mutation_name = "UpdateMediaListEntries"
    _default_fields = ["id", "status"]
    _response_model = _model("MediaListEntry")
    _arg_types = {
        "ids": "[Int]",
        "status": "MediaListStatus",
        "score": "Float",
        "scoreRaw": "Int",
        "progress": "Int",
        "progressVolumes": "Int",
        "repeat": "Int",
        "priority": "Int",
        "private": "Boolean",
        "notes": "String",
        "hiddenFromStatusLists": "Boolean",
        "advancedScores": "[Float]",
        "startedAt": "FuzzyDateInput",
        "completedAt": "FuzzyDateInput",
    }


class DeleteMediaListEntryMutation(BaseMutationBuilder):
    _mutation_name = "DeleteMediaListEntry"
    _default_fields = ["deleted"]
    _response_model = _model("DeleteResult")
    _arg_types = {
        "id": "Int",
    }


class DeleteCustomListMutation(BaseMutationBuilder):
    _mutation_name = "DeleteCustomList"
    _default_fields = ["deleted"]
    _response_model = _model("DeleteResult")
    _arg_types = {
        "customList": "String",
        "type": "MediaType",
    }


# ── Activities ────────────────────────────────────────────────────────────────

class SaveTextActivityMutation(BaseMutationBuilder):
    _mutation_name = "SaveTextActivity"
    _default_fields = ["id", "type", "text"]
    _response_model = _model("TextActivity")
    _arg_types = {
        "id": "Int",
        "text": "String",
    }


class SaveMessageActivityMutation(BaseMutationBuilder):
    _mutation_name = "SaveMessageActivity"
    _default_fields = ["id", "type", "message"]
    _response_model = _model("MessageActivity")
    _arg_types = {
        "id": "Int",
        "message": "String",
        "recipientId": "Int",
        "private": "Boolean",
    }


class SaveListActivityMutation(BaseMutationBuilder):
    _mutation_name = "SaveListActivity"
    _default_fields = ["id", "type"]
    _response_model = _model("ListActivity")
    _arg_types = {
        "id": "Int",
    }


class DeleteActivityMutation(BaseMutationBuilder):
    _mutation_name = "DeleteActivity"
    _default_fields = ["deleted"]
    _response_model = _model("DeleteResult")
    _arg_types = {
        "id": "Int",
    }


class SaveActivityReplyMutation(BaseMutationBuilder):
    _mutation_name = "SaveActivityReply"
    _default_fields = ["id", "text"]
    _response_model = _model("ActivityReply")
    _arg_types = {
        "id": "Int",
        "activityId": "Int",
        "text": "String",
    }


class DeleteActivityReplyMutation(BaseMutationBuilder):
    _mutation_name = "DeleteActivity"
    _default_fields = ["deleted"]
    _response_model = _model("DeleteResult")
    _arg_types = {
        "id": "Int",
    }


# ── Social ────────────────────────────────────────────────────────────────────

class ToggleFollowMutation(BaseMutationBuilder):
    _mutation_name = "ToggleFollow"
    _default_fields = ["id", "name", "isFollowing"]
    _response_model = _model("UserFollowResult")
    _arg_types = {
        "userId": "Int",
    }


class ToggleFavouriteMutation(BaseMutationBuilder):
    _mutation_name = "ToggleFavourite"
    _default_fields = ["anime { nodes { id } }", "manga { nodes { id } }"]
    _response_model = _model("FavouritesResult")
    _arg_types = {
        "animeId": "Int",
        "mangaId": "Int",
        "characterId": "Int",
        "staffId": "Int",
        "studioId": "Int",
    }


class UpdateFavouriteOrderMutation(BaseMutationBuilder):
    _mutation_name = "UpdateFavouriteOrder"
    _default_fields = ["anime { nodes { id } }"]
    _response_model = _model("FavouritesResult")
    _arg_types = {
        "animeIds": "[Int]",
        "mangaIds": "[Int]",
        "characterIds": "[Int]",
        "staffIds": "[Int]",
        "studioIds": "[Int]",
        "animeOrder": "[Int]",
        "mangaOrder": "[Int]",
        "characterOrder": "[Int]",
        "staffOrder": "[Int]",
        "studioOrder": "[Int]",
    }


class ToggleLikeMutation(BaseMutationBuilder):
    _mutation_name = "ToggleLikeV2"
    _default_fields = ["id", "type"]
    _response_model = _model("ToggleLikeResult")
    _arg_types = {
        "id": "Int",
        "type": "LikeableType",
    }


# ── Reviews ───────────────────────────────────────────────────────────────────

class SaveReviewMutation(BaseMutationBuilder):
    _mutation_name = "SaveReview"
    _default_fields = ["id", "summary", "body"]
    _response_model = _model("ReviewResult")
    _arg_types = {
        "id": "Int",
        "mediaId": "Int",
        "body": "String",
        "summary": "String",
        "score": "Int",
        "private": "Boolean",
    }


class DeleteReviewMutation(BaseMutationBuilder):
    _mutation_name = "DeleteReview"
    _default_fields = ["deleted"]
    _response_model = _model("DeleteResult")
    _arg_types = {
        "id": "Int",
    }


class RateReviewMutation(BaseMutationBuilder):
    _mutation_name = "RateReview"
    _default_fields = ["id", "rating", "ratingAmount"]
    _response_model = _model("ReviewResult")
    _arg_types = {
        "reviewId": "Int",
        "rating": "ReviewRating",
    }


# ── Recommendations ───────────────────────────────────────────────────────────

class SaveRecommendationMutation(BaseMutationBuilder):
    _mutation_name = "SaveRecommendation"
    _default_fields = ["id", "rating"]
    _response_model = _model("RecommendationResult")
    _arg_types = {
        "mediaId": "Int",
        "mediaRecommendationId": "Int",
        "rating": "RecommendationRating",
    }


# ── Threads ───────────────────────────────────────────────────────────────────

class SaveThreadMutation(BaseMutationBuilder):
    _mutation_name = "SaveThread"
    _default_fields = ["id", "title"]
    _response_model = _model("ThreadResult")
    _arg_types = {
        "id": "Int",
        "title": "String",
        "body": "String",
        "categories": "[Int]",
        "mediaCategories": "[Int]",
        "sticky": "Boolean",
        "locked": "Boolean",
    }


class DeleteThreadMutation(BaseMutationBuilder):
    _mutation_name = "DeleteThread"
    _default_fields = ["deleted"]
    _response_model = _model("DeleteResult")
    _arg_types = {
        "id": "Int",
    }


class ToggleThreadSubscriptionMutation(BaseMutationBuilder):
    _mutation_name = "ToggleThreadSubscription"
    _default_fields = ["id", "isSubscribed"]
    _response_model = _model("ThreadResult")
    _arg_types = {
        "threadId": "Int",
        "subscribe": "Boolean",
    }


class SaveThreadCommentMutation(BaseMutationBuilder):
    _mutation_name = "SaveThreadComment"
    _default_fields = ["id", "comment"]
    _response_model = _model("ThreadCommentResult")
    _arg_types = {
        "id": "Int",
        "threadId": "Int",
        "parentCommentId": "Int",
        "comment": "String",
    }


class DeleteThreadCommentMutation(BaseMutationBuilder):
    _mutation_name = "DeleteThreadComment"
    _default_fields = ["deleted"]
    _response_model = _model("DeleteResult")
    _arg_types = {
        "id": "Int",
    }


# ── User Settings ─────────────────────────────────────────────────────────────

class UpdateUserMutation(BaseMutationBuilder):
    _mutation_name = "UpdateUser"
    _default_fields = ["id", "name"]
    _response_model = _model("UserResult")
    _arg_types = {
        "about": "String",
        "titleLanguage": "UserTitleLanguage",
        "displayAdultContent": "Boolean",
        "airingNotifications": "Boolean",
        "scoreFormat": "ScoreFormat",
        "rowOrder": "String",
        "profileColor": "String",
        "donatorBadge": "String",
        "notificationOptions": "[NotificationOptionInput]",
        "timezone": "String",
        "activityMergeTime": "Int",
        "animeListOptions": "MediaListOptionsInput",
        "mangaListOptions": "MediaListOptionsInput",
        "staffNameLanguage": "UserStaffNameLanguage",
        "restrictMessagesToFollowing": "Boolean",
        "disabledListActivity": "[ListActivityOptionInput]",
    }


class UpdateAniChartSettingsMutation(BaseMutationBuilder):
    _mutation_name = "UpdateAniChartSettings"
    _default_fields = ["id"]
    _response_model = _model("UserResult")
    _arg_types = {
        "titleLanguage": "String",
        "outgoingLinkProvider": "String",
        "theme": "String",
        "sort": "String",
    }


class UpdateAniChartHighlightsMutation(BaseMutationBuilder):
    _mutation_name = "UpdateAniChartHighlights"
    _default_fields = ["id"]
    _response_model = _model("UserResult")
    _arg_types = {
        "highlights": "[AniChartHighlightInput]",
    }
