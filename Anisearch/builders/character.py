"""Character query builder — complete coverage of AniList Character type (14 fields)."""

from Anisearch.builders.base import BaseBuilder


class CharacterBuilder(BaseBuilder):
    _graphql_type = "Character"

    # --- Scalar fields ---

    def id(self):
        self._add_scalar("id")
        return self

    def description(self, as_html=False):
        if as_html:
            self._add_scalar("description(asHtml: true)")
        else:
            self._add_scalar("description")
        return self

    def gender(self):
        self._add_scalar("gender")
        return self

    def age(self):
        self._add_scalar("age")
        return self

    def blood_type(self):
        self._add_scalar("bloodType")
        return self

    def is_favourite(self):
        self._add_scalar("isFavourite")
        return self

    def is_favourite_blocked(self):
        self._add_scalar("isFavouriteBlocked")
        return self

    def site_url(self):
        self._add_scalar("siteUrl")
        return self

    def favourites(self):
        self._add_scalar("favourites")
        return self

    def mod_notes(self):
        self._add_scalar("modNotes")
        return self

    # --- Object fields ---

    def name(self, *fields):
        """Sub-fields: "first", "middle", "last", "full", "native",
        "userPreferred", "alternative", "alternativeSpoiler"."""
        self._add_object("name", fields,
                         defaults=("first", "middle", "last", "full", "native",
                                   "userPreferred", "alternative", "alternativeSpoiler"))
        return self

    def image(self, *fields):
        """Sub-fields: "large", "medium"."""
        self._add_object("image", fields, defaults=("large",))
        return self

    def date_of_birth(self, *fields):
        self._add_object("dateOfBirth", fields, defaults=("year", "month", "day"))
        return self

    # --- Connection fields ---

    def media(self, *, sort=None, type=None, on_list=None, page=None, per_page=None, fields=None):
        """Media connection. fields: lambda m: m.title("romaji")"""
        from Anisearch.builders.media import MediaBuilder
        args = {}
        if sort is not None:
            args["sort"] = sort
        if type is not None:
            args["type"] = type
        if on_list is not None:
            args["onList"] = on_list
        if page is not None:
            args["page"] = page
        if per_page is not None:
            args["perPage"] = per_page
        self._add_connection("media", args=args, fields_fn=fields,
                             node_type=MediaBuilder,
                             edge_fields=["id", "characterRole"])
        return self
