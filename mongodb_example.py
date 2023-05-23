import RPi.GPIO as GPIO
import time
from pymongo import MongoClient

# MongoDB connection settings
mongodb_uri = "mongodb+srv://meraj154213:iCFmmhPjFdUk2hvV@cluster0.hj5abn5.mongodb.net/?retryWrites=true&w=majority"

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin connected to the soil sensor
soil_moisture_pin = 21

def read_soil_moisture():
    # Set up the GPIO pin as an input
    GPIO.setup(soil_moisture_pin, GPIO.IN)

    # Read the soil moisture level
    moisture_level = GPIO.input(soil_moisture_pin)

    return moisture_level

try:
    # Connect to MongoDB
    client = MongoClient(mongodb_uri)

    # Access a database and collection
    db = client['mydatabase']
    collection = db['testdb']

    while True:
        moisture = read_soil_moisture()
        print("Soil moisture level: {}".format(moisture))

        # Prepare the document to be inserted into the collection
        document = {'moisture_level': moisture, 'timestamp': time.time()}

        # Insert the document into the collection
        collection.insert_one(document)

        time.sleep(60)

except KeyboardInterrupt:
    # Clean up GPIO settings on keyboard interrupt
    GPIO.cleanup()

    # Close MongoDB connection
    client.close()
