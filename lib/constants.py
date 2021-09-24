import os
from pathlib import Path
import utility as U
import gitstat as G
from pprint import pprint

MYBORG      = Path(os.environ[ 'MYBORG'          ])
MYBORG_MODS = Path(os.environ[ 'MYBORG_MODS'     ])
MANIFEST    = Path(os.environ[ 'MYBORG_MANIFEST' ])
SPACE=' '

class IndexObject:
    def __init__(self,line):
        parts = line.split()
        self._name = parts.pop(0)
        self._url = parts.pop(0)
        self._options = dict()
        try:
            self._stat = self.stat_dst()
        except G.GitStatExc:
            self._stat = None

        if parts:
            assert len(parts) == 2
            flag, val = parts
            assert flag == '-b'
            self._options[flag] = val
    def options_list(self):
        acc=[]
        for flag,val in self._options.items():
            acc.append( flag )
            acc.append( val )
        return acc
    def name(self) : return self._name
    def branch(self): return self._options.get( '-b' )
    def dst(self): return MYBORG_MODS/self.name()
    def url(self): return self._url
    def clone(self):
        acc = [ 'git', 'clone', self.url() ] + self.options_list() + [ str(self.dst()) ]
        return  U.run( *acc )
    def stat_dst(self):
        return G.GitStat(self.dst())
    def dst_remote_branch(self):
        if not self._stat:
            return None
        return self._stat.remote_branch()

    def test_dst(self):
        def branch_test( remote_branch, index_branch ):
            if not remote_branch: return False
            if remote_branch == index_branch : return True
            if remote_branch in ('master','main') and index_branch == None: return True
            return False
        name=self.name()
        rbranch=self.dst_remote_branch()
        ibranch=self.branch()
        ok=branch_test( rbranch, ibranch )
        ret=U.Namespace()
        parts = [
            f'[{name}]'.ljust(35),
            f'rbranch/ibranch: [{rbranch}]/[{ibranch}]',
            f'ok:[{ok}]'
        ]
        line = ' '.join(parts)
        ret.line=line
        ret.ok=ok
        return ret


def index_dict():
    def items():
        prefix = '__myborg_load__ '
        for line in U.readlines( MANIFEST):
            line = line.strip()
            if not line: continue
            if line.startswith('#'): continue
            if not line.startswith( prefix ): continue
            line = line[len(prefix):].strip()
            obj=IndexObject(line)
            yield obj.name(), obj
    global __INDEX_OBJECTS
    try: return __INDEX_OBJECTS
    except NameError: __INDEX_OBJECTS = dict(sorted(items()))
    return __INDEX_OBJECTS
def index_objects(): return index_dict()
def __index():
    lines=U.readlines( MYBORG/'index')
    lines=[ line.strip() for line in lines  ]
    lines=[ line for line in lines if line.startswith( '__myborg_load__' )  ]
    lines.sort()
    acc=dict()
    for line in lines:
        parts=line.split()
        parts.pop(0)
        key = parts.pop(0)
        url = parts.pop(0)
        options = ' '.join(parts)
        acc[ key ] = (url, options)
    return acc

def local():
    acc=dict()
    for path in sorted( MYBORG_MODS.glob('*') ):
        obj=U.Namespace()
        obj._path = path
        try: obj._stat = G.GitStat(path)
        except G.GitStatExc: obj._stat=None
        acc[path.name] = obj
    return acc

#INDEX=index()
INDEX2=index_objects()
LOCAL=local()
MISSING2 = [ name for name in INDEX2.keys() if not name in LOCAL.keys() ]
#MISSING = [ name for name in INDEX.keys() if not name in LOCAL.keys() ]
#EXTRA   = [ name for name in LOCAL.keys() if not name in INDEX.keys() ]
EXTRA2   = [ name for name in LOCAL.keys() if not name in INDEX2.keys() ]

