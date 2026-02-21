"""Staff model types."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from Anisearch.models._utils import _parse_obj
from Anisearch.models.shared import FuzzyDate


@dataclass
class StaffName:
    first: Optional[str] = None
    middle: Optional[str] = None
    last: Optional[str] = None
    full: Optional[str] = None
    native: Optional[str] = None
    user_preferred: Optional[str] = None
    alternative: Optional[list] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[StaffName]:
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
        )


@dataclass
class StaffImage:
    large: Optional[str] = None
    medium: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[StaffImage]:
        if not isinstance(data, dict):
            return None
        return cls(large=data.get("large"), medium=data.get("medium"))


@dataclass
class Staff:
    id: Optional[int] = None
    language_v2: Optional[str] = None
    description: Optional[str] = None
    primary_occupations: Optional[List[str]] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    years_active: Optional[List[int]] = None
    home_town: Optional[str] = None
    blood_type: Optional[str] = None
    is_favourite: Optional[bool] = None
    is_favourite_blocked: Optional[bool] = None
    site_url: Optional[str] = None
    favourites: Optional[int] = None
    submission_status: Optional[int] = None
    submission_notes: Optional[str] = None
    mod_notes: Optional[str] = None
    name: Optional[StaffName] = None
    image: Optional[StaffImage] = None
    date_of_birth: Optional[FuzzyDate] = None
    date_of_death: Optional[FuzzyDate] = None
    staff_media: Optional[list] = None
    characters: Optional[list] = None
    character_media: Optional[list] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[Staff]:
        if not isinstance(data, dict):
            return None
        return cls(
            id=data.get("id"),
            language_v2=data.get("languageV2"),
            description=data.get("description"),
            primary_occupations=data.get("primaryOccupations"),
            gender=data.get("gender"),
            age=data.get("age"),
            years_active=data.get("yearsActive"),
            home_town=data.get("homeTown"),
            blood_type=data.get("bloodType"),
            is_favourite=data.get("isFavourite"),
            is_favourite_blocked=data.get("isFavouriteBlocked"),
            site_url=data.get("siteUrl"),
            favourites=data.get("favourites"),
            submission_status=data.get("submissionStatus"),
            submission_notes=data.get("submissionNotes"),
            mod_notes=data.get("modNotes"),
            name=_parse_obj(StaffName, data.get("name")),
            image=_parse_obj(StaffImage, data.get("image")),
            date_of_birth=_parse_obj(FuzzyDate, data.get("dateOfBirth")),
            date_of_death=_parse_obj(FuzzyDate, data.get("dateOfDeath")),
            staff_media=data.get("staffMedia"),
            characters=data.get("characters"),
            character_media=data.get("characterMedia"),
        )
