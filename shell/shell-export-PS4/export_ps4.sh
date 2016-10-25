#!/bin/bash
exec 2>test.log
export PS4='+ [${BASH_SOURCE[0]}:$LINENO ${FUNCNAME[0]} \D{%F %T}] '
set -x

function test_log
{
	echo "here is the test func"
}

function test_record
{
	echo "here is the test record func"
}

test_log
test_record
