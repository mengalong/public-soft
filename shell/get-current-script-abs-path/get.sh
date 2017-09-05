#!/bin/bash

SOURCE="$0"
while [ -h "$SOURCE"  ];
do
    current_path="$( cd -P "$( dirname "$SOURCE"  )" && pwd  )"
    SOURCE="$(readlink "$SOURCE")"
    [[ $SOURCE != /*  ]] && SOURCE="$current_path/$SOURCE"
done
current_path="$( cd -P "$( dirname "$SOURCE"  )" && pwd  )"

echo $current_path
