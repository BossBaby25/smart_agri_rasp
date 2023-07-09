import RPi.GPIO as GPIO
import time
from pymongo import MongoClient
import serial
import Adafruit_DHT
import requests

# ThingSpeak API settings
thingspeak_api_key = "GEKETSRJ26FSSSXK"
thingspeak_update_url = "https://api.thingspeak.com/update.json"

# MongoDB connection settings
mongodb_uri = "mongodb+srv://meraj154213:iCFmmhPjFdUk2hvV@cluster0.hj5abn5.mongodb.net/?retryWrites=true&w=majority"

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Serial port settings for Arduino
serial_port = serial.Serial('/dev/ttyACM0', baudrate=4800, timeout=1)

# DHT22 sensor pin
dht_pin = 4

def read_npk_sensor():
    # Read the response from Arduino
    arduino_data = serial_port.readline().decode().strip()
    npk_data = arduino_data.split(',')

    print("Received data from Arduino:", npk_data)  # Debugging line

    if len(npk_data) >= 4:
        nitrogen = npk_data[0]
        phosphorus = npk_data[1]
        potassium = npk_data[2]
        soil_moisture = npk_data[3]
        humidity, temperature = read_dht_sensor()
    else:
        nitrogen, phosphorus, potassium, soil_moisture, humidity, temperature = "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"

    return nitrogen, phosphorus, potassium, soil_moisture, humidity, temperature

def read_dht_sensor():
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, dht_pin)
    return humidity, temperature

try:
    # Connect to MongoDB
    client = MongoClient(mongodb_uri)

    # Access a database and collection
    db = client['mydatabase']
    collection = db['test11db']

    while True:
        nitrogen, phosphorus, potassium, soil_moisture, humidity, temperature = read_npk_sensor()
        print("NPK levels - N: {}, P: {}, K: {}, soil_moisture: {}".format(nitrogen, phosphorus, potassium, soil_moisture))
        print("DHT22 sensor - Humidity: {:.2f}%, Temperature: {:.2f}°C".format(humidity, temperature))

        # Prepare the document to be inserted into the collection
        document = {
            'nitrogen': nitrogen,
            'phosphorus': phosphorus,
            'potassium': potassium,
            'soil_moisture': soil_moisture,
            'humidity': humidity,
            'temperature': temperature,
            'timestamp': time.time()
        }

        # Insert the document into the collection
        collection.insert_one(document)

        # Prepare the data to be sent to ThingSpeak
        data = {
            'api_key': thingspeak_api_key,
            'field1': nitrogen,
            'field2': phosphorus,
            'field3': potassium,
            'field4': soil_moisture,
            'field5': humidity,
            'field6': temperature
        }

        # Send the data to ThingSpeak using HTTP POST request
        response = requests.post(thingspeak_update_url, data=data)
        print("Data sent to ThingSpeak. Response:", response.text)

        time.sleep(1)

except KeyboardInterrupt:
    # Clean up GPIO settings on keyboard interrupt
    GPIO.cleanup()

    # Close MongoDB connection
    client.close()

    # Close the serial port
    serial_port.close()
