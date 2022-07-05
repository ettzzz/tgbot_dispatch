
#！/bin/bash
# DO NOT USE SPYDER TO EDIT SHELL FILES

pid_file="pids.uvicorn"

kill_now(){
    cat $pid_file|xargs sudo kill -9
}

start_new(){
    uvicorn main:app --port 7710 >> ./uvicorn.log 2>&1 & echo $! > $pid_file
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
