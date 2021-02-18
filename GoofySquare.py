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


def GoofySquare1():

  verts = (
    [0.0, 0.0], [0.25, 0.0], [0.5, 0.0], [0.75, 0.0], [1.0, 0.0],
    [0.0, 0.5], [0.25, 0.5], [0.5, 0.5], 
    [0.0, 1.0], [0.25, 1.0], [0.5, 1.0], [0.75, 1.0], [1.0, 1.0]
  )

  elems = (
    (0,1,6), (0,6,5), (1,2,7), (1,7,6), (2,3,7), (3,11,7), (3, 12, 11),
    (3, 4, 12), (7, 11, 10), (6, 7, 10), (6, 10, 9), (6, 9, 8), (5,6,8)
  )

  sides = findSides(elems)

  mesh = LoadableMesh2D()

  for v in verts:
    mesh.addVertex(v)

  for s in sides:
    mesh.addSide(s[0], s[1], 0)

  for e in elems:
    mesh.addElem(e[0], e[1], e[2])


  return mesh


if __name__=='__main__':

  mesh = GoofySquare1()

  from MPLMeshViewer import MPLMeshViewer

  viewer = MPLMeshViewer()
  viewer.show(mesh)
