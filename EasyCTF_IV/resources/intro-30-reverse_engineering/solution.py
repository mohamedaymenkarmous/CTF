#!/usr/bin/env python3
import binascii
key = "graAhogG"
flag="6513c2b1c2bac3835f0cc28a5b6ac2abc2b9c2bfc381c39b7613c3bac2b3c2a17f7ac29f00c3aa46c2b9c2a6"
def mystery(s):
    r = ""
    # Adding this line
    t = binascii.unhexlify(s).decode("utf-8")
    for i, c in enumerate(t):
        r += chr(ord(c) ^ ((i * ord(key[i % len(key)])) % 256))
    return bytes(r, "utf-8")

print(mystery(flag))
