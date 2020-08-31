#!/usr/bin/python

from pwn import *
import z3
import time

r = remote('secretarray.fword.wtf', 1337)
s=z3.Solver()
print r.recv(1024).decode()
for i in range(0,1337):
  print i
  if i<1336:
    #print "send",str(i)+" "+str(i+1)
    r.send(str(i)+" "+str(i+1)+"\n")
    time.sleep(0.3)
    result=r.recv(1024).strip()
    exec("a"+str(i)+" = z3.Int('a"+str(i)+"')")
    exec("a"+str(i+1)+" = z3.Int('a"+str(i+1)+"')")
    #print "a"+str(i)+"+a"+str(i+1)+"=="+(result if result else "0")
    s.add(eval("a"+str(i))+eval("a"+str(i+1))==(result if result else "0"))
  else:
    #print "send",str(i)+" 0"
    r.send(str(i)+" 0\n")
    result=r.recv(1024).strip()
    exec("a"+str(i)+" = z3.Int('a"+str(i)+"')")
    #print "a"+str(i)+"+a0=="+(result if result else "0")
    s.add(eval("a"+str(i))+a0==(result if result else "0"))

s.check()
#print s
model=s.model()
results="DONE"
#print "model",s.model()
for i in range(0,1337):
  for j in model:
    if str(j)=="a"+str(i):
      #print "a"+str(i),str(int(s.model()[j].as_string()))
      results=results+" "+str(int(s.model()[j].as_string()))
      break

print results.strip()
print "length of the solved system:",len(model)
print "length of the array's results:",(len(results.strip().split(" "))-1)
r.sendline(results.strip())
time.sleep(1)
print r.recv(1024)
time.sleep(1)
print r.recv(1024)
