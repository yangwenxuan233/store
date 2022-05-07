from __future__ import print_function
import binascii
from numpy import r_
import serial
import struct


class LaserModbus():
    def __init__(self, port: str) -> None:
        self.port = port

    def single_range(self) -> None:
        com = serial.Serial(self.port, 9600)
        status = com.write()


com = serial.Serial('COM5', 9600, timeout=0.1)
w_status = com.write(bytes.fromhex('FA040150B1'))
print(w_status)
r_status = com.readline()
print(r_status)
# string = binascii.b2a_hex(r_status).decode('utf-8')
string = bytes.hex(r_status)

print(string)

w_status = com.write(bytes.fromhex('FA0604FC'))
print(w_status)
r_status = com.readline()
print(r_status)
