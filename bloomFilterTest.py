

from pybloom.pybloom import BloomFilter

import bitarray
import numpy as np
from sklearn import linear_model
from scipy.linalg import solve

f = BloomFilter(capacity=60, error_rate=0.30)

[f.add(x) for x in range(50)]

# print(9 in f)
# print('num of key: '+str(len(f)))
print(f.bitarray) #the final array
# f.add('10')
# print(f.bitarray)
# print(len(f.bitarray))
print(f.num_bits) #bloomFilter's size(length)
#
# a = bitarray.bitarray('0'*10)
# print(a)

print(f.keyhash(5))
#
#
#
# a = np.mat(np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 1, ]]).T)
# y = np.mat(np.array([1, 1, 2, 2])).T
#
# num = np.mat(np.array([1, 1, 2])).T
#
# print(a)
# print(y)
#
# aa = np.mat(np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]).T)
# yy = np.mat(np.array([1, 1, 2])).T
# print(solve(aa,yy))
#
# print()
# print(a @ num)
#
# print(a.I @ y)
#
# reg = linear_model.Lasso(alpha=0.001,positive=True)
# reg.fit(a,y)
# print(reg.coef_)