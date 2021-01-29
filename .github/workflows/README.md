# UART Terminal Python

It is a simple serial terminal written in Python.

## Software requirements

- Python 3

**Obs:** 
- *Tested with Python 3.7.3 using Windows 10 [Build 18362]*

## Python required libraries

- sys
- _thread
- datetime
- pyserial

## Usage

- ### **Linux**

```
./uart-terminal.py [port] [baud] *[logfile]
```
Where:
- [port]: device port (ex: /dev/ttyUSB0)
- [baud]: device baud rate (ex: 115200)
- [logfile]: if defined, will store the input data to the file (ex: log_yyyy_mm_dd.txt)
- *: optional

Example:
```
./uart-terminal.py /dev/ttyACM0 115200 log_2020-02-17.txt
```

- ### **Windows**

```
py.exe .\uart-terminal.py [port] [baud] *[logfile]
```
Where:
- [port]: device port (ex: COM1)
- [baud]: device baud rate (ex: 115200)
- [logfile]: if defined, will store the input data to the file (ex: log_yyyy_mm_dd.txt)
- *: optional

Example:
```
py.exe .\uart-terminal.py COM1 115200 log_2020-02-17.txt
```