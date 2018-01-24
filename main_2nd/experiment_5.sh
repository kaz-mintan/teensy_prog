#!/bin/sh

if [ $# -ne 1 ]; then
	echo "input 1 argument (number or name)" 1>&2
	exit 1
fi

number=$1
today=$(date "+%Y%m%d")
mode1=heuristic
mode2=delta

dir_1="/home/kumagai/data/waterloo/exp_"$today"_"$mode1"_"$number
dir_2="/home/kumagai/data/waterloo/exp_"$today"_"$mode2"_"$number
server="kumagai@mizuuchi.lab.tuat.ac.jp:/home/kumagai/data/waterloo/user_study/"

f1="question_picture.csv"

#python motion_dqn_hard.py $mode /dev/ttyACM$sma_port /dev/ttyACM$ir_port

#mv $f1 $f2 $f3 $f4 $f5 $f6 $f7 $f9 $f10 $f11 $dir
#mv $dir_2 $dir
rm $f1

scp -rp $dir_1 $dir_2 $server

#python motion_dqn_hard.py heuristic /dev/ttyACM0 /dev/ttyACM1
#csv files
