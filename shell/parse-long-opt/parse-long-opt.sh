#!/bin/bash
## parse arguments and options
LONGOPTS="index_type:,index_num:,key:,help"
PROGNAME="$0"
SHORT="t:n:k:h"
TEMP=`getopt --options ${SHORT} --longoptions ${LONGOPTS} --name ${PROGNAME} -- "$@"`
[ $? -ne 0 ] && usage && exit 1

eval set -- "$TEMP"
while true ; do
	case "$1" in
		-t|--index_type) INDEX_TYPE="$2"; shift 2;;
		-n|--index_num) INDEX_NUM="$2"; shift 2;;
		-k|--key) KEY="$2";shift 2;;
		--) shift;break;;
		-h|--help) usage;shift;;
		?) usage; exit 1;shift;;
	esac
done

echo "INDEX_TYPE:$INDEX_TYPE"
echo "INDEX_NUM:$INDEX_NUM"
echo "KEY:$KEY"

