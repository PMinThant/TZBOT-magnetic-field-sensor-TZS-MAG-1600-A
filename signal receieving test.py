#!/usr/bin/env python
import serial
import struct
import rospy

from std_msgs.msg import Int16
def talker():
    pub = rospy.Publisher('loc', Int16, queue_size=10)
    rospy.init_node('mag_loc', anonymous=False)
    rate = rospy.Rate(10) # 10hz
    ser = serial.Serial('/dev/ttyUSB0', 115200)
    data = ser.read(size=14)
    print(data)
    listTestByte = list(data)
    print(listTestByte)   
    lbyte = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    i = 0
    ft = False
    while not rospy.is_shutdown():
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
                pos = b''.join(lbyte[11:13])
                binary_string = "".join(map("{0:08b}".format, map(ord, list(pos))))
                decimal_number = int(binary_string, 2)
                
                loc = struct.unpack('>H', pos)[0]
                print(loc)
                pub.publish(loc)
                if (loc > 0):
                    print "Line detected"
                else:
                    print "No line"
            i = i + 1
            

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass