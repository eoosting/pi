#!/bin/bash
cd ~pi/bin
curl -O https://raw.githubusercontent.com/eoosting/pi/master/setupnotes.txt
curl -O https://raw.githubusercontent.com/eoosting/pi/master/bluenotes.txt
curl -O https://raw.githubusercontent.com/eoosting/pi/master/audionotes.txt
curl -O https://raw.githubusercontent.com/eoosting/pi/master/ipannounce.py
curl -O https://raw.githubusercontent.com/eoosting/pi/master/pibot.py
curl -O https://raw.githubusercontent.com/eoosting/pi/master/mqttnotes.txt
curl -O https://raw.githubusercontent.com/eoosting/pi/master/irnotes.txt
curl -O https://raw.githubusercontent.com/eoosting/pi/master/gitnotes.txt
curl -O https://raw.githubusercontent.com/eoosting/pi/master/getgit.sh
curl -O https://raw.githubusercontent.com/eoosting/pi/master/rpi-hdmi.sh
chown pi:pi getgit.sh
chmod ugo+rx getgit.sh
chmod ugo+rx rpi-hdmi.sh
