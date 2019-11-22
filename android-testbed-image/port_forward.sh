#!/bin/bash

echo "Starting port forawrding script...."

ip=$(ip addr show eth0 | grep "inet" | cut -f6 -d" " | cut -f1 -d"/")

echo "Container IP: ${ip}"

socat tcp-listen:5554,bind=$ip,fork tcp:127.0.0.1:5554 &
socat tcp-listen:5555,bind=$ip,fork tcp:127.0.0.1:5555