#!/usr/bin/python

import re

# s1 xor s2
def sxor(s1, s2):
 return "".join([chr(ord(c1) ^ ord(c2)) for (c1,c2) in zip(s1,s2)])

# repeat s many time until the max length m
def rep(s, m):
    a, b = divmod(m, len(s))
    return s * a + s[:b]

# Open the encrypted file
f=open("keyed_xor.txt","r").read()

# Open the wordlist
f2=open("words.txt","r").readlines()

# For each word in the wordlist (searching for the first part of the xor key)
for x in f2:
  # If ( encrypted_file xor "easyctf{" ) starts with the selected word from the worlist 
  if x.strip().startswith(sxor(f,"easyctf{")):
    # It can be the first part of the xor key
    # For each word in the wordlist (searching for the second part of the xor key)
    for y in f2:
      # we compute : encrypted_file xor ( (word1+word2) repeated to the encrypted_file length)
      xored2=sxor(f,rep(x.strip()+y.strip(),len(f)))
      # We extract the alpha-numeric string inside the "easyctf{...}"
      found=re.search('^[a-zA-Z0-9_\-]+$',xored2[8:-1])
      # If the xored string ends with "}" and inside the "easyctf{...}" we found an alpha-numeric string
      if xored2.endswith("}")  and found is not None:
        # Youpi ! it's probably a flag
        print x.strip(),y.strip(),"\t => ",xored2

