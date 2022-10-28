import logging
import warnings

from Anisearch.connection import Connection
from Anisearch.get import AnilistGet
from Anisearch.search import AnilistSearch


class Anilist(Connection):
    logger = logging.getLogger(__name__)

    def __init__(self, *, settings=None, request_param=None, log_name=None, log_level=None):
        # use package's logger if log_name is None
        if log_name:
            self.logger = logging.getLogger(f"{__name__}@{log_name}")
            self.logger.setLevel(log_level or logging.root.level)  # set log level for this package
        elif log_level:
            warnings.warn("log_level is ignored if log_name is None, package's logger is used!")
        self.logger.debug('Initializing Anilist Connection')
        super(Anilist, self).__init__(settings, request_param)

        self.logger.debug('Initializing Anilist API')
        self.search = AnilistSearch(self.request)
        self.get = AnilistGet(self.request)

    # set package's logger level
    @classmethod
    def set_logger_level(cls, level):
        Anilist.logger.setLevel(level)
