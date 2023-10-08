# This Python script is designed to communicate with a serial device (a TZBOT-magnetic-field-sensor-TZS-MAG-1600-A sensor) and 
# publish the received data to a ROS (Robot Operating System) topic named 'loc'. 
# Here's a step-by-step explanation of the code:
# In summary, this script reads data from a serial port

# Shebang Line This line specifies the interpreter to use to run the script, in this case, Python.
#!/usr/bin/env python
# Import Statements
import serial # Imports the Python Serial library, which is used for serial communication.
import struct # Imports the Python struct library, which is used for packing and unpacking binary data.

# This function is the main part of the script where data is read from the serial port and 
# published to the 'loc' topic.
def talker():
    # Serial Port Configuration
    # Configures the serial port. 
    # It specifies the port ('/dev/ttyUSB0') and the baud rate (38400) for communication with the sensor.
    ser = serial.Serial('/dev/ttyUSB0', 115200)
    #Data Read and Processing
    data = ser.read(size=14) #  Reads 14 bytes of data from the serial port. This assumes that each data packet from the sensor is 14 bytes long.
    print(data)
    listTestByte = list(data)# Converts the received data into a list of bytes for further processing.
    print(listTestByte)   
    lbyte = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    i = 0
    ft = False
    # Data Processing Loop:
    while True: # This loop runs always and not shut down.
        data = ser.read() # Reads one byte of data from the serial port at a time.
        if data == b'\xaa':
            i = 0        
            ft = True
        if ft == True: # Data is processed in the `if ft == True` block:
            lbyte[i] = data # Bytes are stored in the `lbyte` list. 
            if i == 11:
                print ("".join(map("{0:08b}".format, map(ord, list(data))))),
            if i == 12:
                print ("".join(map("{0:08b}".format, map(ord, list(data)))))
        # When the 14 bytes are received (i.e., `i` reaches 13), the last two bytes are combined into a 16-bit integer (`loc`) using `struct.unpack`.
            if i == 13: 
                i = 0
                ft = False
                pos = b''.join(lbyte[5:11])
                binary_string = "".join(map("{0:08b}".format, map(ord, list(pos))))
                decimal_number = int(binary_string, 2)
                
                loc = struct.unpack('>H', pos)[0]
                print(int(loc))
                if (loc > 0):
                    print "Line detected"
                else:
                    print "No line"
            i = i + 1
            
# Main Block:
#    This block is executed when the script is run directly (not imported as a module).
if __name__ == '__main__':
        talker()