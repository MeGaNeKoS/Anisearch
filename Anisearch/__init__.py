import logging

from Anisearch.get import AnilistGet
from Anisearch.search import AnilistSearch
from Anisearch.connection import Connection


class Anilist:
    logger = logging.getLogger(__name__)

    def __init__(self, log_level=logging.root.level, settings=None, request_param=None):
        Anilist.logger.setLevel(log_level)  # set log level for this package

        self.connection = Connection(settings, request_param)
        Anilist.logger.info('Initializing Anilist API')

        self.search = AnilistSearch(self.connection)
        self.get = AnilistGet(self.connection)
