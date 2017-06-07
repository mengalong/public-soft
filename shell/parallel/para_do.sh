#! /bin/bash
tempfifo=$$.fifo

if [ $# -eq 3 ] 
then
	batch_num=$1
	max_times=$2
	cmd=$3
else
    echo "Error! Not enough params."
    echo "Sample: bash para_do.sh 10 100 '\$cmd'"
    exit 2;
fi


trap "exec 1000>&-;exec 1000<&-;exit 0" 2
mkfifo $tempfifo
exec 1000<>$tempfifo
rm -rf $tempfifo

for ((i=1; i<=$batch_num; i++))
do
    echo >&1000
done

start_time=0
while [ $start_time -lt $max_times ]
do
	echo "$start_time start..."
    read -u1000
    {
		$cmd
		echo >&1000
    } &
	echo "$start_time end..."
	((start_time++))
done

wait
echo "all done!!"
