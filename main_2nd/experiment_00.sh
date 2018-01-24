#!/bin/sh

if [ $# -ne 1 ]; then
	echo "input 1 argument (number or name)" 1>&2
	exit 1
fi

number=$1
today=$(date "+%Y%m%d")

if [ $number = delete ]; then
	rm *.csv
fi

