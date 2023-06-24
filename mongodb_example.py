# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
from pymongo import MongoClient
import Adafruit_DHT
import serial

# MongoDB connection settings
mongodb_uri = "mongodb+srv://meraj154213:iCFmmhPjFdUk2hvV@cluster0.hj5abn5.mongodb.net/?retryWrites=true&w=majority"

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin connected to the soil sensor
soil_moisture_pin = 21

# Define the GPIO pin connected to the DHT22 sensor
dht_pin = 4

# Serial port settings for NPK sensor
serial_port = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=1)

def read_soil_moisture():
    # Set up the GPIO pin as an input
    GPIO.setup(soil_moisture_pin, GPIO.IN)

    # Read the soil moisture level
    moisture_level = GPIO.input(soil_moisture_pin)

    return moisture_level

def read_dht22():
    # Read temperature and humidity from DHT22 sensor
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, dht_pin)

    return humidity, temperature

def read_npk_sensor():
    # Send command to request NPK data
    serial_port.write(b'ReadNPK\r\n')

    # Read the response from NPK sensor
    response = serial_port.readline().decode().strip()

    # Process the response and extract N, P, K data
    npk_data = response.split(',')
    nitrogen = float(npk_data[0])
    phosphorus = float(npk_data[1])
    potassium = float(npk_data[2])

    return nitrogen, phosphorus, potassium

try:
    # Connect to MongoDB
    client = MongoClient(mongodb_uri)

    # Access a database and collection
    db = client['mydatabase']
    collection = db['testdb']

    while True:
        moisture = read_soil_moisture()
        print("Soil moisture level: {}".format(moisture))

        humidity, temperature = read_dht22()
        print("Temperature: {}°C, Humidity: {}%".format(temperature, humidity))

        nitrogen, phosphorus, potassium = read_npk_sensor()
        print("NPK levels - N: {}, P: {}, K: {}".format(nitrogen, phosphorus, potassium))

        # Prepare the document to be inserted into the collection
        document = {
            'moisture_level': moisture,
            'temperature': temperature,
            'humidity': humidity,
            'nitrogen': nitrogen,
            'phosphorus': phosphorus,
            'potassium': potassium,
            'timestamp': time.time()
        }

        # Insert the document into the collection
        collection.insert_one(document)

        time.sleep(1)

except KeyboardInterrupt:
    # Clean up GPIO settings on keyboard interrupt
    GPIO.cleanup()

    # Close MongoDB connection
    client.close()

    # Close the serial port
    serial_port.close()
