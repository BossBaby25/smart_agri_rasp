import RPi.GPIO as GPIO
import time
from pymongo import MongoClient
import serial
import Adafruit_DHT
import I2C_LCD_driver

# MongoDB connection settings
mongodb_uri = "mongodb+srv://meraj154213:iCFmmhPjFdUk2hvV@cluster0.hj5abn5.mongodb.net/?retryWrites=true&w=majority"
#include <SoftwareSerial.h>

// Modbus RTU requests for reading NPK values
const byte nitro[] = { 0x01, 0x03, 0x00, 0x1e, 0x00, 0x01, 0xe4, 0x0c };
const byte phos[] = { 0x01, 0x03, 0x00, 0x1f, 0x00, 0x01, 0xb5, 0xcc };
const byte pota[] = { 0x01, 0x03, 0x00, 0x20, 0x00, 0x01, 0x85, 0xc0 };

const int moisturePin = A0;  // Analog pin for soil moisture sensor

// A variable used to store NPK values
byte values[8];

SoftwareSerial mod(2, 3);

void setup() {
  // Set the baud rate for the Serial port
  Serial.begin(4800);

  // Set the baud rate for the SoftwareSerial object
  mod.begin(4800);

  // Set the analog pin for the moisture sensor as input
  pinMode(moisturePin, INPUT);
}

void loop() {
  // Read values
  byte val1, val2, val3;
  val1 = nitrogen();
  delay(250);
  val2 = phosphorous();
  delay(250);
  val3 = potassium();
  delay(250);

  // Read soil moisture value
  int moistureValue = analogRead(moisturePin);

  // Send NPK values and moisture value to Raspberry Pi via serial port
  Serial.print(val1);
  Serial.print(",");
  Serial.print(val2);
  Serial.print(",");
  Serial.print(val3);
  Serial.print(",");
  Serial.println(moistureValue);

  delay(2000);
}

byte nitrogen() {
  mod.write(nitro, 8);
  delay(100);
  for (byte i = 0; i < 8; i++) {
    values[i] = mod.read();
  }
  return values[4];
}

byte phosphorous() {
  mod.write(phos, 8);
  for (byte i = 0; i < 8; i++) {
    values[i] = mod.read();
  }
  return values[4];
}

byte potassium() {
  mod.write(pota, 8);
  for (byte i = 0; i < 8; i++) {
    values[i] = mod.read();
  }
  return values[4];
}

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Serial port settings for Arduino
serial_port = serial.Serial('/dev/ttyACM0', baudrate=4800, timeout=1)

# DHT22 sensor pin
dht_pin = 4

# LCD display
lcd = I2C_LCD_driver.lcd()

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

        # Display the values on the LCD
        lcd.lcd_display_string("NPK levels:", 1)
        lcd.lcd_display_string("N: {}, P: {}, K: {}".format(nitrogen, phosphorus, potassium), 2)
        lcd.lcd_display_string("Soil Moisture: {}".format(soil_moisture), 3)
        lcd.lcd_display_string("Humidity: {:.2f}%, Temp: {:.2f}C".format(humidity, temperature), 4)

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

        time.sleep(1)

except KeyboardInterrupt:
    # Clean up GPIO settings on keyboard interrupt
    GPIO.cleanup()

    # Close MongoDB connection
    client.close()

    # Close the serial port
    serial_port.close()
