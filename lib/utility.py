#!/usr/bin/env python3
import os
import sys
import textwrap
from pathlib import Path
from pprint import pprint
import subprocess
LOGFILE='__log__'
def log(*args):
    for item in args:
        LOG.write(str(item) + '\n')

def run(*args):
    args = list(args)
    obj = subprocess.run(args, capture_output=True)
    return obj
class Namespace:
    pass
def readlines(path):
    with open(path) as path:
        return path.readlines()



def chop( o, sep ):
    ii = o.find(sep)
    if ii < 0: ii = len(o)
    return o[:ii], o[ii+len(sep):]

class InsituContext:
    def __init__(self, path):
        self._path = path
        assert self._path.is_dir()
        self._home = os.getcwd()
    def __enter__(self):
        os.chdir(self._path)
    def __exit__(self,*a,**b):
        os.chdir(self._home)


