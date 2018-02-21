#!/usr/bin/env python3

from Crypto import Random
from Crypto.Random import random
from Crypto.Cipher import AES
from binascii import *

flag = "<redacted>"

BLOCK_SIZE = 16

# Pad m using PKCS#7 
def pad(m):
    p = BLOCK_SIZE - len(m) % BLOCK_SIZE
    return m + p * bytes([p])

# AES encrypt
def encrypt(key, message, mode=AES.MODE_CBC):
    IV = key    # totally a good idea
    aes = AES.new(key, mode, IV)
    return hexlify(IV + aes.encrypt(pad(message))).decode()

key = Random.get_random_bytes(16)
print("The key for this session is: {}".format(key))
print("Input 256 different plaintexts such that:")
print("\t - Each is a binary string")
print("\t - Each has length 256")
print("\t - Input can not be all 0's or all 1's")
print("\t - Let Pi denote the ith plaintext input. Then P0 ^ P1 ^ ... ^ P255 = encrypt(key, P0) ^ encrypt(key, P1) ^ ... ^ encrypt(key, P255)")

xor_1 = 0
xor_2 = 0

inputs = set()
for _ in range(256):
    i = input("Input plaintext {}:\t".format(_))
    
    if i in inputs or len(i) != 256 or not set(i) == set('01'):
        print("Input error")
        xor_1 = 0
        xor_2 = 1
        break

    inputs.add(i)
    
    input_dec = int(i, 2)
    xor_1 ^= input_dec
    
    t = hex(input_dec).lstrip("0x").rstrip("l")
    if len(t) & 1:
        t = unhexlify("0" + t)
    else:
        t = unhexlify(t)
        
    xor_2 ^= int(encrypt(key, t), 16)

if xor_1 == xor_2:
    print(flag)
else:
    print("Try again")

