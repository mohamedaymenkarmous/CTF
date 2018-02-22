#!/usr/bin/python

from zipfile import ZipFile
import re
import time
import hashlib

def get_pattern():
  file3=open("pattern.txt","r")
  pattern=file3.read().strip()
  file3.close()
  return pattern

def get_hash():
  file3=open("hash.txt","r")
  pattern=file3.read().strip()
  file3.close()
  return pattern


def recursive(R,S,password,filename1,pattern):
  reg=""
  if S[0]=='0':
    reg="0123456789"
  elif S[0]=='a':
    reg="abcdefghijklmnopqrstuvwxyz"
  elif S[0]=='A':
    reg="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  else:
    exit()
  for i in list(reg):
   if get_pattern()==pattern:
    if len(R)==1:
      try:
          zf=ZipFile(filename1)
          old=list(password)
          old[R[0]]=i
          password="".join(old)
          #print password #,filename1,hashlib.sha1(password).hexdigest()
          if get_hash()==hashlib.sha1(password).hexdigest():
            zf.extractall(pwd=password)
            print "First password:",password,"for file:",filename1
      except RuntimeError:
        nop=1
    else:
      old=list(password)
      old[R[0]]=i
      password="".join(old)
      recursive(R[1:],S[1:],password,filename1,pattern)
   else:
    break

zf=ZipFile("begin.zip")
zf.extractall(pwd="coolkarni")

# We have to stop this script manually when this script loops on cracking the password of the same zip file (last file)
while 1:
 file1=open("filename.txt","r")
 filename=file1.read().strip()
 file1.close()
 found=re.search('zip_files/(.*)',filename)
 if found is not None:
  file2=found.group(1).strip()
  pattern=get_pattern()
  hash=get_hash()
  R=[]
  S=[]
  T=list(pattern)
  for i in range(len(T)):
    if T[i]!='_':
      R.append(i)
      S.append(T[i])
  #print R,S
  recursive(R,S,pattern,file2,pattern)

