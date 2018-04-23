#!/usr/bin/python

from ctypes import c_uint32
from random import randint

l = lambda x, y: (((x) << ((y) & 31)) | ((x) >> (32 - ((y) & 31))))
r = lambda x, y: (((x) >> ((y) & 31)) | ((x) << (32 - ((y) & 31))))

# Initializations
key = [0x7cd85b03, 0x6e3f9ab8]
x = [randint(0, 0xFFFFFFFF), randint(0, 0xFFFFFFFF)]
k0 = c_uint32(key[0])
k1 = c_uint32(key[1])
x0 = c_uint32(0)
x1 = c_uint32(0)

# Setting the result as an input
x0.value=1483216484
x1.value=4251556088

# k0 and k1 must be set to the final value of the executed crypto1.py script
for i in xrange(16):
	k0.value += 0x9E3779B9
	k1.value -= 0x9E3779B9

# We should store the final k0 because at the end of the crypto1.py, k0 was overwritten, and so its value was lost
# But, now we know that to decrypt the ciphertext, we need to use the last k0 and k1, so we should use them into the for loop.
tmp_k0=k0.value

k0.value=x1.value
x1.value=x0.value
x0.value=k0.value

# Restore the last k0 value
k0.value=tmp_k0
for i in xrange(16):
		x1.value ^= k1.value;
		x1.value += x0.value;
		x1.value = l(x1.value, x0.value) & int('0b'+('1'* 32 ),2)
		x0.value = r(x0.value, x1.value) & int('0b'+('1'* 32 ),2)
		x0.value -= x1.value;
		x0.value ^= k0.value;
		k1.value += 0x9E3779B9
		k0.value -= 0x9E3779B9

x[0]=x0.value
x[1]=x1.value

flag = 'hackfest{'+str(x[0])+'_'+str(x[1])+'}'
print flag

