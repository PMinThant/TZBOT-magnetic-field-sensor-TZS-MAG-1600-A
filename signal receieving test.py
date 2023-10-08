#!/usr/bin/env python
import serial
import struct


def talker():
    ser = serial.Serial('/dev/ttyUSB0', 115200)
    data = ser.read(size=14)
    print(data)
    listTestByte = list(data)
    print(listTestByte)   
    lbyte = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    i = 0
    ft = False
    while True:
        data = ser.read()
        if data == b'\xaa':
            i = 0        
            ft = True
        if ft == True:
            lbyte[i] = data   
            if i == 11:
                print ("".join(map("{0:08b}".format, map(ord, list(data))))),
            if i == 12:
                print ("".join(map("{0:08b}".format, map(ord, list(data)))))
            if i == 13:
                i = 0
                ft = False
                pos = b''.join(lbyte[5:11])
                binary_string = "".join(map("{0:08b}".format, map(ord, list(pos))))
                decimal_number = int(binary_string, 2)
                
                loc = struct.unpack('>H', pos)[0]
                print(loc)
                if (loc > 0):
                    print "Line detected"
                else:
                    print "No line"
            i = i + 1
            

if __name__ == '__main__':
        talker()