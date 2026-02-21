"""Staff query builder — complete coverage of AniList Staff type (25 fields)."""

from __future__ import annotations

import sys
from typing import Callable, List, Optional

if sys.version_info >= (3, 11):
    from typing import Literal
else:
    from typing_extensions import Literal

from Anisearch.builders.base import BaseBuilder
from Anisearch.enums import CHARACTER_SORT, MEDIA_SORT, MEDIA_TYPE


class StaffBuilder(BaseBuilder):
    _graphql_type = "Staff"

    @property
    def _response_model(self):
        from Anisearch.models.staff import Staff
        return Staff

    # --- Scalar fields ---

    def id(self) -> StaffBuilder:
        """Select the ``id`` field."""
        self._add_scalar("id")
        return self

    def language_v2(self) -> StaffBuilder:
        """Select the ``languageV2`` field."""
        self._add_scalar("languageV2")
        return self

    def language(self) -> StaffBuilder:
        """Alias for ``language_v2``."""
        self._add_scalar("languageV2")
        return self

    def description(self, as_html: bool = False) -> StaffBuilder:
        """Select the ``description`` field. Set ``as_html=True`` for HTML formatting."""
        if as_html:
            self._add_scalar("description(asHtml: true)")
        else:
            self._add_scalar("description")
        return self

    def primary_occupations(self) -> StaffBuilder:
        """Select the ``primaryOccupations`` field (list of strings)."""
        self._add_scalar("primaryOccupations")
        return self

    def gender(self) -> StaffBuilder:
        """Select the ``gender`` field."""
        self._add_scalar("gender")
        return self

    def age(self) -> StaffBuilder:
        """Select the ``age`` field."""
        self._add_scalar("age")
        return self

    def years_active(self) -> StaffBuilder:
        """Select the ``yearsActive`` field (list of ints)."""
        self._add_scalar("yearsActive")
        return self

    def home_town(self) -> StaffBuilder:
        """Select the ``homeTown`` field."""
        self._add_scalar("homeTown")
        return self

    def blood_type(self) -> StaffBuilder:
        """Select the ``bloodType`` field."""
        self._add_scalar("bloodType")
        return self

    def is_favourite(self) -> StaffBuilder:
        """Select the ``isFavourite`` field (requires auth)."""
        self._add_scalar("isFavourite")
        return self

    def is_favourite_blocked(self) -> StaffBuilder:
        """Select the ``isFavouriteBlocked`` field."""
        self._add_scalar("isFavouriteBlocked")
        return self

    def site_url(self) -> StaffBuilder:
        """Select the ``siteUrl`` field (AniList URL)."""
        self._add_scalar("siteUrl")
        return self

    def favourites(self) -> StaffBuilder:
        """Select the ``favourites`` field."""
        self._add_scalar("favourites")
        return self

    def submission_status(self) -> StaffBuilder:
        """Select the ``submissionStatus`` field."""
        self._add_scalar("submissionStatus")
        return self

    def submission_notes(self) -> StaffBuilder:
        """Select the ``submissionNotes`` field."""
        self._add_scalar("submissionNotes")
        return self

    def mod_notes(self) -> StaffBuilder:
        """Select the ``modNotes`` field (mod only)."""
        self._add_scalar("modNotes")
        return self

    # --- Object fields ---

    def name(
        self,
        *fields: Literal[
            "first", "middle", "last", "full", "native", "userPreferred", "alternative"
        ]
    ) -> StaffBuilder:
        """Select staff name sub-fields. Defaults to all if none specified."""
        self._add_object("name", fields,
                         defaults=("first", "middle", "last", "full", "native", "userPreferred", "alternative"))
        return self

    def image(
        self, *fields: Literal["large", "medium"]
    ) -> StaffBuilder:
        """Select staff image sub-fields. Defaults to ``large``."""
        self._add_object("image", fields, defaults=("large",))
        return self

    def date_of_birth(
        self, *fields: Literal["year", "month", "day"]
    ) -> StaffBuilder:
        """Select date of birth sub-fields. Defaults to all."""
        self._add_object("dateOfBirth", fields, defaults=("year", "month", "day"))
        return self

    def date_of_death(
        self, *fields: Literal["year", "month", "day"]
    ) -> StaffBuilder:
        """Select date of death sub-fields. Defaults to all."""
        self._add_object("dateOfDeath", fields, defaults=("year", "month", "day"))
        return self

    # --- Connection fields ---

    def staff_media(
        self,
        *,
        sort: Optional[List[MEDIA_SORT]] = None,
        type: Optional[MEDIA_TYPE] = None,
        on_list: Optional[bool] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        fields: Optional[Callable] = None,
    ) -> StaffBuilder:
        """Nested media connection for this staff member.

        Note: ``page``/``per_page`` paginate the *media inside this staff*,
        not the top-level query. Use ``.page()`` to paginate staff results.
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
        self._add_connection("staffMedia", args=args, fields_fn=fields,
                             node_type=MediaBuilder,
                             edge_fields=["staffRole"])
        return self

    def characters(
        self,
        *,
        sort: Optional[List[CHARACTER_SORT]] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        fields: Optional[Callable] = None,
    ) -> StaffBuilder:
        """Nested characters connection for this staff member.

        Note: ``page``/``per_page`` paginate the *characters inside this staff*,
        not the top-level query. Use ``.page()`` to paginate staff results.
        """
        from Anisearch.builders.character import CharacterBuilder
        args = {}
        if sort is not None:
            args["sort"] = sort
        if page is not None:
            args["page"] = page
        if per_page is not None:
            args["perPage"] = per_page
        self._add_connection("characters", args=args, fields_fn=fields,
                             node_type=CharacterBuilder)
        return self

    def character_media(
        self,
        *,
        sort: Optional[List[MEDIA_SORT]] = None,
        on_list: Optional[bool] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        fields: Optional[Callable] = None,
    ) -> StaffBuilder:
        """Nested character-media connection for this staff member.

        Note: ``page``/``per_page`` paginate the *media inside this staff*,
        not the top-level query. Use ``.page()`` to paginate staff results.
        """
        from Anisearch.builders.media import MediaBuilder
        args = {}
        if sort is not None:
            args["sort"] = sort
        if on_list is not None:
            args["onList"] = on_list
        if page is not None:
            args["page"] = page
        if per_page is not None:
            args["perPage"] = per_page
        self._add_connection("characterMedia", args=args, fields_fn=fields,
                             node_type=MediaBuilder,
                             edge_fields=["characterRole", "characterName"])
        return self

    def media(self, *, fields: Optional[Callable] = None) -> StaffBuilder:
        """Alias — delegates to staff_media."""
        return self.staff_media(fields=fields)
