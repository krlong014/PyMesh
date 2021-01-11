import numpy as np
from LoadableMesh import *
from Mesh1D import *
import scipy.sparse as sp

class UniformRefinementSequence:

  def __init__(self, coarse, numLevels, verb=0):

    if coarse.dim==1:
      refiner = UniformLineRefinement
    elif coarse.dim==2:
      refiner = UniformTriangularRefinement
    else:
      raise ValueError('mesh dimension %d not supported' % dim)

    self.meshes = []
    self.meshes.append(coarse)
    self.updates = []
    self.downdates = []

    for i in range(1,numLevels):
      fine, up, down = refiner(self.meshes[i-1], verb)
      self.meshes.append(fine)
      self.updates.append(up)
      self.downdates.append(down)

  def numLevels(self):
    return len(self.meshes)

  def mesh(self, i):
    return self.meshes[i]

  def update(self, i):
    return self.updates[i]

  def downdate(self, i):
    return self.downdates[i]


  def makeMatrixSequence(self, fineA):
    L = len(self.meshes)
    seqA = [None]*L
    seqA[L-1]=fineA
    for i in reversed(range(L-1)):
      eqA[i]=self.downdates[i]*self.seqA[i+1]*self.updates[i]
    return seqA

  def makeVectorSequence(self, fine_b):
    L = len(self.meshes)
    seq_b = [None]*L
    seq_b[L-1]=fine_b
    for i in reversed(range(L-1)):
      seq_b[i]=self.downdates[i]*self.seq_b[i+1]
    return seq_b

# ---------------------------------------------------------------------------
# Test code



if __name__=='__main__':

  from VTKWriter import *
  from TriangleMeshReader import *
  from math import pi, sin
  import numpy.linalg as la

  reader = TriangleMeshReader('../Geometry/oneHole.1')
  mesh = reader.getMesh()

  numLevels = 4

  URS = UniformRefinementSequence(mesh, numLevels)

  fEx = [None]*numLevels
  fUp = [None]*numLevels
  fDown = [None]*numLevels

  print('-- loading fEx and fUp')
  for i in range(numLevels):
    mesh_i = URS.mesh(i)
    f = np.zeros(len(mesh_i.verts))
    for j,p in enumerate(mesh_i.verts):
      f[j] = sin(pi*p[0])*sin(pi*p[1])
    fEx[i]=f

    if i>0:
      fUp[i] = URS.update(i-1)*fUp[i-1]
    if i==numLevels-1:
      fDown[i] = f
    else:
      fUp[i] = f

  print('-- loading fDown')

  for i in reversed(range(numLevels-1)):
    fDown[i] = URS.downdate(i)*fDown[i+1]

  for i in range(numLevels):
    upErr = la.norm(fEx[i]-fUp[i])/len(URS.mesh(i).verts)
    downErr = la.norm(fEx[i]-fDown[i])/len(URS.mesh(i).verts)
    print('%6d up err = %10.3g down err = %10.3g' % (i, upErr, downErr))

  print('-- writing')
  for i in range(numLevels):
    outfile = open('refine.%d.vtu' % i, 'w')
    w = VTKWriter(outfile)
    w.addMesh(URS.mesh(i))
    w.addField('fEx', fEx[i])
    w.addField('fUp', fUp[i])
    w.addField('fDown', fDown[i])
    w.write()
