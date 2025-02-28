"""Motor speed support for Xiaomi Mi Air Humidifier."""
from __future__ import annotations

from dataclasses import dataclass, replace

from homeassistant.components.number import NumberEntity, NumberEntityDescription
from homeassistant.const import DEGREE, ENTITY_CATEGORY_CONFIG, TIME_MINUTES
from homeassistant.core import callback

from .const import (
    CONF_DEVICE,
    CONF_FLOW_TYPE,
    CONF_MODEL,
    DOMAIN,
    FEATURE_FLAGS_AIRFRESH,
    FEATURE_FLAGS_AIRHUMIDIFIER_CA4,
    FEATURE_FLAGS_AIRHUMIDIFIER_CA_AND_CB,
    FEATURE_FLAGS_AIRPURIFIER_2S,
    FEATURE_FLAGS_AIRPURIFIER_3C,
    FEATURE_FLAGS_AIRPURIFIER_MIIO,
    FEATURE_FLAGS_AIRPURIFIER_MIOT,
    FEATURE_FLAGS_AIRPURIFIER_PRO,
    FEATURE_FLAGS_AIRPURIFIER_PRO_V7,
    FEATURE_FLAGS_AIRPURIFIER_V1,
    FEATURE_FLAGS_AIRPURIFIER_V3,
    FEATURE_FLAGS_FAN,
    FEATURE_FLAGS_FAN_1C,
    FEATURE_FLAGS_FAN_P5,
    FEATURE_FLAGS_FAN_P9,
    FEATURE_FLAGS_FAN_P10_P11,
    FEATURE_FLAGS_FAN_ZA5,
    FEATURE_SET_DELAY_OFF_COUNTDOWN,
    FEATURE_SET_FAN_LEVEL,
    FEATURE_SET_FAVORITE_LEVEL,
    FEATURE_SET_FAVORITE_RPM,
    FEATURE_SET_LED_BRIGHTNESS,
    FEATURE_SET_LED_BRIGHTNESS_LEVEL,
    FEATURE_SET_MOTOR_SPEED,
    FEATURE_SET_OSCILLATION_ANGLE,
    FEATURE_SET_VOLUME,
    FEATURE_SET_BUZZER_VOLUME,
    KEY_COORDINATOR,
    KEY_DEVICE,
    MODEL_AIRFRESH_VA2,
    MODEL_AIRHUMIDIFIER_CA1,
    MODEL_AIRHUMIDIFIER_CA4,
    MODEL_AIRHUMIDIFIER_CB1,
    MODEL_AIRPURIFIER_2S,
    MODEL_AIRPURIFIER_3C,
    MODEL_AIRPURIFIER_PRO,
    MODEL_AIRPURIFIER_PRO_V7,
    MODEL_AIRPURIFIER_V1,
    MODEL_AIRPURIFIER_V3,
    MODEL_FAN_1C,
    MODEL_FAN_P5,
    MODEL_FAN_P9,
    MODEL_FAN_P10,
    MODEL_FAN_P11,
    MODEL_FAN_SA1,
    MODEL_FAN_V2,
    MODEL_FAN_V3,
    MODEL_FAN_ZA1,
    MODEL_FAN_ZA3,
    MODEL_FAN_ZA4,
    MODEL_FAN_ZA5,
    MODELS_PURIFIER_MIIO,
    MODELS_PURIFIER_MIOT,
)
from .device import XiaomiCoordinatedMiioEntity

ATTR_DELAY_OFF_COUNTDOWN = "delay_off_countdown"
ATTR_FAN_LEVEL = "fan_level"
ATTR_FAVORITE_LEVEL = "favorite_level"
ATTR_FAVORITE_RPM = "favorite_rpm"
ATTR_LED_BRIGHTNESS = "led_brightness"
ATTR_LED_BRIGHTNESS_LEVEL = "led_brightness_level"
ATTR_MOTOR_SPEED = "motor_speed"
ATTR_OSCILLATION_ANGLE = "angle"
ATTR_VOLUME = "volume"
ATTR_BUZZER_VOLUME = "buzzer_volume"


