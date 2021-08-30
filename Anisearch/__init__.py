from .get import *
from .search import *


class Anilist:
    """
        Initialize a new instance to the Anisearch API.
    """

    def __init__(self):
        """

        """

        self.settings = {'header': {'Content-Type': 'application/json',
                                    'User-Agent': 'Anisearch (github.com/MeGaNeKoS/Anisearch)',
                                    'Accept': 'application/json'},
                         'authurl': 'https://anilist.co/api',
                         'apiurl': 'https://graphql.anilist.co'}
        self.search = AnilistSearch(self.settings)
        self.get = AnilistGet(self.settings)
