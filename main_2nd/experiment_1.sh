#!/bin/sh

if [ $# -ne 4 ]; then
	echo "input 4 argument" 1>&2
	exit 1
fi

mode=$1
sma_port=$2
ir_port=$3
number=$4
today=$(date "+%Y%m%d")

dir="/home/kumagai/data/waterloo/exp_"$today"_"$mode"_"$number
mkdir -p $dir

f1="test_state.csv"
f2="test_state_mean.csv"
f3="test_action_start.csv"
f4="test_reward_face.csv"
f5="reward_extracted.csv"
f6="test_action_stop.csv"
f7="test_reward.csv"
f8="question_picture.csv"

python motion_dqn_hard.py $mode /dev/ttyACM$sma_port /dev/ttyACM$ir_port

mv $f1 $f2 $f3 $f4 $f5 $f6 $f7 $f8 $dir

#python motion_dqn_hard.py heuristic /dev/ttyACM0 /dev/ttyACM1
#csv files
