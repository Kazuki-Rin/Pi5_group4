#!/bin/bash
sleep 10
export XDG_RUNTIME_DIR=/run/user/$(id -u)
export WAYLAND_DISPLAY=wayland-1
export DISPLAY=:0
cd /home/pi/Documents/Raspberry_project_nhom4
python3 hethong.py > log.txt 2>&1