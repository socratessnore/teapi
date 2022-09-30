#!/usr/bin/env bashio

bashio::log.info "Fetching data from TE API"

MQTT_IP=$(bashio::config 'mqtt_ip')
MQTT_USERNAME=$(bashio::config 'mqtt_username')
MQTT_PASSWORD=$(bashio::config 'mqtt_password')
TEAPI_USERNAME=$(bashio::config 'teapi_username')
TEAPI_PASSWORD=$(bashio::config 'teapi_password')

bashio::log.info "MQTT IP VALUE"
bashio::log.info ${MQTT_IP}

python3 /workdir/main.py ${MQTT_IP} ${MQTT_USERNAME} ${MQTT_PASSWORD} ${TEAPI_USERNAME} ${TEAPI_PASSWORD}