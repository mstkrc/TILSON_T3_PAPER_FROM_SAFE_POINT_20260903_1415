"""Phase-7 candidate-only validation; no wallet, risk, or execution behavior."""

import json
from datetime import datetime, timezone
from pathlib import Path

from src.strategy.candidates import CandidateInput, CandidateStatus, filter_candidates, rank_candidates

ROOT = Path(__file__).parents[1]
UTC = datetime(2026, 1, 1, 11, tzinfo=timezone.utc)


def candidate(symbol, adx=30, slope="RISING", volume=100, signal="LONG_CANDIDATE", direction="LONG", **kwargs):
    return CandidateInput(symbol, direction, signal, adx, slope, volume, UTC, UTC, **kwargs)


def test_volume_and_inactive_filters():
    result = filter_candidates([candidate("A", volume=10), candidate("B", symbol_status="BREAK"), candidate("C", data_quality_ok=False)], min_volume_24h=50)
    assert result[0].status == CandidateStatus.BLOCKED and result[0].blocked_reason == "LOW_24H_VOLUME"
    assert result[1].blocked_reason == "INACTIVE_OR_DELISTED"
    assert result[2].blocked_reason == "LOW_DATA_QUALITY"


def test_open_position_ignores_volume_filter():
    result = filter_candidates([candidate("A", volume=1, has_open_position=True)], min_volume_24h=50)
    assert result[0].status == CandidateStatus.VALID


def test_ranking_order_and_same_pool():
    items = filter_candidates([candidate("LOW", adx=20), candidate("HIGH", adx=50, slope="NEAR_FLAT"), candidate("SLOPE", adx=50, slope="RISING", volume=1), candidate("SHORT", adx=50, slope="RISING", volume=200, signal="SHORT_CANDIDATE", direction="SHORT")])
    ranked = rank_candidates(items)
    assert [item.candidate.symbol for item in ranked] == ["SHORT", "SLOPE", "HIGH", "LOW"]
    assert {item.candidate.direction for item in ranked} == {"LONG", "SHORT"}


def test_deterministic_ranking_and_live_lock():
    items = filter_candidates([candidate("B", adx=40), candidate("A", adx=40)])
    assert [x.candidate.symbol for x in rank_candidates(items)] == ["A", "B"]
    config = json.loads((ROOT / "config/live_lock_config.json").read_text(encoding="utf-8"))
    assert config["LIVE_TRADING"] is False
    assert not list((ROOT / "src/strategy").glob("*execution*"))
