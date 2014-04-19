#! /usr/bin/env python
# import serpent
import subprocess
import sys
sys.path.insert(0, './serpent')
from serpent import compiler

def compile(f):
  t = open(f).readlines()
  i = 0
  while 1:
      o = []
      while i < len(t) and (not len(t[i]) or t[i][0] != '='):
          o.append(t[i])
          i += 1
      i += 1
      print '================='
      text = '\n'.join(o).replace('\n\n','\n')
      # print text
      ast = compiler.parse(text)
      print "AST:"
      print ast
      print ""
      aevm = compiler.compile_to_assembly(text)
      print "AEVM:"
      print ' '.join([str(x) for x in aevm])
      print ""
      s = open(f).read()
      code = compiler.compile(text)
      # code = compiler.decode_datalist(compiler.encode_datalist(ast))
      print "Output:"
      print "0x" + code.encode('hex') #' '.join([str(x) for x in aevm])
      print ""
      print "Int:"
      asint = int(code.encode('hex'), 16)
      print asint
      print ""
      aslist = compiler.decode_datalist("0x" + code.encode('hex'))
      print "Datalist of size %d:" % len(aslist)
      print aslist
      print ""
      print "Hex:"
      ascode = compiler.encode_datalist(aslist)
      print ascode
      if i >= len(t):
          break

print '\n'
print '==================='
print 'Compiler tests'
print '==================='
subprocess.call(["python", "serpent/runtests.py"])

print '\n'
print '==================='
print 'EtherEx simulations'
print '==================='
subprocess.call(["cll-sim/run.py", "simulations/etherex.py"]) # , "contracts/etherex.cll"])

print '\n'
print '==================='
print 'EtherEx LVM'
print '==================='
# subprocess.call(["serpent", "compile", "contracts/etherex.ser"])

print 'XETH'
f = 'contracts/xeth.ser'
compile(f)
print '\n'

print 'Balances'
f = 'contracts/balances.ser'
compile(f)
print '\n'

print 'EtherEx'
f = 'contracts/etherex.ser'
compile(f)

print '==================='
print 'WARNING: Experimental code, use at your own risks.'
print '==================='