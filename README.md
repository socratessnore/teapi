# teapi
Home Assistant TE API add on

## Installation

Requires MQTT Broker (eg. Mosquito Broker) and MQTT integration for Home Assistant

1. Install and setup Mosquito Broker from Home Assistant add-ons
2. Install and setup MQTT from Home assistant integrations

		Create a new Home Assistant user for MQTT use or you can use any local Home Assistant user you like.

3. Install TEAPI as a local Add-on

		Instructions:
		https://developers.home-assistant.io/docs/add-ons/tutorial#step-2-installing-and-testing-your-add-on

4. Set TEAPI config values from Configuration tab
		
		Crontab schedule can not be currently changed from the UI (WIP). It's hardcoded to run at 05:00. Make changes to crontab file and rebuild if required.
		
## Known issues

- Turku Energia API does not always update right after midnight correctly but shows very low values. Likely first hour consumption from the last day. Sometimes
yesterdays full consumption value comes available very late next day or not at all. Not sure what causes this but something on Turku Energia's end.
- There is not any manual trigger to fetch latest value. Currently it causes some hassle if you want to update the value during the day (for example first bulletins problem happens)