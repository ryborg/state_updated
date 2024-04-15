"""Support for State updated."""

from __future__ import annotations

from datetime import timedelta

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_ATTRIBUTE,
    CONF_ENTITY_ID,
    CONF_ICON,
    STATE_UNAVAILABLE,
    STATE_UNKNOWN,
)
from homeassistant.core import Event, HomeAssistant, ServiceCall, callback
from homeassistant.helpers import entity_platform

# entity_registry as er,
# icon,
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import (
    EventStateChangedData,
    async_track_state_change_event,
)
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .component_api import ComponentApi
from .const import (
    CONF_LAST_UPDATED,
    CONF_NEW_VALUE,
    CONF_OLD_VALUE,
    DOMAIN,
    LOGGER,
    TRANSLATION_KEY,
)


# ------------------------------------------------------
async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Entry for State updated setup."""

    async_add_entities([StateUpdatedBinarySensor(hass, entry)])


# ------------------------------------------------------
# ------------------------------------------------------
class StateUpdatedBinarySensor(BinarySensorEntity):
    """Sensor class for State updated."""

    entity_list: list[ComponentApi] = []

    # ------------------------------------------------------
    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
    ) -> None:
        """Binary sensor."""

        self.entry: ConfigEntry = entry
        self.hass = hass

        self.translation_key = TRANSLATION_KEY
        self.component_api: ComponentApi = ComponentApi(self.hass, self.entry)

        self.coordinator: DataUpdateCoordinator = DataUpdateCoordinator(
            self.hass,
            LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=1),
            update_method=self.component_api.async_update,
        )
        self.component_api.coordinator = self.coordinator

        platform = entity_platform.async_get_current_platform()
        platform.async_register_entity_service(
            "reset_entity",
            {},
            "async_reset_entity",
        )

        self.hass.services.async_register(
            DOMAIN, "reset_all", self.async_reset_all_service
        )

    # ------------------------------------------------------
    async def async_reset_entity(self) -> None:
        """SReset entity."""
        await self.component_api.async_reset()

    # ------------------------------------------------------------------
    async def async_reset_all_service(self, call: ServiceCall) -> None:
        """Reset all service."""

        for entity in StateUpdatedBinarySensor.entity_list:
            await entity.async_reset()

    # ------------------------------------------------------
    async def async_will_remove_from_hass(self) -> None:
        """When removed from hass."""
        StateUpdatedBinarySensor.entity_list.remove(self.component_api)

    # ------------------------------------------------------
    async def async_added_to_hass(self) -> None:
        """Complete device setup after being added to hass."""

        # ------------------------------------------------------
        @callback
        def sensor_state_listener(
            event: Event[EventStateChangedData],
        ) -> None:
            """Handle state changes on the observed device."""
            if (tmp_state := event.data["new_state"]) is None:
                return
            try:
                if CONF_ATTRIBUTE in self.entry.options:
                    new_value = tmp_state.attributes.get(
                        self.entry.options[CONF_ATTRIBUTE]
                    )
                else:
                    new_value = tmp_state.state

                if new_value not in (STATE_UNKNOWN, STATE_UNAVAILABLE):
                    old_value = STATE_UNKNOWN

                    if (tmp_state := event.data["old_state"]) is not None:
                        if CONF_ATTRIBUTE in self.entry.options:
                            old_value = tmp_state.attributes.get(
                                self.entry.options[CONF_ATTRIBUTE]
                            )
                        else:
                            old_value = tmp_state.state

                    self.component_api.update_state(new_value, old_value)
                    self.async_schedule_update_ha_state(True)
            except (ValueError, TypeError) as ex:
                LOGGER.error(ex)

        await super().async_added_to_hass()

        await self.coordinator.async_config_entry_first_refresh()

        # icons = await icon.async_get_icons(
        #     self.hass, "entity", integrations=["temperature"]
        # )

        StateUpdatedBinarySensor.entity_list.append(self.component_api)

        self.entry.async_on_unload(self.entry.add_update_listener(self.update_listener))

        self.async_on_remove(
            async_track_state_change_event(
                self.hass,
                self.entry.options[CONF_ENTITY_ID],
                sensor_state_listener,
            )
        )
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    # ------------------------------------------------------
    async def update_listener(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
    ) -> None:
        """Reload on config entry update."""
        # await hass.config_entries.async_reload(entry.entry_id)
        await self.component_api.async_config_entry_refresh()

    # ------------------------------------------------------
    @property
    def name(self) -> str:
        """Name.

        Returns:
            str: Name of sensor

        """
        return self.entry.title

    # ------------------------------------------------------
    @property
    def unique_id(self) -> str:
        """Unique id.

        Returns:
            str: Unique id

        """

        return self.entry.entry_id

    # ------------------------------------------------------
    @property
    def icon(self) -> str:
        """Icon.

        Returns:
            str: Icon name

        """

        # entity_registry = er.async_get(self.hass)
        # device_registry = dr.async_get(self.hass)
        # source_entity = entity_registry.async_get(
        #     self.entry.options.get(CONF_ENTITY_ID, "")
        # )

        # if (
        #     (source_entity is not None)
        #     and (source_entity.device_id is not None)
        #     and (
        #         (
        #             device := device_registry.async_get(
        #                 device_id=source_entity.device_id,
        #             )
        #         )
        #         is not None
        #     )
        # ):
        #     tmp_config = self.hass.config_entries.async_get_entry(
        #         source_entity.config_entry_id
        #     )

        # state = self.hass.states.get(self.entry.options.get(CONF_ENTITY_ID, ""))

        # if state is not None:
        #     icon = state.attributes.get(ATTR_ICON)

        if self.entry.options.get(CONF_ICON, "").strip() != "":
            return self.entry.options.get(CONF_ICON, "mdi:state-machine")

        return None

    # ------------------------------------------------------
    @property
    def is_on(self) -> bool:
        """Get the state."""

        return self.component_api.updated

    # ------------------------------------------------------
    @property
    def extra_state_attributes(self) -> dict:
        """Extra state attributes.

        Returns:
            dict: _description_

        """

        return {
            CONF_NEW_VALUE: self.component_api.new_value,
            CONF_OLD_VALUE: self.component_api.old_value,
            CONF_LAST_UPDATED: self.component_api.last_updated.isoformat(),
            "text": self.component_api.text,
        }

    # ------------------------------------------------------
    @property
    def should_poll(self) -> bool:
        """No need to poll. Coordinator notifies entity of updates."""
        return False

    # ------------------------------------------------------
    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success

    # ------------------------------------------------------
    async def async_update(self) -> None:
        """Update the entity. Only used by the generic entity update service."""
        await self.coordinator.async_request_refresh()
