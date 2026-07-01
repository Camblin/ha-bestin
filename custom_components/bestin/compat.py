"""Compatibility helpers for Home Assistant version differences."""

from __future__ import annotations

from typing import Any


def get_color_mode_constants(light_module: Any | None = None) -> tuple[Any, Any]:
    """Return color mode constants across Home Assistant versions."""
    if light_module is None:
        from homeassistant.components import light as light_module

    try:
        return (
            light_module.COLOR_MODE_BRIGHTNESS,
            light_module.COLOR_MODE_COLOR_TEMP,
        )
    except AttributeError:
        pass

    try:
        from homeassistant.components.light import ColorMode
    except Exception:  # pragma: no cover - fallback for very old/new versions
        return "brightness", "color_temp"

    def _cm_get(name: str, default: str) -> Any:
        member = getattr(ColorMode, name, None)
        if hasattr(member, "value"):
            return member.value
        return member or default

    return _cm_get("BRIGHTNESS", "brightness"), _cm_get("COLOR_TEMP", "color_temp")
