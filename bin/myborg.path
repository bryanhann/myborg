#!/usr/bin/env python3
import os
import sys
import argparse
parser=argparse.ArgumentParser()
arg=(sys.argv+[''])[1]
parser.add_argument( 'cmd', nargs='*' )
ARGS=parser.parse_args()
PATH=os.environ['PATH']
PARTS=PATH.split(':')

USAGE="""\
USAGE:
    borg-path SUBCOMMAND

SUBCOMMANDS:
    list    - list components of PATH
    clean   - echo a PATH with duplicates removed
    help    - this help
"""

def nodups4list(_list):
    acc = []
    for item in _list:
        if not item in acc:
            acc.append(item)
    return acc

def cmd_help(*args): print(USAGE)
def cmd_list(*args): list(map(print,PARTS))
def cmd_clean(*args): print(':'.join(nodups4list(PARTS)))
def cmd_remove(*args): print( ':'.join( [part for part in PARTS if not part in args] ) )
def main():
    try: cmd=eval('cmd_' + ARGS.cmd.pop(0) )
    except NameError: cmd=cmd_help
    except IndexError: cmd=cmd_help
    cmd(*ARGS.cmd)

if __name__=='__main__':
    main()
