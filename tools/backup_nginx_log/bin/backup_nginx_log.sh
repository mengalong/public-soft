#!/bin/bash
current_dir=$(cd `dirname $0` && pwd)

mkdir -p $current_dir/../log/
exec 2>$current_dir/../log/back.log
export PS4='+ [${BASH_SOURCE[0]}:$LINENO ${FUNCNAME[0]} \D{%F %T}] '
set -x

# config
# 日志文件所在路径
log_path="/data1/shuangyi/www/logs/shuangyi/"

# 需要备份的文件名，多个文件用空格分隔
log_filenames="access.log nginx_error.log"

# 目标的备份路径
dest_path="/data1/shuangyi/www/logs/shuangyi/backup"

# nginx所在路径
nginx_bin="/usr/bin/nginx "

# 切割备份后的文件保留的天数
delay_delete=365

# 异常告警的手机号，多个手机号用逗号分隔
phone_list="13088888888"

# 本地发短信的接口,如果没有这一项设置为空即可
GSMSEND="/root/opbin/sms/gsmsend "

# config end

# can not modify
timestamp=`date +%Y%m%d-%H%M%S`

mkdir -p $dest_path

function do_backup_file()
{
	filename=$1
	if [ -f $log_path/$filename ]
	then
		mv $log_path/$filename $dest_path/${filename}.$timestamp
	fi
}

function reload_nginx()
{
	$nginx_bin -s reload
}

function do_backup_logs()
{
        mkdir -p $dest_path
	for item in $log_filenames
	do
		do_backup_file $item
		ret=$?
		if [ $ret -ne 0 ]
		then
			return $ret
		fi
	done
}

function do_send_error_message()
{
	content="$1"
	if [ -f $GSMSEND ]
	then
		$GSMSEND $phone_list "$content"
	fi
}

function clean_log()
{
	find $dest_path -type f -ctime +$delay_delete | xargs -l rm -fv
}
function main()
{
	do_backup_logs
	ret=$?
	if [ $ret -ne 0 ]
	then
		do_send_error_message "backup the log failed [`hostname`]"
		exit 1
	fi

	reload_nginx
	ret=$?
	if [ $ret -ne 0 ]
	then
		do_send_error_message "reload nginx failed [`hostname`]"
	fi

	clean_log
}

main
