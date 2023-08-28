#!/usr/bin/with-contenv bashio

MQTT_BROKER_HOST=$(bashio::config 'mqtt_broker_host')
export MQTT_BROKER_HOST

MQTT_BROKER_PORT=$(bashio::config 'mqtt_broker_port')
export MQTT_BROKER_PORT

MQTT_USERNAME=$(bashio::config 'mqtt_username')
export MQTT_USERNAME

MQTT_PASSWORD=$(bashio::config 'mqtt_password')
export MQTT_PASSWORD

echo "running pws server"

python3 /pws_server.py
