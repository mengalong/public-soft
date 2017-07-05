#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import re
import time

def print_help(cmd):
    print 'Usage: '
    print '  python %s 100MB' % cmd
    print '  python %s 1GB' % cmd

if __name__ == "__main__":
    if len(sys.argv) == 2:
        pattern = re.compile('^(\d*)([M|G]B)$')
        match = pattern.match(sys.argv[1].upper())
        if match:
            num = int(match.group(1))
            unit = match.group(2)
            if unit == 'MB':
                s = ' ' * (num * 1024 * 1024)
            else:
                s = ' ' * (num * 1024 * 1024 * 1024)

            while True:
                time.sleep(1)
        else:
            print_help(sys.argv[0])
    else:
        print_help(sys.argv[0])


