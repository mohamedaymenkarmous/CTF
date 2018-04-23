from ctypes import c_uint32
from random import randint

l = lambda x, y: (((x) << ((y) & 31)) | ((x) >> (32 - ((y) & 31))))
r = lambda x, y: (((x) >> ((y) & 31)) | ((x) << (32 - ((y) & 31))))

def encrypt(x, k):
	k0 = c_uint32(k[0])
	k1 = c_uint32(k[1])
	x0 = c_uint32(x[0])
	x1 = c_uint32(x[1])

	for i in xrange(16):
		k0.value += 0x9E3779B9
		k1.value -= 0x9E3779B9
		x0.value ^= k0.value;
		x0.value += x1.value;
		x0.value = l(x0.value, x1.value);
		x1.value = r(x1.value, x0.value);
		x1.value -= x0.value;
		x1.value ^= k1.value;
	k0.value = x0.value
	x0.value = x1.value
	x1.value = k0.value
	return x0.value, x1.value

if __name__ == "__main__":
	key = [0x7cd85b03, 0x6e3f9ab8]
	x = [randint(0, 0xFFFFFFFF), randint(0, 0xFFFFFFFF)]
	flag = 'hackfest{'+str(x[0])+'_'+str(x[1])+'}'
	c1, c2 = encrypt(x,key)
	print c1, c2

#output : 1483216484 4251556088