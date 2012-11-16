Connections
===========

Ensure correct access
---------------------
See http://www.das-werkstatt.com/forum/werkstatt/viewtopic.php?f=7&t=1902

Test from command line
----------------------
stty -F /dev/ttyUSB0 ispeed 4800 && cat < /dev/ttyUSB0

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