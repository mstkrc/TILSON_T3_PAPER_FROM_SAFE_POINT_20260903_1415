"""Candidate filtering and deterministic ranking; no trade authorization."""

from dataclasses import dataclass, replace
from datetime import datetime
from enum import Enum


class CandidateStatus(str, Enum):
    VALID = "VALID"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class CandidateInput:
    symbol: str
    direction: str
    signal_type: str
    adx_value: float
    adx_slope_state: str
    volume_24h: float
    candle_timestamp_utc: datetime
    candle_timestamp_tr: datetime
    blocked_reason: str | None = None
    symbol_status: str = "TRADING"
    data_quality_ok: bool = True
    has_open_position: bool = False
    is_new_entry: bool = True


@dataclass(frozen=True)
class CandidateOutput:
    candidate: CandidateInput
    status: CandidateStatus
    blocked_reason: str | None = None


def filter_candidates(candidates: list[CandidateInput], *, min_volume_24h: float = 0) -> list[CandidateOutput]:
    outputs = []
    for item in candidates:
        reason = item.blocked_reason
        if item.symbol_status != "TRADING":
            reason = "INACTIVE_OR_DELISTED"
        elif not item.data_quality_ok:
            reason = "LOW_DATA_QUALITY"
        elif item.is_new_entry and not item.has_open_position and item.volume_24h < min_volume_24h:
            reason = "LOW_24H_VOLUME"
        outputs.append(CandidateOutput(item, CandidateStatus.BLOCKED if reason else CandidateStatus.VALID, reason))
    return outputs


def rank_candidates(outputs: list[CandidateOutput]) -> list[CandidateOutput]:
    slope_rank = {"RISING": 2, "NEAR_FLAT": 1, "FALLING": 0}
    signal_rank = {"LONG_CANDIDATE": 2, "SHORT_CANDIDATE": 2, "CONTINUATION": 1}
    valid = [item for item in outputs if item.status == CandidateStatus.VALID]
    return sorted(valid, key=lambda item: (
        -item.candidate.adx_value,
        -slope_rank.get(item.candidate.adx_slope_state, 0),
        -item.candidate.volume_24h,
        -signal_rank.get(item.candidate.signal_type, 0),
        item.candidate.symbol,
        item.candidate.direction,
    ))
