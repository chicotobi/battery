from numpy import array
from scipy import sparse
from scipy.sparse import linalg
import pypardiso

nx = 100
ny = 1
nz = 1

def f_idx(nx,ny,nz):
  def f(x,y,z):
    x = x%nx
    y = y%ny
    z = z%nz
    return z*ny*nx + y*nx + z
  return f

idx = f_idx(nx,ny,nz)

i = []
j = []
v = []
for x in range(nx):
  for y in range(ny):
    for z in range(nz):
      i += [idx(x,y,z)]

for k in range(1,n-1):
  i += [k,k,k]
  j += [k-1,k,k+1]
  v += [1,-2,1]
i += [n-1,n-1]
j += [n-2,n-1]
v += [1,-1]

i = array(i)
j = array(j)
v = array(v)*n

A = sparse.coo_matrix((v,(i,j)),shape=(n,n)).tocsr()

A.toarray()

b = array(list(range(n)))/n/n

x = linalg.spsolve(A, b)
x2 = pypardiso.spsolve(A,b)

import matplotlib.pyplot as plt

plt.plot(x,'.-')
