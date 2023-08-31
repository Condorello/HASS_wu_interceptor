#!/usr/bin/with-contenv bashio

export MQTT_BROKER_HOST=$(bashio::config 'mqtt_broker_host')
export MQTT_BROKER_PORT=$(bashio::config 'mqtt_broker_port')
export MQTT_USERNAME=$(bashio::config 'mqtt_username')
export MQTT_PASSWORD=$(bashio::config 'mqtt_password')

if bashio::var.has_value "$(bashio::services 'mqtt')"; then
    export MQTT_BROKER_HOST="$(bashio::services 'mqtt' 'host')"
    export MQTT_BROKER_PORT="$(bashio::services 'mqtt' 'port')"
    export MQTT_USERNAME="$(bashio::services 'mqtt' 'username')"
    export MQTT_PASSWORD="$(bashio::services 'mqtt' 'password')"
fi

echo "running pws server"

python3 /pws_server.py
