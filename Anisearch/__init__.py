import logging
import warnings

try:
    from Anisearch._version import version as __version__
except ImportError:
    __version__ = "0.0.0"

from Anisearch.connection import Connection
from Anisearch.retry import RetryStrategy
from Anisearch.fragment import Fragment
from Anisearch.builders.media import MediaBuilder
from Anisearch.builders.character import CharacterBuilder
from Anisearch.builders.staff import StaffBuilder
from Anisearch.builders.studio import StudioBuilder
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


class Anilist(Connection):
    logger = logging.getLogger(__name__)

    def __init__(self, *, token=None, settings=None, request_param=None, log_name=None, log_level=None,
                 retry=RetryStrategy(), **kwargs):
        if log_name:
            self.logger = logging.getLogger(f"{__name__}@{log_name}")
            self.logger.setLevel(log_level or logging.root.level)
        elif log_level:
            warnings.warn("log_level is ignored if log_name is None, package's logger is used!")
        super().__init__(settings, request_param, retry=retry)

        self._async_conn = None
        self._async_settings = settings
        self._retry = retry

        if token:
            self.set_token(token)

    def _get_async_request(self):
        if self._async_conn is None:
            from Anisearch.async_connection import AsyncConnection
            self._async_conn = AsyncConnection(
                setting=self._async_settings,
                retry=self._retry
            )
        return self._async_conn.request

    def media(self, **kwargs) -> MediaBuilder:
        return MediaBuilder(self.request, self._get_async_request, "Media", kwargs)

    def character(self, **kwargs) -> CharacterBuilder:
        return CharacterBuilder(self.request, self._get_async_request, "Character", kwargs)

    def staff(self, **kwargs) -> StaffBuilder:
        return StaffBuilder(self.request, self._get_async_request, "Staff", kwargs)

    def studio(self, **kwargs) -> StudioBuilder:
        return StudioBuilder(self.request, self._get_async_request, "Studio", kwargs)

    # ── Mutation factory methods ─────────────────────────────────────────

    def save_media_list_entry(self, **kwargs) -> SaveMediaListEntryMutation:
        return SaveMediaListEntryMutation(self.request, self._get_async_request, kwargs)

    def update_media_list_entries(self, **kwargs) -> UpdateMediaListEntriesMutation:
        return UpdateMediaListEntriesMutation(self.request, self._get_async_request, kwargs)

    def delete_media_list_entry(self, **kwargs) -> DeleteMediaListEntryMutation:
        return DeleteMediaListEntryMutation(self.request, self._get_async_request, kwargs)

    def delete_custom_list(self, **kwargs) -> DeleteCustomListMutation:
        return DeleteCustomListMutation(self.request, self._get_async_request, kwargs)

    def save_text_activity(self, **kwargs) -> SaveTextActivityMutation:
        return SaveTextActivityMutation(self.request, self._get_async_request, kwargs)

    def save_message_activity(self, **kwargs) -> SaveMessageActivityMutation:
        return SaveMessageActivityMutation(self.request, self._get_async_request, kwargs)

    def save_list_activity(self, **kwargs) -> SaveListActivityMutation:
        return SaveListActivityMutation(self.request, self._get_async_request, kwargs)

    def delete_activity(self, **kwargs) -> DeleteActivityMutation:
        return DeleteActivityMutation(self.request, self._get_async_request, kwargs)

    def save_activity_reply(self, **kwargs) -> SaveActivityReplyMutation:
        return SaveActivityReplyMutation(self.request, self._get_async_request, kwargs)

    def delete_activity_reply(self, **kwargs) -> DeleteActivityReplyMutation:
        return DeleteActivityReplyMutation(self.request, self._get_async_request, kwargs)

    def toggle_follow(self, **kwargs) -> ToggleFollowMutation:
        return ToggleFollowMutation(self.request, self._get_async_request, kwargs)

    def toggle_favourite(self, **kwargs) -> ToggleFavouriteMutation:
        return ToggleFavouriteMutation(self.request, self._get_async_request, kwargs)

    def update_favourite_order(self, **kwargs) -> UpdateFavouriteOrderMutation:
        return UpdateFavouriteOrderMutation(self.request, self._get_async_request, kwargs)

    def toggle_like(self, **kwargs) -> ToggleLikeMutation:
        return ToggleLikeMutation(self.request, self._get_async_request, kwargs)

    def save_review(self, **kwargs) -> SaveReviewMutation:
        return SaveReviewMutation(self.request, self._get_async_request, kwargs)

    def delete_review(self, **kwargs) -> DeleteReviewMutation:
        return DeleteReviewMutation(self.request, self._get_async_request, kwargs)

    def rate_review(self, **kwargs) -> RateReviewMutation:
        return RateReviewMutation(self.request, self._get_async_request, kwargs)

    def save_recommendation(self, **kwargs) -> SaveRecommendationMutation:
        return SaveRecommendationMutation(self.request, self._get_async_request, kwargs)

    def save_thread(self, **kwargs) -> SaveThreadMutation:
        return SaveThreadMutation(self.request, self._get_async_request, kwargs)

    def delete_thread(self, **kwargs) -> DeleteThreadMutation:
        return DeleteThreadMutation(self.request, self._get_async_request, kwargs)

    def toggle_thread_subscription(self, **kwargs) -> ToggleThreadSubscriptionMutation:
        return ToggleThreadSubscriptionMutation(self.request, self._get_async_request, kwargs)

    def save_thread_comment(self, **kwargs) -> SaveThreadCommentMutation:
        return SaveThreadCommentMutation(self.request, self._get_async_request, kwargs)

    def delete_thread_comment(self, **kwargs) -> DeleteThreadCommentMutation:
        return DeleteThreadCommentMutation(self.request, self._get_async_request, kwargs)

    def update_user(self, **kwargs) -> UpdateUserMutation:
        return UpdateUserMutation(self.request, self._get_async_request, kwargs)

    def update_ani_chart_settings(self, **kwargs) -> UpdateAniChartSettingsMutation:
        return UpdateAniChartSettingsMutation(self.request, self._get_async_request, kwargs)

    def update_ani_chart_highlights(self, **kwargs) -> UpdateAniChartHighlightsMutation:
        return UpdateAniChartHighlightsMutation(self.request, self._get_async_request, kwargs)

    def raw_query(self, variables, query, **kwargs):
        return self.request(variables, query, **kwargs)

    def set_token(self, token):
        """Set the OAuth2 bearer token for authenticated requests."""
        self.settings['header']['Authorization'] = f'Bearer {token}'
        if self._async_conn is not None:
            self._async_conn.settings['header']['Authorization'] = f'Bearer {token}'
        if self._async_settings is not None:
            self._async_settings.setdefault('header', {})['Authorization'] = f'Bearer {token}'

    def remove_token(self):
        """Remove the OAuth2 bearer token."""
        self.settings['header'].pop('Authorization', None)
        if self._async_conn is not None:
            self._async_conn.settings['header'].pop('Authorization', None)
        if self._async_settings is not None and 'header' in self._async_settings:
            self._async_settings['header'].pop('Authorization', None)

    @classmethod
    def set_logger_level(cls, level):
        Anilist.logger.setLevel(level)
