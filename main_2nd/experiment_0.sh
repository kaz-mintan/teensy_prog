#!/bin/bash
#./experiment_0.py "ir or sma" "port number"

if [ $# -ne 2 ]; then
	echo "input 2 argument" 1>&2
	exit 1
fi

echo $1
echo $2

if [ $1 = ir ]; then
	echo "ir"
	python serial_com/serial_read5.py /dev/ttyACM$2
elif [ $1 = sma ]; then
	echo "ir"
	python serial_com/send_4para.py /dev/ttyACM$2
else
	echo "hoge"
fi
