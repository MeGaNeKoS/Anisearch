"""Studio query builder — complete coverage of AniList Studio type (7 fields)."""

from __future__ import annotations

import sys
from typing import Callable, List, Optional

if sys.version_info >= (3, 11):
    from typing import Literal
else:
    from typing_extensions import Literal

from Anisearch.builders.base import BaseBuilder
from Anisearch.enums import MEDIA_SORT


class StudioBuilder(BaseBuilder):
    _graphql_type = "Studio"

    @property
    def _response_model(self):
        from Anisearch.models.studio import Studio
        return Studio

    # --- Scalar fields ---

    def id(self) -> StudioBuilder:
        """Select the ``id`` field."""
        self._add_scalar("id")
        return self

    def name(self) -> StudioBuilder:
        """Select the ``name`` field."""
        self._add_scalar("name")
        return self

    def is_animation_studio(self) -> StudioBuilder:
        """Select the ``isAnimationStudio`` field."""
        self._add_scalar("isAnimationStudio")
        return self

    def site_url(self) -> StudioBuilder:
        """Select the ``siteUrl`` field (AniList URL)."""
        self._add_scalar("siteUrl")
        return self

    def is_favourite(self) -> StudioBuilder:
        """Select the ``isFavourite`` field (requires auth)."""
        self._add_scalar("isFavourite")
        return self

    def favourites(self) -> StudioBuilder:
        """Select the ``favourites`` field."""
        self._add_scalar("favourites")
        return self

    # --- Connection fields ---

    def media(
        self,
        *,
        sort: Optional[List[MEDIA_SORT]] = None,
        is_main: Optional[bool] = None,
        on_list: Optional[bool] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        fields: Optional[Callable] = None,
    ) -> StudioBuilder:
        """Nested media connection for this studio.

        Note: ``page``/``per_page`` paginate the *media inside this studio*,
        not the top-level query. Use ``.page()`` to paginate studio results.
        """
        from Anisearch.builders.media import MediaBuilder
        args = {}
        if sort is not None:
            args["sort"] = sort
        if is_main is not None:
            args["isMain"] = is_main
        if on_list is not None:
            args["onList"] = on_list
        if page is not None:
            args["page"] = page
        if per_page is not None:
            args["perPage"] = per_page
        self._add_connection("media", args=args, fields_fn=fields,
                             node_type=MediaBuilder,
                             edge_fields=["isMainStudio"])
        return self
