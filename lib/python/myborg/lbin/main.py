#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

def copyall( srcd ):
    dstd=Path(os.environ['MYBORG_LBIN'])
    for src in srcd.glob('*'):
        dst=dstd/src.name
        if src.is_file():
            shutil.copyfile(src,dst)
        if src.is_dir():
            shutil.copytree(src,dst)

