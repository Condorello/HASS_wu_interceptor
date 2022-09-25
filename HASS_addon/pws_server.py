#!/usr/bin/env python3
import http.server
import socketserver
import paho.mqtt.client as mqtt
from urllib.parse import urlparse
from urllib.parse import parse_qs

#WEBSERVER PORT
WEBSERVER_PORT = 8087

# MQTT Client configuration

MQTT_BROKER_HOST  = 'xxx.xxx.xxx.xxx' ## MQTT BROKER
MQTT_BROKER_PORT  = 1883
MQTT_CLIENT_ID    = "weatherstation"
MQTT_TOPIC_PREFIX = "homeassistant"
MQTT_TOPIC = MQTT_TOPIC_PREFIX + "/weatherstation"
MQTT_USERNAME = "mqttuser"  ### MQTT BROKER USERNAME
MQTT_PASSWORD = "mqttpassword"  ### MQTT BROKER PASSWORD

# mostly copied + pasted from https://www.emqx.io/blog/how-to-use-mqtt-in-python and some of my own MQTT scripts
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"connected to MQTT broker at {MQTT_BROKER_HOST}")
    else:
        print("Failed to connect, return code %d\n", rc)
def on_disconnect(client, userdata, flags, rc):
    print("disconnected from MQTT broker")
# set up mqtt client
client = mqtt.Client(client_id=MQTT_CLIENT_ID)
if MQTT_USERNAME and MQTT_PASSWORD:
    client.username_pw_set(MQTT_USERNAME,MQTT_PASSWORD)
    print("Username and password set.")
client.will_set(MQTT_TOPIC_PREFIX+"/status", payload="Offline", qos=1, retain=True) # set LWT
client.on_connect = on_connect # on connect callback
client.on_disconnect = on_disconnect # on disconnect callback
# connect to broker
client.connect(MQTT_BROKER_HOST, port=MQTT_BROKER_PORT, keepalive=60)
client.loop_start()
def publish(client, topic, msg):
    result = client.publish(topic, msg)
    # result: [0, 1]
    status = result[0]
    # uncomment for debug. don't need all the success messages.
    if status == 0:
        #print(f"Sent {msg} to topic {topic}")
        pass
    else:
        print(f"Failed to send message to topic {topic}")


