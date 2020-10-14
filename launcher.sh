#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd /
cd home/pi/Documents/Tracking-Tortoise
sudo python3 track_geno.py
cd /
