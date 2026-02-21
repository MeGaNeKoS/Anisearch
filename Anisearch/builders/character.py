"""Character query builder — complete coverage of AniList Character type (14 fields)."""

from __future__ import annotations

import sys
from typing import Callable, List, Optional

if sys.version_info >= (3, 11):
    from typing import Literal
else:
    from typing_extensions import Literal

from Anisearch.builders.base import BaseBuilder
from Anisearch.enums import MEDIA_SORT, MEDIA_TYPE


class CharacterBuilder(BaseBuilder):
    _graphql_type = "Character"

    @property
    def _response_model(self):
        from Anisearch.models.character import Character
        return Character

    # --- Scalar fields ---

    def id(self) -> CharacterBuilder:
        """Select the ``id`` field."""
        self._add_scalar("id")
        return self

    def description(self, as_html: bool = False) -> CharacterBuilder:
        """Select the ``description`` field. Set ``as_html=True`` for HTML formatting."""
        if as_html:
            self._add_scalar("description(asHtml: true)")
        else:
            self._add_scalar("description")
        return self

    def gender(self) -> CharacterBuilder:
        """Select the ``gender`` field."""
        self._add_scalar("gender")
        return self

    def age(self) -> CharacterBuilder:
        """Select the ``age`` field."""
        self._add_scalar("age")
        return self

    def blood_type(self) -> CharacterBuilder:
        """Select the ``bloodType`` field."""
        self._add_scalar("bloodType")
        return self

    def is_favourite(self) -> CharacterBuilder:
        """Select the ``isFavourite`` field (requires auth)."""
        self._add_scalar("isFavourite")
        return self

    def is_favourite_blocked(self) -> CharacterBuilder:
        """Select the ``isFavouriteBlocked`` field."""
        self._add_scalar("isFavouriteBlocked")
        return self

    def site_url(self) -> CharacterBuilder:
        """Select the ``siteUrl`` field (AniList URL)."""
        self._add_scalar("siteUrl")
        return self

    def favourites(self) -> CharacterBuilder:
        """Select the ``favourites`` field."""
        self._add_scalar("favourites")
        return self

    def mod_notes(self) -> CharacterBuilder:
        """Select the ``modNotes`` field (mod only)."""
        self._add_scalar("modNotes")
        return self

    # --- Object fields ---

    def name(
        self,
        *fields: Literal[
            "first", "middle", "last", "full", "native",
            "userPreferred", "alternative", "alternativeSpoiler"
        ]
    ) -> CharacterBuilder:
        """Select character name sub-fields. Defaults to all if none specified."""
        self._add_object("name", fields,
                         defaults=("first", "middle", "last", "full", "native",
                                   "userPreferred", "alternative", "alternativeSpoiler"))
        return self

    def image(
        self, *fields: Literal["large", "medium"]
    ) -> CharacterBuilder:
        """Select character image sub-fields. Defaults to ``large``."""
        self._add_object("image", fields, defaults=("large",))
        return self

    def date_of_birth(
        self, *fields: Literal["year", "month", "day"]
    ) -> CharacterBuilder:
        """Select date of birth sub-fields. Defaults to all."""
        self._add_object("dateOfBirth", fields, defaults=("year", "month", "day"))
        return self

    # --- Connection fields ---

    def media(
        self,
        *,
        sort: Optional[List[MEDIA_SORT]] = None,
        type: Optional[MEDIA_TYPE] = None,
        on_list: Optional[bool] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        fields: Optional[Callable] = None,
    ) -> CharacterBuilder:
        """Nested media connection within this character.

        Note: ``page``/``per_page`` paginate the *media inside this character*,
        not the top-level query. Use ``.page()`` to paginate character results.
        """
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
