#!/usr/bin/env python3
import utility as U
import textwrap

class GitStatExc(Exception):
    pass
class GitStat:
    def __init__(self,path):
        if not (path/'.git').is_dir():
            raise GitStatExc(path)
        self._path = path
        parts = 'git status --ahead-behind -b -s'.split()
        with U.InsituContext(path):
            self._obj = U.run( *parts )
        self._block = self._obj.stdout.decode()
        self._lines = [ line for line in self._block.split('\n') if line ]
        self._text = '\n'.join(self._lines[1:])
        assert self._lines[0].startswith('## ')
        rest=self._lines[0][3:]
        self._local_branch, rest = U.chop(rest, '...')
        self._remote_name,  rest = U.chop(rest, '/')
        self._remote_branch, rest = U.chop(rest, ' ')
        self._diff = rest
        if self._local_branch.startswith('No commits'):
            self._local_branch = ''
    def dirty(self):
        return bool(self._diff or self._text)
    def report(self):
        print( '' +
            str(self._path).ljust(50)
            , '\t'
            , self._lines[0]
            , f'branch: [{self._local_branch}]'
            , f'dirty:[{self.dirty()}]'
        )
        if self._text:
              print( textwrap.indent( self._text, '\t' ))
    def remote_branch(self):
        return self._remote_branch
    def remote_branch_in_LIST(self,_list):
        return self._remote_branch in _list



