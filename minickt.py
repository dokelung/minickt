#!/usr/bin/python

import sys
import os
import minickt.cmdManager as cmdManager

if __name__=='__main__':
    shell = cmdManager.Shell()
    if len(sys.argv)>1:
        if sys.argv[1]=='-f':
            script_file = sys.argv[2]
            with open(script_file,'r') as reader:
                for line in reader:
                    line = line.strip()
                    print '-------------------------'
                    print 'EXC({0})'.format(line)
                    print '-------------------------'
                    shell.excCmd(line)
            shell.cmdloop()
    else:
        shell.cmdloop()
