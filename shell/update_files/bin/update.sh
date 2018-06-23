#!/bin/bash

PROGNAME="$0"
CURRENT_PATH="$(cd -P "$(dirname ${PROGNAME})" && pwd)"
TOP_PATH="${CURRENT_PATH}/../"
LOG_PATH="${TOP_PATH}/log"
BACK_PATH="${TOP_PATH}/backup"

timestamp=`date +%Y%m%d%H%M%S`
echo ">>>timestamp:$timestamp"

LONGOPTS="action:,soruce:,dest:,list:,timestamp:,help"
SHORT="a:s:d:l:t:h"
TEMP=`getopt --options ${SHORT} --longoptions ${LONGOPTS} --name ${PROGNAME} -- "$@"`
[ $? -ne 0 ] && usage && exit 1


function usage()
{
    echo "Usage:"
    echo -e "\tupdate:"
	echo -e "\t\t$PROGNAME -a|--action [update|rollback] -s|--source [source_code_path] -d|--dest [dest_path] -l|--list [to_update_file_list] -h|--help"
	echo -e "\trollback:"
	echo -e "\t\t$PROGNAME -a|--action [update|rollback] -t|--timestamp [timestamp] -d|--dest [dest_path] -l|--list [to_update_file_list] -h|--help"
	exit
}

eval set -- "$TEMP"
while true ; do
	case "$1" in
		-a|--action) ACTION="$2"; shift 2;;
		-s|--source) SOURCE_PATH="$2"; shift 2;;
		-d|--dest) DEST_PATH="$2";shift 2;;
		-l|--list) LIST_FILE="$2";shift 2;;
		-t|--timestamp) TIMESTAMP="$2";shift 2;;
		--) shift;break;;
		-h|--help) usage; exit 1;shift;;
		?) usage; exit 1;shift;;
	esac
done

mkdir -p ${LOG_PATH}
mkdir -p ${BACK_PATH}
logfile="${LOG_PATH}/${ACTION}.$timestamp"
backupdir="${BACK_PATH}/$timestamp"
mkdir -p $backupdir

exec 2>$logfile
export PS4='+ [${BASH_SOURCE[0]}:$LINENO ${FUNCNAME[0]} \D{%F %T}] '
set -x


# update.sh -a update -s xxx -d xxx -l list
# update.sh -a rollback -s xxx -d xxx -l list
#
#

#更新时，分为：备份/拷贝，先判断源文件中是否存在以及目标文件是否存在，对于目标文件不存在的需要提示出来
#回滚时，直接拷贝即可
#

function check_list_file()
{
	code_path=$1
	list_file=$2
    echo ">> start check list file"
    if [ ! -f $list_file ]
    then
        echo -e "\t更新列表文件:$list_file 不存在"
        usage;exit 1;
    fi

    if [ ! -s $list_file ]
    then
        echo -e "\t更新列表文件:$list_file 为空"
        usage;exit 1;
    fi

    for line in `cat $list_file`
    do
        target_file=${code_path}/$line
        if  [ -f $target_file ]
        then
            echo -e "\t...Have Got $target_file"
        else
            echo -e "\t... Not Got $target_file"
        fi 
    done

}

function check_source_and_dest()
{
    if [ ! -d $SOURCE_PATH ]
    then
        echo "源路径:$SOURCE_PATH 不存在"
        usage
        exit 1
    fi

    if [ ! -d $DEST_PATH ]
    then
        echo "目标路径:$DEST_PATH 不存在"
        usage
        exit 1
    fi
}

function backup_it()
{
    echo ">>> start to backup file"
    cp $LIST_FILE ${backupdir}/todo.${timestamp}
    for line in `cat $LIST_FILE`
    do
        source_file="${DEST_PATH}/${line}"
        dest_file="${backupdir}/${line}"
        back_path=`dirname $dest_file`
        if [ -f $source_file ]
        then
            mkdir -p $back_path
            cp $source_file $dest_file
            if [ $? -ne 0 ]
            then
                echo -e "\t[Error] backup file:$source_file failed! break down..."
                exit 1;
            fi
        fi
    done
    echo -e "\t[SUCCESS] backup file success"
}

function check_answer()
{
    while [ 1 ]
    do
        echo -ne "\tGo On(Y|N)?:"
        read an
        if [[ x"$an" == x"y" ]] || [[ x"$an" == x"Y" ]]
        then
            return 0
        fi
        if [[ x"$an" == x"n" ]] || [[ x"$an" == x"N" ]]
        then
            return 1
        fi
    done
}
function update_it()
{
    echo ">>> start to update file"
    flag=1
    for line in `cat $LIST_FILE`
    do
        source_file="${SOURCE_PATH}/${line}"
        dest_file="${DEST_PATH}/${line}"
        dest_path=`dirname $dest_file`
        mkdir -p $dest_path
        cp $source_file $dest_file
        if [ $? -eq 0 ]
        then
            echo -e "\t[SUCCESS] update file:$line success!"
            if [ $flag -eq 1 ]
            then
                check_answer
                if [ $? -ne 0 ]
                then
                    cp ${backupdir}/$line $dest_file
                    echo -e "\t Break!"
                    exit
                else
                    flag=2
                fi
            fi
        else
            echo -e "\t[ERROR] update file:$line failed!"
            exit 1
        fi
    done
}

function check_timestamp()
{
    echo ">>> start to check timestamp"
    if [ x"$TIMESTAMP" == x"" ]
    then
        echo "[ERROR] Need timestamp"
        usage
        exit 1;
    fi
}

function rollback()
{
    echo ">>> start to rollback"
    flag=1
    source_path="${BACK_PATH}/$TIMESTAMP"
    todo_list="${source_path}/todo.${TIMESTAMP}"
    for line in `cat $todo_list`
    do
        source_file="${source_path}/${line}"
        dest_file="${DEST_PATH}/${line}"

        if [ ! -f $source_file ]
        then
            echo -e "\t[NOTE] the backup file:$line cannot find"
            continue
        fi
        cp $source_file $dest_file
        if [ $? -eq 0 ]
        then
            echo -e "\t[SUCCESS] rollback file:$line success!"
            if [ $flag -eq 1 ]
            then
                check_answer
                if [ $? -ne 0 ]
                then
                    echo -e "\t Break!"
                    exit
                else
                    flag=2
                fi
            fi
 
        else
            echo -e "\t[ERROR] update file:$line failed!"
            exit 1
        fi
    done
}


if [ x"$ACTION" == x"update" ]
then
    check_source_and_dest
    check_list_file ${SOURCE_PATH} ${LIST_FILE}
    backup_it
    update_it
elif [ x"$ACTION" == x"rollback" ]
then
    check_timestamp
    rollback
else
    usage
fi


