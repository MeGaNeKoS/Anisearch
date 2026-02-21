"""Media model and its nested types."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from Anisearch.models._utils import _parse_list, _parse_obj
from Anisearch.models.shared import (
    AiringScheduleNode,
    FuzzyDate,
    MediaTrendNode,
)


@dataclass
class MediaTitle:
    romaji: Optional[str] = None
    english: Optional[str] = None
    native: Optional[str] = None
    user_preferred: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[MediaTitle]:
        if not isinstance(data, dict):
            return None
        return cls(
            romaji=data.get("romaji"),
            english=data.get("english"),
            native=data.get("native"),
            user_preferred=data.get("userPreferred"),
        )


@dataclass
class MediaCoverImage:
    extra_large: Optional[str] = None
    large: Optional[str] = None
    medium: Optional[str] = None
    color: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[MediaCoverImage]:
        if not isinstance(data, dict):
            return None
        return cls(
            extra_large=data.get("extraLarge"),
            large=data.get("large"),
            medium=data.get("medium"),
            color=data.get("color"),
        )


@dataclass
class MediaTrailer:
    id: Optional[str] = None
    site: Optional[str] = None
    thumbnail: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[MediaTrailer]:
        if not isinstance(data, dict):
            return None
        return cls(id=data.get("id"), site=data.get("site"), thumbnail=data.get("thumbnail"))


@dataclass
class MediaTag:
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    rank: Optional[int] = None
    is_general_spoiler: Optional[bool] = None
    is_media_spoiler: Optional[bool] = None
    is_adult: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[MediaTag]:
        if not isinstance(data, dict):
            return None
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            description=data.get("description"),
            category=data.get("category"),
            rank=data.get("rank"),
            is_general_spoiler=data.get("isGeneralSpoiler"),
            is_media_spoiler=data.get("isMediaSpoiler"),
            is_adult=data.get("isAdult"),
        )


@dataclass
class MediaExternalLink:
    id: Optional[int] = None
    url: Optional[str] = None
    site: Optional[str] = None
    site_id: Optional[int] = None
    type: Optional[str] = None
    language: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[MediaExternalLink]:
        if not isinstance(data, dict):
            return None
        return cls(
            id=data.get("id"),
            url=data.get("url"),
            site=data.get("site"),
            site_id=data.get("siteId"),
            type=data.get("type"),
            language=data.get("language"),
            color=data.get("color"),
            icon=data.get("icon"),
        )


@dataclass
class MediaStreamingEpisode:
    title: Optional[str] = None
    thumbnail: Optional[str] = None
    url: Optional[str] = None
    site: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[MediaStreamingEpisode]:
        if not isinstance(data, dict):
            return None
        return cls(
            title=data.get("title"),
            thumbnail=data.get("thumbnail"),
            url=data.get("url"),
            site=data.get("site"),
        )


@dataclass
class MediaRank:
    id: Optional[int] = None
    rank: Optional[int] = None
    type: Optional[str] = None
    format: Optional[str] = None
    year: Optional[int] = None
    season: Optional[str] = None
    all_time: Optional[bool] = None
    context: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[MediaRank]:
        if not isinstance(data, dict):
            return None
        return cls(
            id=data.get("id"),
            rank=data.get("rank"),
            type=data.get("type"),
            format=data.get("format"),
            year=data.get("year"),
            season=data.get("season"),
            all_time=data.get("allTime"),
            context=data.get("context"),
        )


@dataclass
class MediaList:
    id: Optional[int] = None
    status: Optional[str] = None
    score: Optional[float] = None
    progress: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[MediaList]:
        if not isinstance(data, dict):
            return None
        return cls(
            id=data.get("id"),
            status=data.get("status"),
            score=data.get("score"),
            progress=data.get("progress"),
        )


@dataclass
class StatusDistribution:
    status: Optional[str] = None
    amount: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[StatusDistribution]:
        if not isinstance(data, dict):
            return None
        return cls(status=data.get("status"), amount=data.get("amount"))


@dataclass
class ScoreDistribution:
    score: Optional[int] = None
    amount: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[ScoreDistribution]:
        if not isinstance(data, dict):
            return None
        return cls(score=data.get("score"), amount=data.get("amount"))


@dataclass
class MediaStats:
    status_distribution: Optional[List[StatusDistribution]] = None
    score_distribution: Optional[List[ScoreDistribution]] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[MediaStats]:
        if not isinstance(data, dict):
            return None
        return cls(
            status_distribution=_parse_list(StatusDistribution, data.get("statusDistribution")),
            score_distribution=_parse_list(ScoreDistribution, data.get("scoreDistribution")),
        )


@dataclass
class ReviewNode:
    id: Optional[int] = None
    user_id: Optional[int] = None
    summary: Optional[str] = None
    rating: Optional[int] = None
    rating_amount: Optional[int] = None
    score: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[ReviewNode]:
        if not isinstance(data, dict):
            return None
        return cls(
            id=data.get("id"),
            user_id=data.get("userId"),
            summary=data.get("summary"),
            rating=data.get("rating"),
            rating_amount=data.get("ratingAmount"),
            score=data.get("score"),
        )


@dataclass
class RecommendationNode:
    id: Optional[int] = None
    rating: Optional[int] = None
    media_recommendation: Optional[object] = None  # Media (deferred)

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[RecommendationNode]:
        if not isinstance(data, dict):
            return None
        media_rec = data.get("mediaRecommendation")
        parsed_rec = None
        if isinstance(media_rec, dict):
            parsed_rec = Media.from_dict(media_rec)
        return cls(
            id=data.get("id"),
            rating=data.get("rating"),
            media_recommendation=parsed_rec,
        )


@dataclass
class Media:
    id: Optional[int] = None
    id_mal: Optional[int] = None
    type: Optional[str] = None
    format: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None
    season: Optional[str] = None
    season_year: Optional[int] = None
    season_int: Optional[int] = None
    episodes: Optional[int] = None
    duration: Optional[int] = None
    chapters: Optional[int] = None
    volumes: Optional[int] = None
    country_of_origin: Optional[str] = None
    is_licensed: Optional[bool] = None
    source: Optional[str] = None
    hashtag: Optional[str] = None
    updated_at: Optional[int] = None
    banner_image: Optional[str] = None
    genres: Optional[List[str]] = None
    synonyms: Optional[List[str]] = None
    average_score: Optional[int] = None
    mean_score: Optional[int] = None
    popularity: Optional[int] = None
    is_locked: Optional[bool] = None
    trending: Optional[int] = None
    favourites: Optional[int] = None
    is_favourite: Optional[bool] = None
    is_favourite_blocked: Optional[bool] = None
    is_adult: Optional[bool] = None
    site_url: Optional[str] = None
    auto_create_forum_thread: Optional[bool] = None
    is_recommendation_blocked: Optional[bool] = None
    is_review_blocked: Optional[bool] = None
    mod_notes: Optional[str] = None
    title: Optional[MediaTitle] = None
    cover_image: Optional[MediaCoverImage] = None
    start_date: Optional[FuzzyDate] = None
    end_date: Optional[FuzzyDate] = None
    trailer: Optional[MediaTrailer] = None
    next_airing_episode: Optional[AiringScheduleNode] = None
    tags: Optional[List[MediaTag]] = None
    external_links: Optional[List[MediaExternalLink]] = None
    streaming_episodes: Optional[List[MediaStreamingEpisode]] = None
    rankings: Optional[List[MediaRank]] = None
    media_list_entry: Optional[MediaList] = None
    stats: Optional[MediaStats] = None
    characters: Optional[list] = None
    staff: Optional[list] = None
    studios: Optional[list] = None
    relations: Optional[list] = None
    reviews: Optional[list] = None
    recommendations: Optional[list] = None
    airing_schedule: Optional[list] = None
    trends: Optional[list] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[Media]:
        if not isinstance(data, dict):
            return None
        from Anisearch.models.connections import (
            CharacterEdge,
            MediaRelationEdge,
            StaffEdge,
            StudioEdge,
            _parse_edges,
        )

        return cls(
            id=data.get("id"),
            id_mal=data.get("idMal"),
            type=data.get("type"),
            format=data.get("format"),
            status=data.get("status"),
            description=data.get("description"),
            season=data.get("season"),
            season_year=data.get("seasonYear"),
            season_int=data.get("seasonInt"),
            episodes=data.get("episodes"),
            duration=data.get("duration"),
            chapters=data.get("chapters"),
            volumes=data.get("volumes"),
            country_of_origin=data.get("countryOfOrigin"),
            is_licensed=data.get("isLicensed"),
            source=data.get("source"),
            hashtag=data.get("hashtag"),
            updated_at=data.get("updatedAt"),
            banner_image=data.get("bannerImage"),
            genres=data.get("genres"),
            synonyms=data.get("synonyms"),
            average_score=data.get("averageScore"),
            mean_score=data.get("meanScore"),
            popularity=data.get("popularity"),
            is_locked=data.get("isLocked"),
            trending=data.get("trending"),
            favourites=data.get("favourites"),
            is_favourite=data.get("isFavourite"),
            is_favourite_blocked=data.get("isFavouriteBlocked"),
            is_adult=data.get("isAdult"),
            site_url=data.get("siteUrl"),
            auto_create_forum_thread=data.get("autoCreateForumThread"),
            is_recommendation_blocked=data.get("isRecommendationBlocked"),
            is_review_blocked=data.get("isReviewBlocked"),
            mod_notes=data.get("modNotes"),
            title=_parse_obj(MediaTitle, data.get("title")),
            cover_image=_parse_obj(MediaCoverImage, data.get("coverImage")),
            start_date=_parse_obj(FuzzyDate, data.get("startDate")),
            end_date=_parse_obj(FuzzyDate, data.get("endDate")),
            trailer=_parse_obj(MediaTrailer, data.get("trailer")),
            next_airing_episode=_parse_obj(AiringScheduleNode, data.get("nextAiringEpisode")),
            tags=_parse_list(MediaTag, data.get("tags")),
            external_links=_parse_list(MediaExternalLink, data.get("externalLinks")),
            streaming_episodes=_parse_list(MediaStreamingEpisode, data.get("streamingEpisodes")),
            rankings=_parse_list(MediaRank, data.get("rankings")),
            media_list_entry=_parse_obj(MediaList, data.get("mediaListEntry")),
            stats=_parse_obj(MediaStats, data.get("stats")),
            characters=_parse_edges(CharacterEdge, data.get("characters")),
            staff=_parse_edges(StaffEdge, data.get("staff")),
            studios=_parse_edges(StudioEdge, data.get("studios")),
            relations=_parse_edges(MediaRelationEdge, data.get("relations")),
            reviews=_parse_nodes(ReviewNode, data.get("reviews")),
            recommendations=_parse_nodes(RecommendationNode, data.get("recommendations")),
            airing_schedule=_parse_nodes(AiringScheduleNode, data.get("airingSchedule")),
            trends=_parse_nodes(MediaTrendNode, data.get("trends")),
        )


def _parse_nodes(node_cls, data):
    """Parse a ``{"nodes": [...]}`` connection into a list."""
    if not isinstance(data, dict):
        return None
    nodes = data.get("nodes")
    if not isinstance(nodes, list):
        return None
    return [node_cls.from_dict(n) for n in nodes if isinstance(n, dict)]
