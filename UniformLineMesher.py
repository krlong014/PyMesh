from LoadableMesh1D import *

def UniformLineMesh(a, b, nx):

  mesh = Mesh1D()

  h = (b-a)/float(nx)
  for i in range(nx+1):
    x = a + i*h
    mesh.addVertex(x)

  mesh.setLabel(0, 0, 1)
  mesh.setLabel(0, nx, 2)

  for i in range(nx):
    mesh.addElem(i, i+1)

  return mesh

# --------------------------------------------------------------------------

if __name__=='__main__':
  mesh = UniformLineMesh(0.0, 1.0, 10)
  mesh.dump()
