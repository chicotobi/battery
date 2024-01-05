from numpy import array, zeros
from scipy import sparse
import pypardiso
import time

nx = 60
ny = 60
nz = 60
n = nx*ny*nz

def f_idx(nx,ny,nz):
  def f(x,y,z):
    x = x%nx
    y = y%ny
    z = z%nz
    return z*ny*nx + y*nx + x
  return f

idx = f_idx(nx,ny,nz)

tau = 0.0001
h = 1/nx

i = []
j = []
v = []
b = zeros((n))
for x in range(nx):
  for y in range(ny):
    for z in range(nz):
      i += [idx(x,y,z)]
      j += [idx(x,y,z)]
      v += [1+6*tau/h/h]
      
      i += [idx(x,y,z)]*6
      j += [idx(x+1,y,z)]
      j += [idx(x-1,y,z)]
      j += [idx(x,y+1,z)]
      j += [idx(x,y-1,z)]
      j += [idx(x,y,z+1)]
      j += [idx(x,y,z-1)]
      v += [-tau/h/h]*6
      
      if (x-nx/2)**2+(y-ny/4)**2 <= nx/5:
        b[idx(x,y,z)] = 1

i = array(i)
j = array(j)
v = array(v)
A = sparse.coo_matrix((v,(i,j)),shape=(n,n)).tocsr()

t0 = time.time()
x2 = pypardiso.spsolve(A,b)
print("pardiso:",time.time()-t0)

import matplotlib.pyplot as plt

if ny==1:
  plt.plot(x,'.-')
elif nz==1:
  x2 = x2.reshape((nx,ny))
  plt.imshow(x2)
else:
  import pyevtk
