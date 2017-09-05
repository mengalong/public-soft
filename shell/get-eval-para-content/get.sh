#!/bin/bash

test_para="meng_var"
meng_var="hahah"

target=`eval echo '$'"$test_para"`
echo $target
