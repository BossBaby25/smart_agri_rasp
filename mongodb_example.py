import RPi.GPIO as GPIO
import time
from pymongo import MongoClient
import serial

# MongoDB connection settings
mongodb_uri = "mongodb+srv://meraj154213:iCFmmhPjFdUk2hvV@cluster0.hj5abn5.mongodb.net/?retryWrites=true&w=majority"

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Serial port settings for Arduino
serial_port = serial.Serial('/dev/ttyACM0', baudrate=4800, timeout=1)

def read_npk_sensor():
    # Read the response from Arduino
    arduino_data = serial_port.readline().decode().strip()
    npk_data = arduino_data.split(',')
    
    print("Received data from Arduino:", npk_data)  # Debugging line
    
    if len(npk_data) >= 3:
        nitrogen = npk_data[0]
        phosphorus = npk_data[1]
        potassium = npk_data[2]
        soil_moisture = npk_data[3]
    else:
        nitrogen, phosphorus, potassium, soil_moisture = "N/A", "N/A", "N/A", "N/A"

    return nitrogen, phosphorus, potassium, soil_moisture

try:
    # Connect to MongoDB
    client = MongoClient(mongodb_uri)

    # Access a database and collection
    db = client['mydatabase']
    collection = db['test11db']

    while True:
        nitrogen, phosphorus, potassium, soil_moisture = read_npk_sensor()
        print("NPK levels - N: {}, P: {}, K: {},, soil_moisture: {}".format(nitrogen, phosphorus, potassium, soil_moisture))

        # Prepare the document to be inserted into the collection
        document = {
            'nitrogen': nitrogen,
            'phosphorus': phosphorus,
            'potassium': potassium,
            'soil_moisture' : soil_moisture,
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
