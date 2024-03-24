"""Constants for State updated integration."""
from logging import Logger, getLogger

DOMAIN = "state_updated"
DOMAIN_NAME = "State updated"
LOGGER: Logger = getLogger(__name__)

CONF_CLEAR_UPDATES_AFTER_HOURS: str = "clear_update_after_hours"
CONF_NEW_VALUE: str = "new_value"
CONF_OLD_VALUE: str = "old_value"
CONF_LAST_UPDATED: str = "last_updated"
CONF_UPDATED: str = "updated"
CONF_TEXT_TEMPLATE: str = "text_template"

CONF_DEFAULT_TEXT_TEMPLATE: str = "default.text_template"
