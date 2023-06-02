
filename=$1
rm -fr data
rm -fr data.$filename.tar.gz
mkdir -p data
while read line
do
	app_name=`echo $line | awk -F# '{print $2}'`
	ip=$filename
	file=`echo $line | awk -F# '{print $NF}'`
	base_path=`dirname $file`
	dest_path="data/unit-files/$app_name/$ip/$base_path"
	mkdir -p $dest_path
	st=`date +%Y-%m-%d_%H:%M:%S`
	cp $file $dest_path
	if [ $? -ne 0 ]
	then
		echo "[ERROR] $st miss file $line" >>data/get_conf.log.$ip
	else	
		echo "[SUESS] $st $line" >>data/get_conf.log.$ip
	fi
done<$filename

tar czvf data.$filename.tar.gz data &>create_tar.log
