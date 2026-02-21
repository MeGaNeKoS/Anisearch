"""Connection/edge types for nested relationships."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from Anisearch.models._utils import _parse_obj


@dataclass
class CharacterEdge:
    id: Optional[int] = None
    role: Optional[str] = None
    node: Optional[object] = None  # Character (deferred)

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[CharacterEdge]:
        if not isinstance(data, dict):
            return None
        from Anisearch.models.character import Character
        return cls(
            id=data.get("id"),
            role=data.get("role"),
            node=_parse_obj(Character, data.get("node")),
        )


@dataclass
class StaffEdge:
    id: Optional[int] = None
    role: Optional[str] = None
    node: Optional[object] = None  # Staff (deferred)

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[StaffEdge]:
        if not isinstance(data, dict):
            return None
        from Anisearch.models.staff import Staff
        return cls(
            id=data.get("id"),
            role=data.get("role"),
            node=_parse_obj(Staff, data.get("node")),
        )


@dataclass
class StudioEdge:
    is_main: Optional[bool] = None
    node: Optional[object] = None  # Studio (deferred)

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[StudioEdge]:
        if not isinstance(data, dict):
            return None
        from Anisearch.models.studio import Studio
        return cls(
            is_main=data.get("isMain"),
            node=_parse_obj(Studio, data.get("node")),
        )


@dataclass
class MediaRelationEdge:
    id: Optional[int] = None
    relation_type: Optional[str] = None
    node: Optional[object] = None  # Media (deferred)

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[MediaRelationEdge]:
        if not isinstance(data, dict):
            return None
        from Anisearch.models.media import Media
        return cls(
            id=data.get("id"),
            relation_type=data.get("relationType"),
            node=_parse_obj(Media, data.get("node")),
        )


def _parse_edges(edge_cls, data: Optional[dict], key: str = "edges") -> Optional[List]:
    """Parse a connection dict ``{"edges": [...]}`` into a list of edge dataclasses."""
    if not isinstance(data, dict):
        return None
    edges_raw = data.get(key)
    if not isinstance(edges_raw, list):
        return None
    return [edge_cls.from_dict(e) for e in edges_raw if isinstance(e, dict)]


def _parse_media_connection(data: Optional[dict]) -> Optional[list]:
    """Parse a media connection, handling both edges and nodes."""
    if not isinstance(data, dict):
        return None
    if "edges" in data:
        return _parse_edges(MediaRelationEdge, data)
    if "nodes" in data:
        from Anisearch.models.media import Media
        from Anisearch.models._utils import _parse_list
        return _parse_list(Media, data.get("nodes"))
    return None
