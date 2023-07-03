import RPi.GPIO as GPIO
import time
from pymongo import MongoClient
import serial

# MongoDB connection settings
mongodb_uri = "mongodb+srv://meraj154213:iCFmmhPjFdUk2hvV@cluster0.hj5abn5.mongodb.net/?retryWrites=true&w=majority"

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Serial port settings for NPK sensor
serial_port = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=1)

def read_npk_sensor():
    # Read the response from Arduino
    arduino_data = serial_port.readline().decode().strip()
    npk_data = arduino_data.split(',')
    nitrogen = float(npk_data[0])
    phosphorus = float(npk_data[1])
    potassium = float(npk_data[2])

    return nitrogen, phosphorus, potassium

try:
    # Connect to MongoDB
    client = MongoClient(mongodb_uri)

    # Access a database and collection
    db = client['mydatabase']
    collection = db['test1db']

    while True:
        nitrogen, phosphorus, potassium = read_npk_sensor()
        print("NPK levels - N: {}, P: {}, K: {}".format(nitrogen, phosphorus, potassium))

        # Prepare the document to be inserted into the collection
        document = {
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
