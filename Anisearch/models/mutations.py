"""Mutation response model types."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from Anisearch.models.shared import FuzzyDate


@dataclass
class DeleteResult:
    deleted: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[DeleteResult]:
        if not isinstance(data, dict):
            return None
        return cls(deleted=data.get("deleted"))


@dataclass
class MediaListEntry:
    id: Optional[int] = None
    status: Optional[str] = None
    score: Optional[float] = None
    progress: Optional[int] = None
    progress_volumes: Optional[int] = None
    repeat: Optional[int] = None
    priority: Optional[int] = None
    private: Optional[bool] = None
    notes: Optional[str] = None
    started_at: Optional[FuzzyDate] = None
    completed_at: Optional[FuzzyDate] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[MediaListEntry]:
        if not isinstance(data, dict):
            return None
        return cls(
            id=data.get("id"),
            status=data.get("status"),
            score=data.get("score"),
            progress=data.get("progress"),
            progress_volumes=data.get("progressVolumes"),
            repeat=data.get("repeat"),
            priority=data.get("priority"),
            private=data.get("private"),
            notes=data.get("notes"),
            started_at=FuzzyDate.from_dict(data.get("startedAt")),
            completed_at=FuzzyDate.from_dict(data.get("completedAt")),
        )


@dataclass
class TextActivity:
    id: Optional[int] = None
    type: Optional[str] = None
    text: Optional[str] = None
    user_id: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[TextActivity]:
        if not isinstance(data, dict):
            return None
        return cls(id=data.get("id"), type=data.get("type"), text=data.get("text"), user_id=data.get("userId"))


@dataclass
class MessageActivity:
    id: Optional[int] = None
    type: Optional[str] = None
    message: Optional[str] = None
    recipient_id: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[MessageActivity]:
        if not isinstance(data, dict):
            return None
        return cls(
            id=data.get("id"), type=data.get("type"),
            message=data.get("message"), recipient_id=data.get("recipientId"),
        )


@dataclass
class ListActivity:
    id: Optional[int] = None
    type: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[ListActivity]:
        if not isinstance(data, dict):
            return None
        return cls(id=data.get("id"), type=data.get("type"))


@dataclass
class ActivityReply:
    id: Optional[int] = None
    text: Optional[str] = None
    activity_id: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[ActivityReply]:
        if not isinstance(data, dict):
            return None
        return cls(id=data.get("id"), text=data.get("text"), activity_id=data.get("activityId"))


@dataclass
class UserFollowResult:
    id: Optional[int] = None
    name: Optional[str] = None
    is_following: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[UserFollowResult]:
        if not isinstance(data, dict):
            return None
        return cls(id=data.get("id"), name=data.get("name"), is_following=data.get("isFollowing"))


@dataclass
class FavouritesResult:
    anime: Optional[list] = None
    manga: Optional[list] = None
    characters: Optional[list] = None
    staff: Optional[list] = None
    studios: Optional[list] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[FavouritesResult]:
        if not isinstance(data, dict):
            return None
        return cls(
            anime=data.get("anime"),
            manga=data.get("manga"),
            characters=data.get("characters"),
            staff=data.get("staff"),
            studios=data.get("studios"),
        )


@dataclass
class ReviewResult:
    id: Optional[int] = None
    summary: Optional[str] = None
    body: Optional[str] = None
    rating: Optional[int] = None
    rating_amount: Optional[int] = None
    score: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[ReviewResult]:
        if not isinstance(data, dict):
            return None
        return cls(
            id=data.get("id"),
            summary=data.get("summary"),
            body=data.get("body"),
            rating=data.get("rating"),
            rating_amount=data.get("ratingAmount"),
            score=data.get("score"),
        )


@dataclass
class RecommendationResult:
    id: Optional[int] = None
    rating: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[RecommendationResult]:
        if not isinstance(data, dict):
            return None
        return cls(id=data.get("id"), rating=data.get("rating"))


@dataclass
class ThreadResult:
    id: Optional[int] = None
    title: Optional[str] = None
    body: Optional[str] = None
    is_subscribed: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[ThreadResult]:
        if not isinstance(data, dict):
            return None
        return cls(
            id=data.get("id"), title=data.get("title"),
            body=data.get("body"), is_subscribed=data.get("isSubscribed"),
        )


@dataclass
class ThreadCommentResult:
    id: Optional[int] = None
    comment: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[ThreadCommentResult]:
        if not isinstance(data, dict):
            return None
        return cls(id=data.get("id"), comment=data.get("comment"))


@dataclass
class ToggleLikeResult:
    id: Optional[int] = None
    type: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[ToggleLikeResult]:
        if not isinstance(data, dict):
            return None
        return cls(id=data.get("id"), type=data.get("type"))


@dataclass
class UserResult:
    id: Optional[int] = None
    name: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[UserResult]:
        if not isinstance(data, dict):
            return None
        return cls(id=data.get("id"), name=data.get("name"))
