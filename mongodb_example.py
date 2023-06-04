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

# RS485 to TTL settings
serial_port = '/dev/ttyAMA0'  # Update with the correct serial port
baud_rate = 9600

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

def read_npk_data():
    # Initialize the serial connection
    ser = serial.Serial(serial_port, baud_rate, timeout=1)

    # Send command to request NPK data
    ser.write(b'ReadNPK\r\n')

    # Read the response from the sensor
    response = ser.readline().decode().strip()

    # Extract NPK values from the response
    npk_data = response.split(',')

    # Close the serial connection
    ser.close()

    return npk_data

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

        npk_data = read_npk_data()
        print("NPK Data: N={}, P={}, K={}".format(npk_data[0], npk_data[1], npk_data[2]))

        # Prepare the document to be inserted into the collection
        document = {
            'moisture_level': moisture,
            'temperature': temperature,
            'humidity': humidity,
            'npk_data': {
                'N': npk_data[0],
                'P': npk_data[1],
                'K': npk_data[2]
            },
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
