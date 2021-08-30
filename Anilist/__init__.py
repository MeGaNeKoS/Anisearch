from .get import *
from .search import *


class Anilist:
    """
        Initialize a new instance to the Anilist API.
    """

    def __init__(self):
        """

        """

        self.settings = {'header': {'Content-Type': 'application/json',
                                    'User-Agent': 'Anilist (github.com/MeGaNeKoS/Anilist)',
                                    'Accept': 'application/json'},
                         'authurl': 'https://anilist.co/api',
                         'apiurl': 'https://graphql.anilist.co'}
        self.search = AnilistSearch(self.settings)
        self.get = AnilistGet(self.settings)
