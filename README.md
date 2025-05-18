# HASS_wu_interceptor

Intercepts WU update packets and send them to an mqtt broker

WORK-IN-PROGRESS, this is  the basic script which is running fine but i'm looking for it run on Home Assistant OS as plugin.

Basically the script fire-up a python HTTP server and listen for the update queries originating from the weather station and directed to WeatherUnderground,
then split the data, perform some conversion (farenheit to celsius, low battery alert to number etc.);
send the data as mqtt message to a boker (home assistant).

Its need to forward packet originated from the station on port 80 tcp to the server where the script is running (same port for now).



### UPDATE

added a basic hassio addon. You have to copy the folder in the addon directory, change MQTT BROKER IP, USERNAME, PASSWORD in pws.py and then install the plugin.
