import serial

s = serial.Serial('COM3')
while True:
    res = s.readline()
    print(res.decode())