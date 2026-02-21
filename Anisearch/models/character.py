"""Character model types."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from Anisearch.models._utils import _parse_obj
from Anisearch.models.shared import FuzzyDate


@dataclass
class CharacterName:
    first: Optional[str] = None
    middle: Optional[str] = None
    last: Optional[str] = None
    full: Optional[str] = None
    native: Optional[str] = None
    user_preferred: Optional[str] = None
    alternative: Optional[list] = None
    alternative_spoiler: Optional[list] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[CharacterName]:
        if not isinstance(data, dict):
            return None
        return cls(
            first=data.get("first"),
            middle=data.get("middle"),
            last=data.get("last"),
            full=data.get("full"),
            native=data.get("native"),
            user_preferred=data.get("userPreferred"),
            alternative=data.get("alternative"),
            alternative_spoiler=data.get("alternativeSpoiler"),
        )


@dataclass
class CharacterImage:
    large: Optional[str] = None
    medium: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[CharacterImage]:
        if not isinstance(data, dict):
            return None
        return cls(large=data.get("large"), medium=data.get("medium"))


@dataclass
class Character:
    id: Optional[int] = None
    description: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[str] = None
    blood_type: Optional[str] = None
    is_favourite: Optional[bool] = None
    is_favourite_blocked: Optional[bool] = None
    site_url: Optional[str] = None
    favourites: Optional[int] = None
    mod_notes: Optional[str] = None
    name: Optional[CharacterName] = None
    image: Optional[CharacterImage] = None
    date_of_birth: Optional[FuzzyDate] = None
    media: Optional[list] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[Character]:
        if not isinstance(data, dict):
            return None
        # media connection: edges or nodes
        media_raw = data.get("media")
        media_parsed = None
        if isinstance(media_raw, dict):
            from Anisearch.models.connections import _parse_media_connection
            media_parsed = _parse_media_connection(media_raw)
        elif isinstance(media_raw, list):
            media_parsed = media_raw

        return cls(
            id=data.get("id"),
            description=data.get("description"),
            gender=data.get("gender"),
            age=data.get("age"),
            blood_type=data.get("bloodType"),
            is_favourite=data.get("isFavourite"),
            is_favourite_blocked=data.get("isFavouriteBlocked"),
            site_url=data.get("siteUrl"),
            favourites=data.get("favourites"),
            mod_notes=data.get("modNotes"),
            name=_parse_obj(CharacterName, data.get("name")),
            image=_parse_obj(CharacterImage, data.get("image")),
            date_of_birth=_parse_obj(FuzzyDate, data.get("dateOfBirth")),
            media=media_parsed,
        )
