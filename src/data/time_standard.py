"""UTC system-time and Europe/Istanbul display conversion."""

from datetime import datetime, timezone
from zoneinfo import ZoneInfo

TR_TIMEZONE = ZoneInfo("Europe/Istanbul")


def to_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        raise ValueError("Timezone-aware datetime required")
    return value.astimezone(timezone.utc)


def to_turkey_time(value: datetime) -> datetime:
    return to_utc(value).astimezone(TR_TIMEZONE)

