"""Helpers for parsing BESTIN device status payloads."""

from __future__ import annotations

from typing import Any

from homeassistant.components.climate.const import (
    ATTR_HVAC_MODE,
    ATTR_CURRENT_TEMPERATURE,
    ATTR_PRESET_MODE,
    ATTR_PRESET_MODES,
    SERVICE_SET_TEMPERATURE,
    HVACMode,
)
from homeassistant.const import ATTR_STATE, WIND_SPEED

from .const import PRESET_NONE, PRESET_NV, SPEED_STR_LOW, SPEED_STR_MEDIUM, SPEED_STR_HIGH


def parse_thermostat_status(unit_status: str) -> dict[str, Any]:
    """Parse thermostat status from a string payload."""
    status_parts = unit_status.split("/")
    return {
        ATTR_HVAC_MODE: HVACMode.HEAT if status_parts[0] == "on" else HVACMode.OFF,
        SERVICE_SET_TEMPERATURE: float(status_parts[1]),
        ATTR_CURRENT_TEMPERATURE: float(status_parts[2]),
    }


def parse_temper_status(unit_status: str) -> dict[str, Any]:
    """Parse temperature status from a string payload."""
    return parse_thermostat_status(unit_status)


def parse_ventil_status(unit_status: str) -> dict[str, Any]:
    """Parse ventilation status from a string payload."""
    is_off = unit_status == "off"
    speed_list = [SPEED_STR_LOW, SPEED_STR_MEDIUM, SPEED_STR_HIGH]
    return {
        ATTR_STATE: not is_off,
        WIND_SPEED: unit_status if not is_off else "off",
        "speed_list": speed_list,
        ATTR_PRESET_MODE: None,
        ATTR_PRESET_MODES: [PRESET_NV, PRESET_NONE],
    }
