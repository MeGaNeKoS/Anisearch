"""Studio query builder — complete coverage of AniList Studio type (7 fields)."""

from __future__ import annotations

import sys
from typing import Callable, Optional

if sys.version_info >= (3, 11):
    from typing import Literal
else:
    from typing_extensions import Literal

from Anisearch.builders.base import BaseBuilder


class StudioBuilder(BaseBuilder):
    _graphql_type = "Studio"

    # --- Scalar fields ---

    def id(self):
        self._add_scalar("id")
        return self

    def name(self):
        self._add_scalar("name")
        return self

    def is_animation_studio(self):
        self._add_scalar("isAnimationStudio")
        return self

    def site_url(self):
        self._add_scalar("siteUrl")
        return self

    def is_favourite(self):
        self._add_scalar("isFavourite")
        return self

    def favourites(self):
        self._add_scalar("favourites")
        return self

    # --- Connection fields ---

    def media(self, *, sort=None, is_main=None, on_list=None, page=None, per_page=None, fields=None):
        """Media produced by this studio."""
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
