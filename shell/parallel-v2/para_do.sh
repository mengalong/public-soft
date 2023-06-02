#! /bin/bash
SSH="ssh -o StrictHostKeyChecking=no -o ConnectTimeout=3 -n "
SCP="scp -o StrictHostKeyChecking=no -o ConnectTimeout=3  "
tempfifo=$$.fifo
batch_num=20
data_list=$1
mkdir -p log/agent.log

trap "exec 1000>&-;exec 1000<&-;exit 0" 2
mkfifo $tempfifo
exec 1000<>$tempfifo
rm -rf $tempfifo

#for ((i=1; i<=$batch_num; i++))
for i in `seq 1 $batch_num`
do
	echo >&1000
done
back_tm=`date +%Y%m%d`
function check_alive()
{
	mac=$1
	$SSH $mac "hostname" &>/dev/null
	if [ $? -ne 0 ]
	then
		echo "[ERROR] $mac dead" >>log/get_conf.log
		return 1
	fi
	return 0
}

function do_it()
{
	line=$1
	st=`date +%Y-%m-%d_%H:%M:%S`
	back_path="/home/backup/cz-$back_tm"
	$SSH $line "mkdir -p $back_path"
	if [ $? -ne 0 ]
	then
		echo "[ERROR] machine $line is dead" 
		return
	fi
	$SCP get_single.sh $line:$back_path
	$SCP todolist-new/$line $line:$back_path
	$SSH $line "cd $back_path && bash get_single.sh $line"
	$SCP $line:$back_path/data.$line.tar.gz data/
	et=`date +%Y-%m-%d_%H:%M:%S`
	if [ $? -eq 0 ]
	then
		echo "[SUCCESS] $st $et $line "
	else
		echo "[FAILED] $st $et $line "
	fi
}

for data in `cat $data_list`
do
	read -u1000
	{
		echo "[`date +%H:%m:%S`] start $data"
		do_it $data
		echo >&1000
	} &
done

wait
echo "all done!!"
