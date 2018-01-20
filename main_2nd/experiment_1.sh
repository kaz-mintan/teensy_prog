#!/bin/sh

if [ $# -ne 4 ]; then
	echo "input 4 argument" 1>&2
	exit 1
fi

mode=$1
sma_port=$2
ir_port=$3
number=$4

python motion_dqn_hard.py $1 /dev/ttyACM$2 /dev/ttyACM$3

#python motion_dqn_hard.py heuristic /dev/ttyACM0 /dev/ttyACM1
