# State updated helper - Preview

![GitHub release (latest by date)](https://img.shields.io/github/v/release/kgn3400/state_updated)
![GitHub all releases](https://img.shields.io/github/downloads/kgn3400/state_updated/total)
![GitHub last commit](https://img.shields.io/github/last-commit/kgn3400/state_updated)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/kgn3400/state_updated)

The state updated integration helper allows you to create binary sensors which monitor another entitys __state__ or __state_attributes__. It exposes the new and old value for the monitored entity and are cleared after the user defined time period has expired.

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=state_updated)

## Exposed state attributes

| Attribute | Description |
|-----------|-------------|
| new_state  | New state/state_attribute value |
| old_state  | Old state/state_attribute value |
| text  | Text generated from template |
| last_updated  | Last time the state/state_attribute was updated |
