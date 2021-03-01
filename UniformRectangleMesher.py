from LoadableMesh2D import LoadableMesh2D

def findSides(elems):

  sides = set()

  for e in elems:
    pairs = ([e[0], e[1]], [e[1], e[2]], [e[2], e[0]])
    for p in pairs:
      p.sort()
      s = tuple(p)
      sides.add(s)

  return sides

def runningVertIndex(nx, ix, iy):
  return ix + (nx+1)*iy

def runningElemIndex(nx, ix, iy):
  return ix + nx*iy


def UniformRectangleMesher(ax, bx, nx, ay, by, ny):


  # create the vertices
  verts = []
  for iy in range(ny+1):
    for ix in range (nx+1):
      x = ax + ix*(bx-ax)/float(nx)
      y = ay + iy*(by-ay)/float(ny)
      verts.append((x,y))

  # create the triangles
  elems = []
  for iy in range(ny):
    for ix in range(nx):
      a = runningVertIndex(nx, ix, iy)
      b = runningVertIndex(nx, ix+1, iy)
      c = runningVertIndex(nx, ix+1, iy+1)
      d = runningVertIndex(nx, ix, iy+1)
      if (ix+iy)%2==0:
        T1 = (a,b,c)
        T2 = (a,c,d)
      else:
        T1 = (a,b,d)
        T2 = (b,c,d)
      elems.append(T1)
      elems.append(T2)

  sides = findSides(elems)

  mesh = LoadableMesh2D()

  for v in verts:
    mesh.addVertex(v)

  for s in sides:
    mesh.addSide(s[0], s[1], 0)

  for e in elems:
    print('adding ', e[0], ' ', e[1], ' ', e[2])
    mesh.addElem(e[0], e[1], e[2])


  return mesh


if __name__=='__main__':

  mesh = UniformRectangleMesher(0.0, 1.0, 5, 0.0, 1.0, 3)

  from MPLMeshViewer import MPLMeshViewer

  C = set([1, 3, 6, 7, 9])
  viewer = MPLMeshViewer()
  viewer.show(mesh, marked=C)
