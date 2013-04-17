Connections
===========

Ensure correct access
---------------------
See http://www.das-werkstatt.com/forum/werkstatt/viewtopic.php?f=7&t=1902

Test from command line
----------------------
stty -F /dev/ttyUSB0 ispeed 4800 && cat < /dev/ttyUSB0

GPS Readings:
-------------

See http://aprs.gids.nl/nmea/

Sample output:
```
$GPGSA,A,1,,,,,,,,,,,,,,,*1E

$GPRMC,144207.579,V,,,,,,,170413,,,N*42

$GPGGA,144208.579,,,,,0,00,,,M,0.0,M,,0000*56

$GPGSA,A,1,,,,,,,,,,,,,,,*1E

$GPRMC,144208.579,V,,,,,,,170413,,,N*4D

$GPGGA,144209.579,,,,,0,00,,,M,0.0,M,,0000*57

$GPGSA,A,1,,,,,,,,,,,,,,,*1E

$GPGSV,1,1,00*79

$GPRMC,144209.579,V,,,,,,,170413,,,N*4C

$GPGGA,144210.579,,,,,0,00,,,M,0.0,M,,0000*5F

$GPGSA,A,1,,,,,,,,,,,,,,,*1E
```

Installation
------------
Need to install pyserial
`sudo apt-get install python-serial python-flup`

Wireless Hotspot
================

http://www.raspberrypi.org/phpBB3/viewtopic.php?f=36&t=19120

Enable I2C
==========
http://www.instructables.com/id/Raspberry-Pi-I2C-Python/

This looks like it could be good: http://elinux.org/RPi_ADC_I2C_Python
