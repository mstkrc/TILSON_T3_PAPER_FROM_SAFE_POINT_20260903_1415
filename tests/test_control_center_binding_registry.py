import pytest

from src.ui.control_center.binding_registry import (
    ScreenBinding,
    build_binding_registry,
    get_binding_for_screen,
    get_binding_registry,
    validate_binding_registry,
)
from src.ui.control_center.runtime_sources import get_runtime_source_registry


def test_binding_registry_has_seventeen_safe_screen_bindings():
    bindings = build_binding_registry()
    assert len(bindings) == 17
    assert validate_binding_registry(bindings)
    assert all(item.read_only and item.display_only for item in bindings)
    assert all(not getattr(item, flag) for item in bindings for flag in (
        "can_execute", "can_start_paper", "can_start_live", "can_call_network", "can_send_order"
    ))


def test_all_binding_sources_are_registered_runtime_sources():
    sources = set(get_runtime_source_registry())
    assert all(set(item.source_names) <= sources for item in build_binding_registry())
    assert len(get_binding_registry()) == 17
    assert get_binding_for_screen("01 Overview")["display_only"] is True


def test_unknown_source_fails_validation():
    binding = ScreenBinding("01 Overview", ("missing_source",), "2m", "5m", "UNKNOWN", "test")
    with pytest.raises(ValueError, match="UNKNOWN_RUNTIME_SOURCE"):
        validate_binding_registry((binding,) + build_binding_registry()[1:])


def test_binding_registry_contains_no_active_runtime_surface():
    for item in build_binding_registry():
        assert item.fallback_state in {"UNKNOWN", "OFF", "STALE", "BLOCKED", "READY"}
        assert item.can_execute is False
        assert item.can_send_order is False
