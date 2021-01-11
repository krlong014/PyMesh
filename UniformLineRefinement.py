import numpy as np
from Mesh1D import *
import scipy.sparse as sp

def UniformLineRefinement(coarse, verb=0):

    coarse = coarse
    fine = Mesh1D()

    numVerts = len(coarse.verts)
    numElems = len(coarse.elems)
    numNewVerts = numVerts + numElems

    updateIndices = []
    updateVals = []


    # -------------------------------------------------------------------
    # ---- Insert new vertices and elements concurrently
    # -------------------------------------------------------------------

    for ie,e in coarse.elems:
      if ie==0:
        fine.addVertex(coarse.verts[0], coarse.vertLabels[0])
        leftID = 0
        updateIndices.append([ie])
        updateVals.append([1.0])
      else:
        leftID = 2*ie
      # new vertex is the midpoint of the old element
      newPos = 0.5*(coarse.verts[ie] + coarse.verts[ie+1])
      midID = fine.addVertex(newPos)
      rightID = fine.addVertex(coarse.verts[ie+1], coarse.vertLabels[ie+1])
      fine.addElem(leftID, midID, coarse.elemLabels[ie])
      fine.addElem(midID, rightID, coarse.elemLabels[ie])

      updateIndices.append([ie, ie+1])
      updateIndices.append([ie+1])

      updateVals.append([0.5, 0.5])
      updateVals.append([1.0])

    print('--- refined mesh --- ')
    fine.dump()

    print('--- update information ---')
    for i,(ind,val) in enumerate(zip(updateIndices, updateVals)):
      print('%6d %20s %20s' % (i, ind, val))

    # -- Refinement is done. Create the prolongation and restriction operators.
    # The update operator uses interpolation. The downdate operator is the
    # normalized transpose of the update operator.

    # build the matrices in DOK form
    update = sp.dok_matrix((numNewVerts, numVerts))
    downdate = sp.dok_matrix((numVerts, numNewVerts))
    for r in range(numNewVerts):
        for c,v in zip(updateIndices[r],updateVals[r]):
            update[r,c]=v
            downdate[c,r]=v

    # Update matrix is ready; convert to CSR
    update = update.tocsr()

    # Normalize the rows of the downdate operator by the row sum.
    # Start by converting to list-of-list format
    downdate = downdate.tolil()
    # normalize rows
    for r in range(numVerts):
        row = downdate.getrowview(r)
        nrm = row.sum()
        row /= nrm

    # Convert to CSR
    downdate = downdate.tocsr()

    return (fine, update, downdate)


# ---------------------------------------------------------------------------
# Test code



if __name__=='__main__':

  from UniformLineMesher import *

  coarse = UniformLineMesh(0.0, 1.0, 4)
  print('--- coarse mesh --- ')
  coarse.dump()
  print('--- refining --- ')

  fine, up, down = UniformLineRefinement(coarse)

  print('--- fine mesh ---')
  fine.dump()

  print('--- update operator ---')
  print(up.todense())

  print('--- downdate operator ---')
  print(down.todense())
