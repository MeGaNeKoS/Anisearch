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


class Anilist(Connection):
    logger = logging.getLogger(__name__)

    def __init__(self, *, settings=None, request_param=None, log_name=None, log_level=None,
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

    def raw_query(self, variables, query, **kwargs):
        return self.request(variables, query, **kwargs)

    @classmethod
    def set_logger_level(cls, level):
        Anilist.logger.setLevel(level)
