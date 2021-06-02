#!/usr/bin/python3

import sys
import serial
from datetime import datetime
from time import sleep
import logging
from multiprocessing import Process  # Used to define a timeout

# Check system arguments
if 2 < len(sys.argv) < 6:
    device = sys.argv[1]
    baudrate = sys.argv[2]
    timeout = int(sys.argv[3])
    if len(sys.argv) == 5:
        logfile = sys.argv[4]
        logflag = 1
    else:
        logflag = 0
else:
    print('\n')
    print('Wrong arguments')
    print('\n')
    print('Use: ./uart-terminal [device] [baud rate] [timeout] *[logfile]')
    print('\n')
    print('* optional')
    print('\n')
    sys.exit(1)


logger = logging.getLogger()
logger.setLevel(logging.INFO)
stdout_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stdout_handler)

if logflag:
    output_handler = logging.FileHandler(logfile)
    logger.addHandler(output_handler)


# Creating read process fuction
def read():
    while True:
        data = ser.readline()
        if data != b'' and data[0] == 0x0d:
            # Remove the Carriage Return character
            output = str(datetime.now()) + ">    " + data[1:].decode('utf-8')
            logger.info(output)

        elif data != b'':
            output = str(datetime.now()) + ">    " + data.decode('utf-8')
            logger.info(output)


# Define serial port
with serial.Serial(device, baudrate, timeout=0.5) as ser:

    if ser.isOpen():
        ser.close()
        print('Reset serial connection')

    ser.open()
    print('Open serial port at ' + device)

    while ser.inWaiting():
        ser.reset_input_buffer()
        print('Reseting input buffer')

    # This defines a process which will execute the 'read' function
    # after a predetermined ammount of time, it will terminate
    # that way we can control for how long we'll log the execution
    log_process = Process(target=read, name='Logging_Process')
    log_process.start()
    log_process.join(timeout=int(timeout))
    log_process.terminate()

    if log_process.exitcode is None:
        logger.info('process terminated after %s seconds', timeout)
        logger.info('Closing serial port')
        sleep(1)
        ser.close()
        sys.exit(0)
