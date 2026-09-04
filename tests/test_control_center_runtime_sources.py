from src.ui.control_center.runtime_sources import (
    build_runtime_source_registry,
    get_runtime_source_registry,
    get_screen_source_map,
)


def test_registry_has_twelve_read_only_sources():
    registry = build_runtime_source_registry()
    assert len(registry) == 12
    assert len(get_runtime_source_registry()) == 12
    assert all(source.read_only for source in registry)
    assert all(not source.can_execute for source in registry)
    assert all(not source.can_start_paper for source in registry)
    assert all(not source.can_start_live for source in registry)
    assert all(not source.can_call_network for source in registry)
    assert all(not source.can_send_order for source in registry)


def test_registry_fallbacks_and_screen_map_are_complete():
    allowed = {"UNKNOWN", "OFF", "STALE", "BLOCKED"}
    assert all(source.fallback_state in allowed for source in build_runtime_source_registry())
    screen_map = get_screen_source_map()
    assert len(screen_map) == 17
    assert all(screen_map.values())
    registered = set(get_runtime_source_registry())
    assert all(set(sources) <= registered for sources in screen_map.values())


def test_registry_is_metadata_only_and_has_no_runtime_call_surface():
    registry = get_runtime_source_registry()
    assert all(set(source) == {
        "name", "provider", "refresh_cadence", "stale_threshold", "fallback_state",
        "blocking_rule", "read_only", "can_execute", "can_start_paper",
        "can_start_live", "can_call_network", "can_send_order",
    } for source in registry.values())
    assert all(source["read_only"] for source in registry.values())