@dataclass
class XiaomiMiioNumberDescription(NumberEntityDescription):
    """A class that describes number entities."""

    min_value: float | None = None
    max_value: float | None = None
    step: float | None = None
    available_with_device_off: bool = True
    method: str | None = None


@dataclass
class OscillationAngleValues:
    """A class that describes oscillation angle values."""

    max_value: float | None = None
    min_value: float | None = None
    step: float | None = None


SET_VOLUME_NUMBER_DESCRIPTION = XiaomiMiioNumberDescription(
    key=ATTR_VOLUME,
    name="Volume",
    icon="mdi:volume-high",
    min_value=0,
    max_value=100,
    step=1,
    method="async_set_volume",
    entity_category=ENTITY_CATEGORY_CONFIG,
)



NUMBER_TYPES = {
    FEATURE_SET_MOTOR_SPEED: XiaomiMiioNumberDescription(
        key=ATTR_MOTOR_SPEED,
        name="Motor Speed",
        icon="mdi:fast-forward-outline",
        unit_of_measurement="rpm",
        min_value=200,
        max_value=2000,
        step=10,
        available_with_device_off=False,
        method="async_set_motor_speed",
        entity_category=ENTITY_CATEGORY_CONFIG,
    ),
    FEATURE_SET_FAVORITE_LEVEL: XiaomiMiioNumberDescription(
        key=ATTR_FAVORITE_LEVEL,
        name="Favorite Level",
        icon="mdi:star-cog",
        min_value=0,
        max_value=17,
        step=1,
        method="async_set_favorite_level",
        entity_category=ENTITY_CATEGORY_CONFIG,
    ),
    FEATURE_SET_FAN_LEVEL: XiaomiMiioNumberDescription(
        key=ATTR_FAN_LEVEL,
        name="Fan Level",
        icon="mdi:fan",
        min_value=1,
        max_value=3,
        step=1,
        method="async_set_fan_level",
        entity_category=ENTITY_CATEGORY_CONFIG,
    ),
    FEATURE_SET_VOLUME: SET_VOLUME_NUMBER_DESCRIPTION,
    FEATURE_SET_BUZZER_VOLUME: replace(
        SET_VOLUME_NUMBER_DESCRIPTION,
        key=ATTR_BUZZER_VOLUME,
    ),
    FEATURE_SET_OSCILLATION_ANGLE: XiaomiMiioNumberDescription(
        key=ATTR_OSCILLATION_ANGLE,
        name="Oscillation Angle",
        icon="mdi:angle-acute",
        unit_of_measurement=DEGREE,
        min_value=1,
        max_value=120,
        step=1,
        method="async_set_oscillation_angle",
        entity_category=ENTITY_CATEGORY_CONFIG,
    ),
    FEATURE_SET_DELAY_OFF_COUNTDOWN: XiaomiMiioNumberDescription(
        key=ATTR_DELAY_OFF_COUNTDOWN,
        name="Delay Off Countdown",
        icon="mdi:fan-off",
        unit_of_measurement=TIME_MINUTES,
        min_value=0,
        max_value=480,
        step=1,
        method="async_set_delay_off_countdown",
        entity_category=ENTITY_CATEGORY_CONFIG,
    ),
    FEATURE_SET_LED_BRIGHTNESS: XiaomiMiioNumberDescription(
        key=ATTR_LED_BRIGHTNESS,
        name="Led Brightness",
        icon="mdi:brightness-6",
        min_value=0,
        max_value=100,
        step=1,
        method="async_set_led_brightness",
        entity_category=ENTITY_CATEGORY_CONFIG,
    ),
    FEATURE_SET_LED_BRIGHTNESS_LEVEL: XiaomiMiioNumberDescription(
        key=ATTR_LED_BRIGHTNESS_LEVEL,
        name="Led Brightness",
        icon="mdi:brightness-6",
        min_value=0,
        max_value=8,
        step=1,
        method="async_set_led_brightness_level",
        entity_category=ENTITY_CATEGORY_CONFIG,
    ),
    FEATURE_SET_FAVORITE_RPM: XiaomiMiioNumberDescription(
        key=ATTR_FAVORITE_RPM,
        name="Favorite Motor Speed",
        icon="mdi:star-cog",
        unit_of_measurement="rpm",
        min_value=300,
        max_value=2200,
        step=10,
        method="async_set_favorite_rpm",
        entity_category=ENTITY_CATEGORY_CONFIG,
    ),
}

