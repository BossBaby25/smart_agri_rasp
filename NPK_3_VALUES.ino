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
