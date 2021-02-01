#!/usr/bin/python3

import sys
import serial
from datetime import datetime
import re


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
    sys.exit(1)


## Checking the result of the test
def test_result_check(output):
    test_flag = re.search("\033\[1\;34m", output)
    if test_flag is not None:
        test_flag_index = test_flag.span()
        test_message_start = test_flag_index[1]

        if re.search("Automated test passed!", output[test_message_start:]) is not None:
            return 0
        else:         
            return 1
    else:
        return 2

## Creating Keyboard Interrupt Handler function
def keyboardInterruptHandler(handler_check):
    if handler_check == 0:
        print('Test finished with success!')
        print('[#] Port ' + device + ' closed.')
        ser.close()
        sys.exit(0)
    elif handler_check == 1:
        print('Test finished with erros!')
        print('[#] Port ' + device + ' closed.')
        ser.close()
        sys.exit(1)
    else:
        print('Test aborted!')
        print('[#] Port ' + device + ' closed.')
        ser.close()
        sys.exit(1)


## Creating read process fuction
def read():
    handler_check = 3
    try:
        while True:
            data = ser.readline()
            if data != b'' and data[0] == 0x0d:
                output = str(datetime.now()) + ">    " + data[1:].decode('utf-8') ## Remove the Carriage Return character
                if logflag:
                    f.write(output)
                    f.flush()
                print(output, end = '') 
                handler_check = test_result_check(output)
                if handler_check != 2:  ## Check if it is a regular case or the end of the test
                    ser.close()         ## Just to activate the exception

            elif data != b'':
                output = str(datetime.now()) + ">    " + data.decode('utf-8')
                if logflag:
                    f.write(output)
                    f.flush()
                print(output, end = '')
                handler_check = test_result_check(output)
                if handler_check != 2:  ## Check if it is a regular case or the end of the test
                    ser.close()         ## Just to activate the exception

    except:
        keyboardInterruptHandler(handler_check)

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
            
    read()






