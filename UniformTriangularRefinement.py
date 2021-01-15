import numpy as np
from LoadableMesh2D import *
import scipy.sparse as sp

def UniformTriangularRefinement(coarse, verb=0):

    coarse = coarse
    fine = LoadableMesh()

    numVerts = len(coarse.verts)
    numEdges = len(coarse.sides)
    numElems = len(coarse.elems)

    numNewVerts = numVerts + numEdges
    numNewEdges = 2*numEdges + 3*numElems
    numNewElems = 4*numElems

    vertDone = np.zeros(numVerts, dtype=np.bool)
    oldEdgeDone = np.zeros(numEdges, dtype=np.bool)
    oldToNewVertexMap = -np.ones(numVerts, dtype=np.int64)
    oldEdgeToNewVertMap = -np.ones(numEdges, dtype=np.int64)

    updateIndices = []
    updateVals = []

    elemVerts = np.zeros([numElems, 6], dtype=np.int64)


    # -------------------------------------------------------------------
    # ---- Insert new vertices and new edges
    # -------------------------------------------------------------------

    # Loop over old elems, inserting each old vertex exactly once and then
    # create insert new vertices at the edge midpoint
    for el in range(numElems):

        curElemVerts = coarse.elems[el]

        if verb>0:
            print('processing old element id=', el, ', verts=', curElemVerts)

        # Put this element's vertices in new mesh
        for i,oldVertID in enumerate(curElemVerts):
            # Add only those vertices that haven't yet been added
            if not vertDone[oldVertID]:
                if verb>0:
                    print('\tadding vertex ID=', oldVertID )
                # Put the vertex in the refined mesh
                newVertID = fine.addVertex(coarse.verts[oldVertID])
                # Record the indices and the weights for the update
                # matrix
                updateIndices.append([oldVertID])
                updateVals.append([1.0])
                elemVerts[el,i]=newVertID
                oldToNewVertexMap[oldVertID]=newVertID
                vertDone[oldVertID] = True
            else:
                elemVerts[el,i]=oldToNewVertexMap[oldVertID]

        # Put new vertices at midpoints of old edges.
        # Use Exodus ordering where new vertex i+3 is
        # opposite vertex i.
        for i,S in enumerate(([1,2], [2,0], [0,1])):
            # Get vertices on current edge, then sort to make a key
            # into old mesh's dictionary of vertices
            s = [curElemVerts[S[0]], curElemVerts[S[1]]]
            s.sort();
            if verb>0:
                print('\tchecking vertex at midpoint of edge=', s )
            sKey = tuple(s)
            oldEdgeIndex = coarse.sideToIndexMap[sKey]
            # Add only those edges that haven't yet been added
            if not oldEdgeDone[oldEdgeIndex]:
                if verb>0:
                    print('\t\tinserting vertex at midpoint of edge=', s )
                # Find midpoint of new edge
                p1 = coarse.verts[s[0]]
                p2 = coarse.verts[s[1]]
                pMid= (0.5*(p1[0]+p2[0]), 0.5*(p1[1]+p2[1]))
                # Put a new vertex at the midpoint
                newVertID = fine.addVertex(pMid)
                if verb>0:
                    print('\t\tnew vertex ID =', newVertID )
                # Associate the new vertex with the current element
                elemVerts[el, 3+i] = newVertID
                # Record the indices and weights for the update matrix
                updateIndices.append(s)
                updateVals.append([0.5, 0.5])
                oldEdgeDone[oldEdgeIndex] = True
                oldEdgeToNewVertMap[oldEdgeIndex]=newVertID

                # Now that we've created the new vertex, add the two
                # new child edges to the new mesh. The children inherit
                # the label of the parent.
                oldLabel = coarse.sideLabels[oldEdgeIndex]
                v0 = oldToNewVertexMap[s[0]]
                v1 = oldToNewVertexMap[s[1]]
                if verb>0:
                    print('\t\tadding new edge ', (v0, newVertID) )
                newEdgeID = fine.addSide(v0, newVertID, oldLabel)

                if verb>0:
                    print('\t\tadding new edge ', (v1, newVertID) )
                newEdgeID = fine.addSide(v1, newVertID, oldLabel)
            else:
                if verb>0:
                    print('\t\treusing vertex at midpoint of edge=', s )
                v = oldEdgeToNewVertMap[oldEdgeIndex]
                elemVerts[el,i+3]=v
                if verb>0:
                    print('\t\treusing vertex at midpoint of edge=', s,
                        ' with ID=', v)

        # Add the new interior edges ([3,5], [3,4], [4,5]). Since these
        # aren't shared between elements, there's no need to check
        # whether they've been done before.
        newEdgeID = fine.addSide(elemVerts[el,3], elemVerts[el,5], 0)
        newEdgeID = fine.addSide(elemVerts[el,3], elemVerts[el,4], 0)
        newEdgeID = fine.addSide(elemVerts[el,4], elemVerts[el,5], 0)

        # -------- Done inserting new vertices and edges

        # ---- Insert child elements
        if verb>0:
            print('\tinserting four child elements')
        v = elemVerts[el,:]
        if verb>0:
            print('\telemVerts are ', v)

        if verb>0:
            print('\t\tadding new elem ', (v[0], v[5], v[4]) )
        fine.addElem(v[0], v[5], v[4])

        if verb>0:
            print('\t\tadding new elem ', (v[1], v[3], v[5]) )
        fine.addElem(v[1], v[3], v[5])

        if verb>0:
            print('\t\tadding new elem ', (v[2], v[4], v[3]) )
        fine.addElem(v[2], v[4], v[3])

        if verb>0:
            print('\t\tadding new elem ', (v[3], v[4], v[5]) )
        fine.addElem(v[3], v[4], v[5])

    # -- Refinemnt is done. Create the prolongation and restriction operators.
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

  from TriangleMeshReader import *

  print('--- coarse --- ')
  coarse = TwoElemSquare()
  coarse.dump()

  fine, up, down = UniformTriangularRefinement(coarse)

  print('--- fine --- ')
  fine.dump()

  print('--- update operator ---')
  print(up.todense())

  print('--- downdate operator ---')
  print(down.todense())
