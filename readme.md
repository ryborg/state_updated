# State updated helper - Preview

![GitHub release (latest by date)](https://img.shields.io/github/v/release/kgn3400/state_updated)
![GitHub all releases](https://img.shields.io/github/downloads/kgn3400/state_updated/total)
![GitHub last commit](https://img.shields.io/github/last-commit/kgn3400/state_updated)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/kgn3400/state_updated)

The state updated integration helper allows you to create binary sensors which monitor another entity's __state__ or __state_attributes__. It exposes the new and old value for the monitored entity and are cleared after the user defined time period has expired.

For installation instructions [see this guide](https://hacs.xyz/docs/faq/custom_repositories).

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=state_updated)

## Configuration

Configuration is setup via UI in Home assistant.

| Field name | Mandatory/Optional | Description |
|------------|------------------|-------------|
| Name | Optional | Name. If empty, entity id name are used  |
| Entity id | Mandatory | Entity that this sensor tracks  |
| Attribute | Optional | Attribute of entity that this sensor tracks  |
| Icon | Mandatory | Icon used by entity  |
| Clear updates after | Mandatory | User defined time period indicating when to clear the entity  |
| Text template | Optional | Defines a template to create the text attribute. Value = new_value, old_value, entity_id, attribute and last_updated |

## Exposed state attributes

The state updated integration helper provides the following state attributes.

| Attribute | Description |
|-----------|-------------|
| new_value  | New state/state_attribute value |
| old_value  | Old state/state_attribute value |
| text  | Text generated from template |
| last_updated  | Last time the state/state_attribute was updated |

## Usage scenario

Using the Scrape integration for retrieving latest software version. By letting state_updated monitor the Scrape entity, a card can be built that only shows when there are changes and a content about what has changed.
