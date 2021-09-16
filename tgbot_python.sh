#！/bin/bash

pid_file="pids.tgbot"
conda_python_bin="/root/miniconda3/envs/django/bin/python3"

kill_now(){
    cat $pid_file|xargs kill -9
}

start_new(){
    $conda_python_bin ./bot_dispatch/manage.py runserver localhost:7710 >> ./tgbot.log 2>&1 & echo $! > $pid_file
}

option=$1

if [ $option == "reload" ]; then
    kill_now
    start_new
    echo "reload done"
elif [ $option == "stop" ]; then
    kill_now
    echo "stop done"
elif [ $option == "start" ]; then
    start_new
    echo "start done"
else
    echo "Wrong option!"
fi
