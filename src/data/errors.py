"""Data-quality error categories for Phase-3 diagnostics."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class DataErrorScope(str, Enum):
    COIN_LEVEL = "COIN_LEVEL"
    SYSTEM_LEVEL = "SYSTEM_LEVEL"


@dataclass(frozen=True)
class DataQualityIssue:
    scope: DataErrorScope
    code: str
    message: str
    symbol: Optional[str] = None
