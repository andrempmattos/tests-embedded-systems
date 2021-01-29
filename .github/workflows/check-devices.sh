#!/bin/bash

for i in {0..9} 
do
	if [ -a "/dev/ttyUSB${i}" ] 
	then
		output=$(/bin/udevadm info --name=/dev/ttyUSB${i} | grep SERIAL_SHORT)
		echo "/dev/ttyUSB${i} ${output}"
	fi
done

for i in {0..9} 
do
    if [ -a "/dev/ttyACM${i}" ] 
	then
		output=$(/bin/udevadm info --name=/dev/ttyACM${i} | grep SERIAL_SHORT)
		echo "/dev/ttyACM${i} ${output}"
	fi
done
