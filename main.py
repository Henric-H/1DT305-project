#importing all I need in this program.
import dht
import machine
from machine import Pin, I2C
import network
import esp32
import time
from umqtt.simple import MQTTClient
import re
import utime

# Library for BME280 found at: https://github.com/RuiSantosdotme/ESP-MicroPython/blob/master/code/WiFi/HTTP_Client_IFTTT_BME280/BME280.py
import BME280


# I2C Pin assignment
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=10000)

# Put your network stuff here.
ESSID = 'alfaEspritos'
Password = 'MagiskSkalbaggeUnderPappasKaktus'

# Put ThingSpeak stuff here.
ThingSpeak_API_Key = "VPLHSBH88T0LCFRT"
ThingSpeak_Channel_ID = "1080128"
MQTT_SERVER = "mqtt.thingspeak.com"

# Set up MQTT clent
MQTT_client = MQTTClient("umqtt_client", MQTT_SERVER)
    
# Create Topic for MQTT
MQTT_topic = "channels/{0}/publish/{1}".format(ThingSpeak_Channel_ID, ThingSpeak_API_Key)



# This is the thing that runs the other stuff cause it's main...
def main():

    # check if the device woke from a deep sleep
    if machine.reset_cause() == machine.DEEPSLEEP_RESET:
        print('woke from a deep sleep')

    print('Activate all systems')

    temp_DGT11, hum_DGT11 = get_data_DGT11(4)
    
    temp_BME280, hum_BME280, pres_BME280 = get_data_BME280()
    
    temp_core = get_data_ESP32()
    
    # Enable Network and Send Data then turn it off
    send_data(temp_DGT11, hum_DGT11, temp_core, temp_BME280, hum_BME280, pres_BME280)
    
    # Going to sleep for a couple of minutes
    print('Going to sleep')
    #time.sleep(240)
    machine.deepsleep(240000)



# This Function gets a pin id and return with the temperature and humidity from a DHT11 sensor
def get_data_ESP32():

    # Get Temperature of the ESP itself and convert to Celsius
    temp_core = ( esp32.raw_temperature() - 32 ) / 1.8
    print('Temperature in Core in Celsius')
    print(temp_core)
    
    return temp_core



# This Function gets a pin id and return with the temperature and humidity from a DHT11 sensor
def get_data_DGT11(x):

    print('Setting up and reading Temperature and Humidity')
    sens_t_h = dht.DHT11(machine.Pin(x))

    sens_t_h.measure()
    temp_DGT11 = sens_t_h.temperature()
    print('Temperature in Celsius')
    print(temp_DGT11)
    hum_DGT11 = sens_t_h.humidity()
    print('Humidity Relative Percentage')
    print(hum_DGT11)
    
    return temp_DGT11, hum_DGT11
    
    
    
# This is for reading the data from the BME280
def get_data_BME280():
    
    # Gets the Data from the BME280
    bme = BME280.BME280(i2c=i2c)
    temp_BME280 = bme.temperature
    hum_BME280 = bme.humidity
    pres_BME280 = bme.pressure
    
    # Removes extra stuff after the Data because ThingSpeak don't like it
    temp_BME280 = re.sub('C', '', temp_BME280)
    hum_BME280 = re.sub('%', '', hum_BME280)
    pres_BME280 = re.sub('hPa', '', pres_BME280)
    
    print('Data from BME280')
    print('Temperature: ', temp_BME280)
    print('Humidity: ', hum_BME280)
    print('Pressure: ', pres_BME280)
    
    return temp_BME280, hum_BME280, pres_BME280
    
    
    
 
# This is the Network stuff connecting and sending data and then disconecting the network
def send_data(temp_DGT11, hum_DGT11, temp_core, temp_BME280, hum_BME280, pres_BME280):
    
    print('Setting up network')
    wlan1 = network.WLAN(network.STA_IF)
    wlan1.active(True)
    
    # I know it allways return False the first time, but this is easier and makes sure conection is made
    # and the slight delay this makes don't realy matter.
    wlan1.connect(ESSID, Password)
    time_at_connect = utime.ticks_ms()
    while wlan1.isconnected() == False:
        pass
        if utime.ticks_diff(time_at_connect, utime.ticks_ms()) > 60000:
            print('Network error can not connect')
            break
    
    print('Established Network Access')
    
    # MQTT stuff for Conecting to ThingSpeak
    
    print('Create Data Package to ThingSpeak')
    # Combine Data for MQTT
    MQTT_data = "field1={0}&field2={1}&field3={2}&field4={3}&field5={4}&field6={5}".format(temp_DGT11, hum_DGT11, temp_core, temp_BME280, hum_BME280, pres_BME280)
    
    print('Send data to ThingSpeak')
    #Connect to ThingSpeak over MQTT
    MQTT_client.connect()
    MQTT_client.publish(MQTT_topic, MQTT_data)
    MQTT_client.disconnect() 
    
    print('A Short Pause')
    time.sleep(20)
    
    # Shut down Network
    #wlan1.active(False)
    #time.sleep(5)
    
    
    
# Endless Loop. Did it here because i did not want to push the main longer to the right.
while True:
    main()
