#！/bin/bash

pid_file="./bot.pids"
log_file="./bot.log"
conda_python_bin="/home/$USER/miniconda3/envs/django/bin/python3"

kill_now(){
    cat $pid_file|xargs kill -9
    rm $log_file
}

start_new(){
    $conda_python_bin ./bot_dispatch/manage.py runserver localhost:7710 >> $log_file 2>&1 & echo $! > $pid_file
}

option=$1

if [ $option == "--reload" ]; then
    kill_now
    start_new
    echo "reload done"
elif [ $option == "--stop" ]; then
    kill_now
    echo "stop done"
elif [ $option == "--start" ]; then
    start_new
    echo "start done"
else
    echo "Wrong option!"
fi
