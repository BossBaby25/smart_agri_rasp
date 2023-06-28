import serial
import time

# Modbus RTU requests for reading NPK values
nitro = [0x01, 0x03, 0x00, 0x1e, 0x00, 0x01, 0xe4, 0x0c]
phos = [0x01, 0x03, 0x00, 0x1f, 0x00, 0x01, 0xb5, 0xcc]
pota = [0x01, 0x03, 0x00, 0x20, 0x00, 0x01, 0x85, 0xc0]

# Serial port configuration
ser = serial.Serial('/dev/ttyUSB0', 4800, timeout=1)  # Replace '/dev/ttyUSB0' with your Raspberry Pi's serial port

def read_nitrogen():
    ser.write(nitro)
    time.sleep(0.1)
    response = ser.read(7)
    values = list(response)
    print("Nitrogen:", values[4], "mg/kg")

def read_phosphorous():
    ser.write(phos)
    response = ser.read(7)
    values = list(response)
    print("Phosphorous:", values[4], "mg/kg")

def read_potassium():
    ser.write(pota)
    response = ser.read(7)
    values = list(response)
    print("Potassium:", values[4], "mg/kg")

# Open the serial port
ser.open()

# Check if the serial port is open
if ser.is_open:
    print("Serial port opened successfully")
else:
    print("Failed to open serial port")
    exit()

try:
    while True:
        read_nitrogen()
        time.sleep(0.25)
        read_phosphorous()
        time.sleep(0.25)
        read_potassium()
        time.sleep(1)
except KeyboardInterrupt:
    ser.close()
    print("Serial port closed")