MODEL_TO_FEATURES_MAP = {
    MODEL_AIRFRESH_VA2: FEATURE_FLAGS_AIRFRESH,
    MODEL_AIRHUMIDIFIER_CA1: FEATURE_FLAGS_AIRHUMIDIFIER_CA_AND_CB,
    MODEL_AIRHUMIDIFIER_CA4: FEATURE_FLAGS_AIRHUMIDIFIER_CA4,
    MODEL_AIRHUMIDIFIER_CB1: FEATURE_FLAGS_AIRHUMIDIFIER_CA_AND_CB,
    MODEL_AIRPURIFIER_2S: FEATURE_FLAGS_AIRPURIFIER_2S,
    MODEL_AIRPURIFIER_3C: FEATURE_FLAGS_AIRPURIFIER_3C,
    MODEL_AIRPURIFIER_PRO: FEATURE_FLAGS_AIRPURIFIER_PRO,
    MODEL_AIRPURIFIER_PRO_V7: FEATURE_FLAGS_AIRPURIFIER_PRO_V7,
    MODEL_AIRPURIFIER_V1: FEATURE_FLAGS_AIRPURIFIER_V1,
    MODEL_AIRPURIFIER_V3: FEATURE_FLAGS_AIRPURIFIER_V3,
    MODEL_FAN_1C: FEATURE_FLAGS_FAN_1C,
    MODEL_FAN_P10: FEATURE_FLAGS_FAN_P10_P11,
    MODEL_FAN_P11: FEATURE_FLAGS_FAN_P10_P11,
    MODEL_FAN_P5: FEATURE_FLAGS_FAN_P5,
    MODEL_FAN_P9: FEATURE_FLAGS_FAN_P9,
    MODEL_FAN_SA1: FEATURE_FLAGS_FAN,
    MODEL_FAN_V2: FEATURE_FLAGS_FAN,
    MODEL_FAN_V3: FEATURE_FLAGS_FAN,
    MODEL_FAN_ZA1: FEATURE_FLAGS_FAN,
    MODEL_FAN_ZA3: FEATURE_FLAGS_FAN,
    MODEL_FAN_ZA4: FEATURE_FLAGS_FAN,
    MODEL_FAN_ZA5: FEATURE_FLAGS_FAN_ZA5,
}

