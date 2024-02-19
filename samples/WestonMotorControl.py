#!/usr/bin/env python
"""
Simple g-code streaming script for grbl
"""

import serial
import serial.tools.list_ports
import time


print(serial.tools.list_ports.comports())
# Open grbl serial port
s = serial.Serial('COM24', 115200)

# Open g-code file
f = open(r"C:\Users\westontest\Downloads\3DBenchy.gcode", 'r')

s.write(b'G90\n')


# Stream g-code to grbl
for line in f:
    l = line.strip()  # Strip all EOL characters for streaming
    print('Sending: {}'.format(l))
    s.write(l.encode() + b'\n')  # Send g-code block to grbl
    grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
    print(' : {}'.format(grbl_out.strip()))

# Wait here until grbl is finished to close serial port and file.
input("  Press <Enter> to exit and disable grbl.")

# Close file and serial port
f.close()
s.close()
