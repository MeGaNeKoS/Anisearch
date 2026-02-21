"""Studio model types."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Studio:
    id: Optional[int] = None
    name: Optional[str] = None
    is_animation_studio: Optional[bool] = None
    site_url: Optional[str] = None
    is_favourite: Optional[bool] = None
    favourites: Optional[int] = None
    media: Optional[list] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[Studio]:
        if not isinstance(data, dict):
            return None
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            is_animation_studio=data.get("isAnimationStudio"),
            site_url=data.get("siteUrl"),
            is_favourite=data.get("isFavourite"),
            favourites=data.get("favourites"),
            media=data.get("media"),
        )
