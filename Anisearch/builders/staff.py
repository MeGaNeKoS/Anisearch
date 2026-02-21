"""Staff query builder — complete coverage of AniList Staff type (25 fields)."""

from __future__ import annotations

import sys
from typing import Callable, Optional

if sys.version_info >= (3, 11):
    from typing import Literal
else:
    from typing_extensions import Literal

from Anisearch.builders.base import BaseBuilder


class StaffBuilder(BaseBuilder):
    _graphql_type = "Staff"

    # --- Scalar fields ---

    def id(self):
        self._add_scalar("id")
        return self

    def language_v2(self):
        self._add_scalar("languageV2")
        return self

    def language(self):
        """Alias for languageV2."""
        self._add_scalar("languageV2")
        return self

    def description(self, as_html=False):
        if as_html:
            self._add_scalar("description(asHtml: true)")
        else:
            self._add_scalar("description")
        return self

    def primary_occupations(self):
        self._add_scalar("primaryOccupations")
        return self

    def gender(self):
        self._add_scalar("gender")
        return self

    def age(self):
        self._add_scalar("age")
        return self

    def years_active(self):
        self._add_scalar("yearsActive")
        return self

    def home_town(self):
        self._add_scalar("homeTown")
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

    def submission_status(self):
        self._add_scalar("submissionStatus")
        return self

    def submission_notes(self):
        self._add_scalar("submissionNotes")
        return self

    def mod_notes(self):
        self._add_scalar("modNotes")
        return self

    # --- Object fields ---

    def name(
        self,
        *fields: Literal[
            "first", "middle", "last", "full", "native", "userPreferred", "alternative"
        ]
    ) -> StaffBuilder:
        self._add_object("name", fields,
                         defaults=("first", "middle", "last", "full", "native", "userPreferred", "alternative"))
        return self

    def image(
        self, *fields: Literal["large", "medium"]
    ) -> StaffBuilder:
        self._add_object("image", fields, defaults=("large",))
        return self

    def date_of_birth(
        self, *fields: Literal["year", "month", "day"]
    ) -> StaffBuilder:
        self._add_object("dateOfBirth", fields, defaults=("year", "month", "day"))
        return self

    def date_of_death(
        self, *fields: Literal["year", "month", "day"]
    ) -> StaffBuilder:
        self._add_object("dateOfDeath", fields, defaults=("year", "month", "day"))
        return self

    # --- Connection fields ---

    def staff_media(self, *, sort=None, type=None, on_list=None, page=None, per_page=None, fields=None):
        """Media where this person is staff."""
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

    def characters(self, *, sort=None, page=None, per_page=None, fields=None):
        """Characters voiced/played by this staff."""
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

    def character_media(self, *, sort=None, on_list=None, page=None, per_page=None, fields=None):
        """Media where this person voiced/played characters."""
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

    def media(self, *, fields=None):
        """Alias — delegates to staff_media."""
        return self.staff_media(fields=fields)
