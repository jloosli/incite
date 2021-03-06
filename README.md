Connections
===========

Ensure correct access
---------------------
See http://www.das-werkstatt.com/forum/werkstatt/viewtopic.php?f=7&t=1902

Test from command line
----------------------
stty -F /dev/ttyUSB0 ispeed 4800 && cat < /dev/ttyUSB0

Troubleshooting
---------------
I needed to edit the default file on the Ubuntu system:

```
sudo vi /etc/default/gpsd
```

and add in `/dev/ttyUSB0` into the default devices

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

`sudo apt-get install git python-serial python-flup sqlite3 python-smbus gpsd gpsd-clients python-gps python-pip`

get requests library
`sudo pip install requests`

set up gpsd
`sudo dpkg-reconfigure gpsd`

Enable USB GPS
`echo 'KERNEL=="ttyUSB0", MODE="0666"' | sudo tee -a /etc/udev/rules.d/80-ttyusb.rules`

Add usergroups
`sudo usermod -a -G i2c pi`

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
echo "Incite incite init.d"
# Carry out specific functions when asked to by the system
case "$1" in
  start)
    echo "Starting incite"
    # run application you want to start
    gpsd /dev/ttyUSB0
    /home/pi/incite/incite.py &
    ;;
  stop)
    echo "Stopping incite"
    # kill application you want to stop
    pkill -f incite.py
    ;;
  *)
    echo "Usage: /etc/init.d/incite {start|stop}"
    exit 1
    ;;
esac

exit 0

```

```
sudo chmod 755 /etc/init.d/incite
sudo update-rc.d incite defaults && sudo /etc/init.d/incite start
```

GPS setup:
gps.db
```
CREATE TABLE gps_datum (id INTEGER PRIMARY KEY AUTOINCREMENT, dataset_id INTEGER, gpsstring TEXT, speed REAL);
CREATE TABLE gps_dataset (id INTEGER PRIMARY KEY AUTOINCREMENT, start TEXT);
```
samples.db
```
CREATE TABLE samples(id INTEGER PRIMARY KEY AUTOINCREMENT, dataset INTEGER, date TEXT, ch0 REAL, ch1 REAL, ch2 REAL, ch3 REAL, lat TEXT, lon TEXT, speed REAL, gpstime TEXT);
```

on server:
```
CREATE TABLE samples(id INTEGER PRIMARY KEY AUTOINCREMENT, dataset TEXT, date TEXT, ch0 REAL, ch1 REAL, ch2 REAL, ch3 REAL, lat TEXT, lon TEXT, speed REAL, gpstime TEXT);
```

To reset the samples table (including autoincrement):
```
delete from samples;
update sqlite_sequence SET seq=0 WHERE name='samples';
```

Update if-up.d sleep 10 seconds then call everything (non blocking)

`sudo nano /etc/network/if-up.d/incite-update` 
```
#! /bin/sh

HOMEDIR="/home/pi/"
INCITEDIR="${HOMEDIR}incite/"
GITLOG="${HOMEDIR}git.log"

(
sleep 10
cd $INCITEDIR
git pull 2>&1 | tee -a $GITLOG
git submodule update 2>&1 | tee -a $GITLOG
"${INCITEDIR}zipdataset.py"
) &
```

`sudo chmod +x /etc/network/if-up.d/incite-update`

Wireless Hotspot
================

http://www.raspberrypi.org/phpBB3/viewtopic.php?f=36&t=19120

Enable I2C
==========
http://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c

Configure automatic startup
================
http://www.stuffaboutcode.com/2012/06/raspberry-pi-run-program-at-start-up.html

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
