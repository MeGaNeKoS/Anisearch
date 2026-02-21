"""Internal helpers for parsing API responses into dataclass instances."""

from __future__ import annotations

from typing import List, Optional, Type, TypeVar

T = TypeVar("T")


def _parse_obj(cls: Type[T], data) -> Optional[T]:
    """Parse a dict into a dataclass instance via its ``from_dict`` classmethod.

    Returns *None* when *data* is not a dict.
    """
    if not isinstance(data, dict):
        return None
    return cls.from_dict(data)  # type: ignore[attr-defined]


def _parse_list(cls: Type[T], data) -> Optional[List[T]]:
    """Parse a list of dicts into a list of dataclass instances.

    Returns *None* when *data* is not a list.
    """
    if not isinstance(data, list):
        return None
    return [cls.from_dict(item) for item in data if isinstance(item, dict)]  # type: ignore[attr-defined]
