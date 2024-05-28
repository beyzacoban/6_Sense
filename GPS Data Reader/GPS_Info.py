import serial

def read_gps():
    ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)
    while True:
        line = ser.readline().decode('ascii', errors='replace')
        if '$GPGGA' in line:
            data = line.split(',')
            latitude = data[2]
            longitude = data[4]
            return latitude, longitude

latitude, longitude = read_gps()
print(f"Latitude: {latitude}, Longitude: {longitude}")
