"""Shared model types used across multiple entities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, List, Optional, Type, TypeVar

from Anisearch.models._utils import _parse_list, _parse_obj

T = TypeVar("T")


@dataclass
class FuzzyDate:
    year: Optional[int] = None
    month: Optional[int] = None
    day: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[FuzzyDate]:
        if not isinstance(data, dict):
            return None
        return cls(year=data.get("year"), month=data.get("month"), day=data.get("day"))


@dataclass
class PageInfo:
    total: Optional[int] = None
    per_page: Optional[int] = None
    current_page: Optional[int] = None
    last_page: Optional[int] = None
    has_next_page: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[PageInfo]:
        if not isinstance(data, dict):
            return None
        return cls(
            total=data.get("total"),
            per_page=data.get("perPage"),
            current_page=data.get("currentPage"),
            last_page=data.get("lastPage"),
            has_next_page=data.get("hasNextPage"),
        )


@dataclass
class PageResult(Generic[T]):
    page_info: Optional[PageInfo] = None
    items: Optional[List[T]] = None

    @classmethod
    def from_dict(cls, data: Optional[dict], item_cls: Type[T] = None, collection_key: str = "media") -> Optional[PageResult[T]]:
        if not isinstance(data, dict):
            return None
        return cls(
            page_info=PageInfo.from_dict(data.get("pageInfo")),
            items=_parse_list(item_cls, data.get(collection_key)) if item_cls else None,
        )


@dataclass
class AiringScheduleNode:
    id: Optional[int] = None
    airing_at: Optional[int] = None
    time_until_airing: Optional[int] = None
    episode: Optional[int] = None
    media_id: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[AiringScheduleNode]:
        if not isinstance(data, dict):
            return None
        return cls(
            id=data.get("id"),
            airing_at=data.get("airingAt"),
            time_until_airing=data.get("timeUntilAiring"),
            episode=data.get("episode"),
            media_id=data.get("mediaId"),
        )


@dataclass
class MediaTrendNode:
    media_id: Optional[int] = None
    date: Optional[int] = None
    trending: Optional[int] = None
    average_score: Optional[int] = None
    popularity: Optional[int] = None
    in_progress: Optional[int] = None
    releasing: Optional[bool] = None
    episode: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[MediaTrendNode]:
        if not isinstance(data, dict):
            return None
        return cls(
            media_id=data.get("mediaId"),
            date=data.get("date"),
            trending=data.get("trending"),
            average_score=data.get("averageScore"),
            popularity=data.get("popularity"),
            in_progress=data.get("inProgress"),
            releasing=data.get("releasing"),
            episode=data.get("episode"),
        )
