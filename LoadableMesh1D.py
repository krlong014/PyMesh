# --------------------------------------------------------------------------
# A 1D mesh class
#
# Katharine Long, Jan 2021
# For Math 5345
# --------------------------------------------------------------------------

class LoadableMesh1D:

  # Initialize an empty mesh
  def __init__(self):
    # Mesh is 1D
    self.dim = 1

    # mesh points
    self.verts = []

    # mesh elements, stored as pairs of vertices
    self.elems = []

    # map from position to vertex index
    self.vertToIndexMap = {}

    # list of connected elements for each vertex
    self.connectedElemsForVert = []

    # labels for vertices
    self.vertLabels = []

    # labels for elements
    self.elemLabels = []

  def addVertex(self, v, label=0):

    # Ensure that the vertex isn't a duplicate
    if v in self.vertToIndexMap:
        raise RuntimeError('Added vertex (%g) twice' % v)
    else:
        # Assign an index to the new vertex
        vertIndex = len(self.verts)
        # Store the mapping (x,y) <==> index
        self.vertToIndexMap[v] = vertIndex
        self.verts.append(v)
        # Record the label
        self.vertLabels.append(label)
        # Allocate an empty set for the set of connected elements
        self.connectedElemsForVert.append(set())

    # Return the index assigned to this vertex
    return vertIndex

  def addElem(self, a, b, label=0):
    '''a'''

    # Get the index for the new elements
    elemIndex = len(self.elems)

    # store the vertices in a sorted tuple
    abList = [a,b]
    abList.sort()
    ab = tuple(abList)

    # Record the element as the sorted tuple of indices
    self.elems.append(ab)
    self.elemLabels.append(label)

    # for each vertex, record this element in the vertex's set
    # of connected elements
    for v in ab:
      # v is a vertex index
      self.connectedElemsForVert[v].add(elemIndex)

    return elemIndex

  # Set a label for a specified cell
  def setLabel(self, cellDim, cellID, label):
    if cellDim==0:
      self.vertLabels[cellID]=label
    else:
      self.elemLabels[cellID]=label

  # Dump the internal data
  def dump(self):

      print('Vertices: num=%d' % len(self.verts))
      for v,cf,lb in zip(self.verts, self.connectedElemsForVert, self.vertLabels):
        print('\t{:<10.3g} cofacets={:<8} label={}'.format(v, str(cf), lb))

      print('Elements: num=%d' % len(self.elems))
      for e,lb in zip(self.elems, self.elemLabels):
        print('\t{:<20} label={}'.format(str(e), lb))

# ---------------------------------------------------------------------------
def FourElemLine():
  from math import sqrt

  mesh = LoadableMesh1D()

  mesh.addVertex(0.0, 1)
  mesh.addVertex(0.25, 0)
  mesh.addVertex(0.5, 0)
  mesh.addVertex(sqrt(0.5), 0)
  mesh.addVertex(1.0, 1)

  mesh.addElem(0,1)
  mesh.addElem(1,2)
  mesh.addElem(2,3)
  mesh.addElem(3,4)

  return mesh

# ---------------------------------------------------------------------------
# Test code

if __name__=='__main__':

    mesh = FourElemLine()
    mesh.dump()
