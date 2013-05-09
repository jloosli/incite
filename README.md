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
`sudo apt-get install git python-serial python-flup sqlite3`

Enable USB GPS
`echo 'KERNEL=="TTYUSB0", MODE="0666"' | sudo tee -a /etc/udev/rules.d/80-ttyusb.rules`

Set up repository
`git clone https://github.com/jloosli/incite.git && cd incite && git submodule init && git submodule update`

set up auto run
`sudo nano /etc/init.d/incite`

Enter the following:
```
#! /bin/sh
# /etc/init.d/incite 

### BEGIN INIT INFO
# Provides:          incite
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Simple script to start a program at boot
# Description:       Run script at startup
### END INIT INFO

# If you want a command to always run, put it here

# Carry out specific functions when asked to by the system
case "$1" in
  start)
    echo "Starting incite"
    # run application you want to start
    /home/pi/incite/testadc.py
    ;;
  stop)
    echo "Stopping incite"
    # kill application you want to stop
    killall testadc.py
    ;;
  *)
    echo "Usage: /etc/init.d/incite {start|stop}"
    exit 1
    ;;
esac

exit 0
```

GPS setup:
gps.db
```
CREATE TABLE gps_datum (id INTEGER PRIMARY KEY AUTOINCREMENT, dataset_id INTEGER, gpsstring TEXT, speed REAL);
CREATE TABLE gps_dataset (id INTEGER PRIMARY KEY AUTOINCREMENT, start TEXT);
```


Wireless Hotspot
================

http://www.raspberrypi.org/phpBB3/viewtopic.php?f=36&t=19120

Enable I2C
==========
http://www.instructables.com/id/Raspberry-Pi-I2C-Python/

This looks like it could be good: http://elinux.org/RPi_ADC_I2C_Python

Startup location
================
/etc/rc.local

Network config
==============
/etc/network/interfaces
```
auto lo
 
iface lo inet loopback
iface eth0 inet dhcp
 
allow-hotplug wlan0
iface wlan0 inet manual
wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf
iface default inet dhcp
```

/etc/wpa_suplicant/wpa_supplicant.conf
```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
  ssid="{SSID}"
    psk="{Password}"
    proto=RSN
    key_mgmt=WPA-PSK
    pairwise=CCMP
    auth_alg=OPEN
}
```
