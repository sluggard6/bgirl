#!/bin/sh
foo=$0

foo="${foo%/*}"

BASE_PATH="${foo%/*}"

echo $BASE_PATH
if [ $# -lt 1 ]; then
    echo '请输入要运行的py脚本名称'
    exit 0
fi

SCRIPT=$1
#pythonpath搞一搞
export PYTHONPATH=$BASE_PATH

#加上文件锁,保证单实例运行
LOCK_FILE=$BASE_PATH/script/$SCRIPT.lock
if [ -f $LOCK_FILE ]; then
	echo "锁文件存在，直接退出" >> $BASE_PATH/script/$SCRIPT.log
	exit 0
else
	touch $LOCK_FILE
	cd $BASE_PATH
	python ./script/$SCRIPT.py >> ./script/$SCRIPT.log 2>&1 &
	#python ./script/$SCRIPT.py
	rm $LOCK_FILE
fi
