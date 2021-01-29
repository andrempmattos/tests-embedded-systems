#!/usr/bin/python3

import sys
import _thread
import serial
from datetime import datetime


## Check system arguments
if 2 < len(sys.argv) < 5:
    device = sys.argv[1]
    baudrate = sys.argv[2]
    if len(sys.argv) == 4:
        logfile = sys.argv[3]
        logflag = 1
    else:
        logflag = 0
else:
    print('\n')
    print('Wrong arguments')
    print('\n')
    print('Use: ./uart-terminal [device] [baud rate] *[logfile]')
    print('\n')
    print('* optional')
    print('\n')
    sys.exit()

## Creating Keyboard Interrupt Handler function
def keyboardInterruptHandler():
    print('[#] Port ' + device + ' closed.')
    ser.close()
    _thread.exit()

## Creating read process fuction
def read():
    try:
        while True:
            data = ser.readline()
            if data != b'' and data[0] == 0x0d:
                output = str(datetime.now()) + ">    " + data[1:].decode('utf-8') ## Remove the Carriage Return character
                if logflag:
                    f.write(output)
                    f.flush()
                print(output, end = '') 
            elif data != b'':
                output = str(datetime.now()) + ">    " + data.decode('utf-8')
                if logflag:
                    f.write(output)
                    f.flush()
                print(output, end = '')
    except:
        keyboardInterruptHandler()

## Define serial port
with serial.Serial(device, baudrate, timeout=0.5) as ser:

    if ser.isOpen():
        ser.close()
        print('Reset serial connection')

    ser.open()
    print('Open serial port at ' + device)

    while ser.inWaiting():
        ser.reset_input_buffer()
        print('Reseting input buffer')

    ## Create logfile if defined
    if logflag:
        f = open(logfile, 'a')
            
    _thread.start_new_thread(read,())

    while True:
        try:
            inp = input().encode('utf-8') + '\n'.encode('utf-8')
            ser.write(inp)
        except:
            sys.exit()