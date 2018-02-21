#!/usr/bin/python
import socket
import time
import re

def calculator(data):
  found=re.search('What is the (.*) of the zip code ([0-9]+)\?',data)
  if found is not None:
    s1=found.group(1)
    s2=found.group(2)
    # Source : https://www.census.gov/geo/maps-data/data/gazetteer2010.html : Zip Code Tabulation Areas
    f=open("Gaz_zcta_national.txt","r").readlines()
    line=""
    # The columns of this file are separeted with many extra blank spaces
    # So we convert all the spaces to one single ","
    for s in f:
      if s.strip().startswith(s2):
        line=re.sub('[ \t]+',',',s.strip())
    print line
    lines=line.split(",")
    if s1 == "land area (m^2)":
      return lines[3]
    elif s1 == "water area (m^2)":
      return lines[4]
    elif s1 == "latitude (degrees)":
      return lines[7]
    elif s1 == "longitude (degrees)":
      return lines[8]
    else:
      print s1,"unknown"
  return;

def netcat(hostname, port):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((hostname, port))
  time.sleep(.5)
  data = s.recv(10240)
  data = s.recv(10240)
  data = s.recv(10240)
  while 1:
    data = s.recv(10240)
    if data == "":
      break
    print "Received:", repr(data)
    result=calculator(data)
    #exit()
    print "Sending",result
    time.sleep(.2)
    s.send(str(result)+"\n")
    time.sleep(.2)
  print "Connection closed."
  s.close()

netcat("c1.easyctf.com", 12483)