OSCILLATION_ANGLE_VALUES = {
    MODEL_FAN_P5: OscillationAngleValues(max_value=140, min_value=30, step=30),
    MODEL_FAN_ZA5: OscillationAngleValues(max_value=120, min_value=30, step=30),
    MODEL_FAN_P9: OscillationAngleValues(max_value=150, min_value=30, step=30),
    MODEL_FAN_P10: OscillationAngleValues(max_value=140, min_value=30, step=30),
    MODEL_FAN_P11: OscillationAngleValues(max_value=140, min_value=30, step=30),
}


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Selectors from a config entry."""
    entities = []
    if not config_entry.data[CONF_FLOW_TYPE] == CONF_DEVICE:
        return
    model = config_entry.data[CONF_MODEL]
    device = hass.data[DOMAIN][config_entry.entry_id][KEY_DEVICE]

    if model in MODEL_TO_FEATURES_MAP:
        features = MODEL_TO_FEATURES_MAP[model]
    elif model in MODELS_PURIFIER_MIIO:
        features = FEATURE_FLAGS_AIRPURIFIER_MIIO
    elif model in MODELS_PURIFIER_MIOT:
        features = FEATURE_FLAGS_AIRPURIFIER_MIOT
    else:
        return

    for feature, description in NUMBER_TYPES.items():
        if feature & features:
            if (
                description.key == ATTR_OSCILLATION_ANGLE
                and model in OSCILLATION_ANGLE_VALUES
            ):
                description.max_value = OSCILLATION_ANGLE_VALUES[model].max_value
                description.min_value = OSCILLATION_ANGLE_VALUES[model].min_value
                description.step = OSCILLATION_ANGLE_VALUES[model].step

            entities.append(
                XiaomiNumberEntity(
                    f"{config_entry.title} {description.name}",
                    device,
                    config_entry,
                    f"{description.key}_{config_entry.unique_id}",
                    hass.data[DOMAIN][config_entry.entry_id][KEY_COORDINATOR],
                    description,
                )
            )

    async_add_entities(entities)


class XiaomiNumberEntity(XiaomiCoordinatedMiioEntity, NumberEntity):
    """Representation of a generic Xiaomi attribute selector."""

    def __init__(self, name, device, entry, unique_id, coordinator, description):
        """Initialize the generic Xiaomi attribute selector."""
        super().__init__(name, device, entry, unique_id, coordinator)

        self._attr_min_value = description.min_value
        self._attr_max_value = description.max_value
        self._attr_step = description.step
        self._attr_value = self._extract_value_from_attribute(
            coordinator.data, description.key
        )
        self.entity_description = description

    @property
    def available(self):
        """Return the number controller availability."""
        if (
            super().available
            and not self.coordinator.data.is_on
            and not self.entity_description.available_with_device_off
        ):
            return False
        return super().available

    async def async_set_value(self, value):
        """Set an option of the miio device."""
        method = getattr(self, self.entity_description.method)
        if await method(int(value)):
            self._attr_value = value
            self.async_write_ha_state()

    @callback
    def _handle_coordinator_update(self):
        """Fetch state from the device."""
        # On state change the device doesn't provide the new state immediately.
        self._attr_value = self._extract_value_from_attribute(
            self.coordinator.data, self.entity_description.key
        )
        self.async_write_ha_state()

    async def async_set_motor_speed(self, motor_speed: int = 400) -> bool:
        """Set the target motor speed."""
        return await self._try_command(
            "Setting the target motor speed of the miio device failed.",
            self._device.set_speed,
            motor_speed,
        )

    async def async_set_favorite_level(self, level: int = 1) -> bool:
        """Set the favorite level."""
        return await self._try_command(
            "Setting the favorite level of the miio device failed.",
            self._device.set_favorite_level,
            level,
        )

    async def async_set_fan_level(self, level: int = 1) -> bool:
        """Set the fan level."""
        return await self._try_command(
            "Setting the favorite level of the miio device failed.",
            self._device.set_fan_level,
            level,
        )

    async def async_set_volume(self, volume: int = 50) -> bool:
        """Set the volume."""
        return await self._try_command(
            "Setting the volume of the miio device failed.",
            self._device.set_volume,
            volume,
        )

    async def async_set_oscillation_angle(self, angle: int) -> bool:
        """Set the volume."""
        return await self._try_command(
            "Setting angle of the miio device failed.", self._device.set_angle, angle
        )

    async def async_set_delay_off_countdown(self, delay_off_countdown: int) -> bool:
        """Set the delay off countdown."""
        return await self._try_command(
            "Setting delay off miio device failed.",
            self._device.delay_off,
            delay_off_countdown * 60,
        )

    async def async_set_led_brightness_level(self, level: int):
        """Set the led brightness level."""
        return await self._try_command(
            "Setting the led brightness level of the miio device failed.",
            self._device.set_led_brightness_level,
            level,
        )

    async def async_set_led_brightness(self, level: int):
        """Set the led brightness level."""
        return await self._try_command(
            "Setting the led brightness level of the miio device failed.",
            self._device.set_led_brightness,
            level,
        )

    async def async_set_favorite_rpm(self, rpm: int):
        """Set the target motor speed."""
        return await self._try_command(
            "Setting the favorite rpm of the miio device failed.",
            self._device.set_favorite_rpm,
            rpm,
        )
