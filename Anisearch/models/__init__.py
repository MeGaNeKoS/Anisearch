"""Public model types for typed API responses."""

from Anisearch.models.shared import (
    AiringScheduleNode,
    FuzzyDate,
    MediaTrendNode,
    PageInfo,
    PageResult,
)
from Anisearch.models.media import (
    Media,
    MediaCoverImage,
    MediaExternalLink,
    MediaList,
    MediaRank,
    MediaStats,
    MediaStreamingEpisode,
    MediaTag,
    MediaTitle,
    MediaTrailer,
    RecommendationNode,
    ReviewNode,
    ScoreDistribution,
    StatusDistribution,
)
from Anisearch.models.character import Character, CharacterImage, CharacterName
from Anisearch.models.staff import Staff, StaffImage, StaffName
from Anisearch.models.studio import Studio
from Anisearch.models.connections import (
    CharacterEdge,
    MediaRelationEdge,
    StaffEdge,
    StudioEdge,
)
from Anisearch.models.mutations import (
    ActivityReply,
    DeleteResult,
    FavouritesResult,
    ListActivity,
    MediaListEntry,
    MessageActivity,
    RecommendationResult,
    ReviewResult,
    TextActivity,
    ThreadCommentResult,
    ThreadResult,
    ToggleLikeResult,
    UserFollowResult,
    UserResult,
)

__all__ = [
    # Shared
    "FuzzyDate", "PageInfo", "PageResult", "AiringScheduleNode", "MediaTrendNode",
    # Media
    "Media", "MediaTitle", "MediaCoverImage", "MediaTrailer", "MediaTag",
    "MediaExternalLink", "MediaStreamingEpisode", "MediaRank", "MediaList",
    "MediaStats", "StatusDistribution", "ScoreDistribution",
    "ReviewNode", "RecommendationNode",
    # Character
    "Character", "CharacterName", "CharacterImage",
    # Staff
    "Staff", "StaffName", "StaffImage",
    # Studio
    "Studio",
    # Connections
    "CharacterEdge", "StaffEdge", "StudioEdge", "MediaRelationEdge",
    # Mutations
    "DeleteResult", "MediaListEntry", "TextActivity", "MessageActivity",
    "ListActivity", "ActivityReply", "UserFollowResult", "FavouritesResult",
    "ReviewResult", "RecommendationResult", "ThreadResult", "ThreadCommentResult",
    "ToggleLikeResult", "UserResult",
]
