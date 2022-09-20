# HASS_wu_interceptor

Intercepts WU update packets and send them to a mqtt broker

WORK-IN-PROGRESS, this is  the basic script wich is running fine but i'm looking for run on Home Assistant as plugin.

Basically the script fire-up a python HTTP server and listen for the update queries originating from the weather station and directed to WeatherUnderground,
then split the data, perform some conversion (farenheit to celsius, low battery alert to number etc.);
send the data as mqtt message to a boker (home assistant).
