#!/usr/bin/env python3
# Modified from https://gist.github.com/cdiener/10491632

import sys
from PIL import Image
import numpy as np

# it's me flage!
flag = '<redacted>'

# settings
chars = np.asarray(list(' -"~rc()+=01exh%'))
SC, GCF, WCF = 1/10, 1, 7/4

# read file
img = Image.open(sys.argv[1])

# process
S = ( round(img.size[0]*SC*WCF), round(img.size[1]*SC) )
img = np.sum( np.asarray( img.resize(S) ), axis=2)
img -= img.min()
img = (1.0 - img/img.max())**GCF*(chars.size-1)

arr = chars[img.astype(int)]
arr = '\n'.join(''.join(row) for row in arr)
print(arr)

# hehehe
try:
    eval(arr)
except SyntaxError:
    pass


