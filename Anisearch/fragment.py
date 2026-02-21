"""Reusable field groups (fragments) for query builders."""


class FragmentDef:
    """Stores field selections from a configuration function."""

    def __init__(self, fields):
        self._fields = fields


class Fragment:
    """Factory for creating reusable field selections.

    Usage:
        basic = Fragment.media(lambda m: m.title("romaji", "english").genres())
        result = anilist.media(id=13601).use(basic).episodes().execute()
    """

    @staticmethod
    def media(configure_fn):
        from Anisearch.builders.media import MediaBuilder
        builder = MediaBuilder(None, None, "", {})
        configure_fn(builder)
        return FragmentDef(builder._collect_fields())

    @staticmethod
    def character(configure_fn):
        from Anisearch.builders.character import CharacterBuilder
        builder = CharacterBuilder(None, None, "", {})
        configure_fn(builder)
        return FragmentDef(builder._collect_fields())

    @staticmethod
    def staff(configure_fn):
        from Anisearch.builders.staff import StaffBuilder
        builder = StaffBuilder(None, None, "", {})
        configure_fn(builder)
        return FragmentDef(builder._collect_fields())

    @staticmethod
    def studio(configure_fn):
        from Anisearch.builders.studio import StudioBuilder
        builder = StudioBuilder(None, None, "", {})
        configure_fn(builder)
        return FragmentDef(builder._collect_fields())
