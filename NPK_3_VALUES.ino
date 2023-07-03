#include <SoftwareSerial.h>

// Modbus RTU requests for reading NPK values
const byte nitro[] = { 0x01, 0x03, 0x00, 0x1e, 0x00, 0x01, 0xe4, 0x0c };
const byte phos[] = { 0x01, 0x03, 0x00, 0x1f, 0x00, 0x01, 0xb5, 0xcc };
const byte pota[] = { 0x01, 0x03, 0x00, 0x20, 0x00, 0x01, 0x85, 0xc0 };

// A variable used to store NPK values
byte values[8];

SoftwareSerial mod(2, 3);

void setup() {
  // Set the baud rate for the Serial port
  Serial.begin(4800);

  // Set the baud rate for the SoftwareSerial object
  mod.begin(4800);
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

  // Print values to the serial monitor
  Serial.print("Nitrogen: ");
  Serial.print(val1);
  Serial.println(" mg/kg");
  Serial.print("Phosphorous: ");
  Serial.print(val2);
  Serial.println(" mg/kg");
  Serial.print("Potassium: ");
  Serial.print(val3);
  Serial.println(" mg/kg");

  delay(2000);
}

byte nitrogen() {
  mod.write(nitro, 8);
  delay(100);
  for (byte i = 0; i < 8; i++) {
    values[i] = mod.read();
    Serial.print(values[i], HEX);
  }
  Serial.println();

  return values[4];
}

byte phosphorous() {
  mod.write(phos, 8);
  for (byte i = 0; i < 8; i++) {
    values[i] = mod.read();
    Serial.print(values[i], HEX);
  }
  Serial.println();
  return values[4];
}

byte potassium() {
  mod.write(pota, 8);
  for (byte i = 0; i < 8; i++) {
    values[i] = mod.read();
    Serial.print(values[i], HEX);
  }
  Serial.println();
  return values[4];
}
