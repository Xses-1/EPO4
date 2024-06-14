#!/bin/bash

# The first 2 arguments are the first target, the 2nd 2 are the 2nd target
# the last 3 are the current position and the angle

# Test command: sudo ./B.sh 2 2 0 0 1 1 1

MIDPOINT="$({ echo "$1"; echo "$2"; echo "$5"; echo "$6"; echo "$7"; } | ./B.py)"
echo $MIDPOINT
IFS=" " read -r cX cY Theta <<< echo $MIDPOINT
sleep 6
(echo "$3"; echo "$4"; echo "$cX"; echo "$cY"; echo "$Theta") | ./B.py
