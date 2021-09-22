#!/usr/bin/env python3
import textwrap
import utility as U

def log_pass(obj) : print( f'[  ok  ] found:   [{obj.name()}]' )
def log_miss(obj) : print( f'[ ---- ] missing: [{obj.name()}]' )
def log_fail(obj) : print( f'[ fail ] missing: [{obj.name()}]' )

def handle_found(obj):
    log_pass(obj)

def handle_notfound(obj):
    log_miss(obj)
    result = obj.clone()
    pretty_run_result(result, indent=12) # this prints the result
    if result.returncode == 0:
        log_pass(obj)
    else:
        log_fail(obj)

def mywrap(text, indent):
    if text: return text and textwrap.indent( text, indent, lambda line:True )
    else:    return ''

def pretty_run_result(proc, indent=0):
    def print_indent_nonempty(text, prefix):
        if text: print( textwrap.indent(text, prefix) )
    def thunkwrap(proc):
        thunk=U.Namespace()
        thunk.args          = type(proc.args)==type('') and proc.args or ' '.join(proc.args)
        thunk.returncode    = f'[{proc.returncode}]'
        thunk.stdout        = proc.stdout.decode()
        thunk.stderr        = proc.stderr.decode()
        thunk.args          = mywrap( thunk.args        , '// arg:        ' )
        thunk.returncode    = mywrap( thunk.returncode  , '// returncode: ' )
        thunk.stdout        = mywrap( thunk.stdout      , '// stdout:     ' )
        thunk.stderr        = mywrap( thunk.stderr      , '// stderr:     ' )
        return thunk
    thunk = thunkwrap(proc)
    indent = ' '*indent
    print_indent_nonempty( thunk.args       , indent  )
    print_indent_nonempty( thunk.returncode , indent  )
    print_indent_nonempty( thunk.stdout     , indent  )
    print_indent_nonempty( thunk.stderr     , indent  )

if 0 and "IMPLEMENT THIS SOON:":
  class ____ProcWrap:
    def __init__(self,proc):
        self._proc
        self.args        = type(proc.args)==type('') and proc.args or ' '.join(proc.args)
        self.returncode  = proc.returncode
        self.r_out = proc.stdout.decode()
        self.r_err = proc.stderr.decode()
        self.w_cmd = mywrap( self.r_cmd , '// cmd:        ' )
        self.w_ret = mywrap( self.r_ret , '// ret:        ' )
        self.w_out = mywrap( self.r_out , '// out:        ' )
        self.w_err = mywrap( self.r_err , '// err:        ' )
    def wrapped(s):
        parts = [s.w_cdm, s.w_ret, s.r_out, s.w_err]