# HTTP SERVER
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def parse_wu_data(query_components):
        data_array = {}
        if 'tempf' in query_components:
            temp_out = round( (float(query_components["tempf"][0])-32) * 5/9)
            data_array['Temperature_out_[C]'] = temp_out
        if 'humidity' in query_components:
            humidity_out = int(query_components["humidity"][0])
            data_array['Humidity_out_[%]'] = humidity_out
        if 'dewptf' in query_components:
            dew_point = round((float(query_components["dewptf"][0])-32) * 5/9)
            data_array['Dew_point_[C]'] = dew_point
        if 'winddir' in query_components:
            wind_dir = int(query_components["winddir"][0])
            data_array['Wind_direction_[degree]'] = wind_dir
        if 'windspeedmph' in query_components:
            wind_speed = round((float(query_components["windspeedmph"][0])*1.609344))
            data_array['Wind_speed_[km/h]'] = wind_speed
        if 'windgustmph' in query_components:
            wind_gust_speed = round((float(query_components["windgustmph"][0])*1.609344))
            data_array['Wind_gust_speed_[km/h]'] = wind_gust_speed
        if 'rainin' in query_components:
            rain_rate_in = float(query_components["rainin"][0])
            data_array['Rain_rate_[]'] = rain_rate_in
        if 'dailyrainin' in query_components:
            rain_daily_in = float(query_components["dailyrainin"][0])
            data_array['Rain_daily_[]'] = rain_daily_in
        if 'weeklyrainin' in query_components:
            rain_weekly_in = float(query_components["weeklyrainin"][0])
            data_array['Rain_weekly_[]'] = rain_weekly_in
        if 'monthlyrainin' in query_components:
            rain_monthly_in = float(query_components["monthlyrainin"][0])
            data_array['Rain_monthly_[]'] = rain_monthly_in
        if 'yearlyrainin' in query_components:
            rain_yearly_in = float(query_components["yearlyrainin"][0])
            data_array['Rain_yearly_[]'] = rain_yearly_in
        if 'solarradiation' in query_components:
            solar_radiation = float(query_components["solarradiation"][0])
            data_array['Solar_radiation_[W/m^2]'] = solar_radiation
        if 'UV' in query_components:
            uv_radiation = float(query_components["UV"][0])
            data_array['UV_[index]'] = uv_radiation
        if 'indoortempf' in query_components:
            temp_in = round( (float(query_components["indoortempf"][0])-32) * 5/9)
            data_array['Temperature_in_[C]'] = temp_in
        if 'indoorhumidity' in query_components:
            humidity_in = int(query_components["indoorhumidity"][0])
            data_array['Humidity_in_[%]'] = humidity_in
        if 'baromin' in query_components:
            barometric_pressure = round((float(query_components["baromin"][0])*33.86389))
            data_array['Barometric_pressure_[hpa]'] = barometric_pressure
        if 'lowbatt' in query_components:
            low_battery = int(query_components["lowbatt"][0])
            if low_battery == 0: ##return battery 100% for home assistant 
                data_array['Low_battery_[]'] = 100
            else: ##return battery 0% for home assistant
                data_array['Low_battery_[]'] = 0
        return data_array


    def do_GET(self):
        # Sending an '200 OK' response
        self.send_response(200)
        # Setting the header
        self.send_header("Content-type", "text/html")
        # Whenever using 'send_header', you also have to call 'end_headers'
        self.end_headers()
        # Extract query param
        query_components = parse_qs(urlparse(self.path).query)
        # Get data from function parse_wu_data and publish over http
        http_message = MyHttpRequestHandler.parse_wu_data(query_components)
        http_message = str(http_message).replace("'", '\"')
        html = f"<html><head></head><body><h1>{http_message}</h1></body></html>"
        #Get data from function parse_wu_data and publish over mqtt
        publish(client, MQTT_TOPIC + "/temperature_out", (MyHttpRequestHandler.parse_wu_data(query_components)['Temperature_out_[C]']) )
        publish(client, MQTT_TOPIC + "/humidity_out", (MyHttpRequestHandler.parse_wu_data(query_components)['Humidity_out_[%]']) )
        publish(client, MQTT_TOPIC + "/dewpoint", (MyHttpRequestHandler.parse_wu_data(query_components)['Dew_point_[C]']) )
        publish(client, MQTT_TOPIC + "/wind_direction", (MyHttpRequestHandler.parse_wu_data(query_components)['Wind_direction_[degree]']) )
        publish(client, MQTT_TOPIC + "/wind_speed", (MyHttpRequestHandler.parse_wu_data(query_components)['Wind_speed_[km/h]']) )
        publish(client, MQTT_TOPIC + "/wind_gust_speed", (MyHttpRequestHandler.parse_wu_data(query_components)['Wind_gust_speed_[km/h]']) )
        publish(client, MQTT_TOPIC + "/rain_rate", (MyHttpRequestHandler.parse_wu_data(query_components)['Rain_rate_[]']) )
        publish(client, MQTT_TOPIC + "/rain_daily", (MyHttpRequestHandler.parse_wu_data(query_components)['Rain_daily_[]']) )
        publish(client, MQTT_TOPIC + "/rain_weekly", (MyHttpRequestHandler.parse_wu_data(query_components)['Rain_weekly_[]']) )
        publish(client, MQTT_TOPIC + "/rain_monthly", (MyHttpRequestHandler.parse_wu_data(query_components)['Rain_monthly_[]']) )
        publish(client, MQTT_TOPIC + "/rain_yearly", (MyHttpRequestHandler.parse_wu_data(query_components)['Rain_yearly_[]']) )
        publish(client, MQTT_TOPIC + "/solar_radiation", (MyHttpRequestHandler.parse_wu_data(query_components)['Solar_radiation_[W/m^2]']) )
        publish(client, MQTT_TOPIC + "/uv_index", (MyHttpRequestHandler.parse_wu_data(query_components)['UV_[index]']) )
        publish(client, MQTT_TOPIC + "/temperature_in", (MyHttpRequestHandler.parse_wu_data(query_components)['Temperature_in_[C]']) )
        publish(client, MQTT_TOPIC + "/humidity_in", (MyHttpRequestHandler.parse_wu_data(query_components)['Humidity_in_[%]']) )
        publish(client, MQTT_TOPIC + "/barometric_pressure", (MyHttpRequestHandler.parse_wu_data(query_components)['Barometric_pressure_[hpa]']) )
        publish(client, MQTT_TOPIC + "/low_battery", (MyHttpRequestHandler.parse_wu_data(query_components)['Low_battery_[]']) )

        # Writing the HTML contents with UTF-8
        self.wfile.write(bytes(html, "utf8"))

        return

# Create an object of the above class
handler_object = MyHttpRequestHandler

my_server = socketserver.TCPServer(("", WEBSERVER_PORT), handler_object)

# Star the server
my_server.serve_forever()
