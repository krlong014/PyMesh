from math import *

class PSLG:
    def __init__(self):
        self.verts = []
        self.edges = []
        self.labels = []
        self.holes = []
        self.vertToIndexMap = {}

    def addVertex(self, vert):
        if not vert in self.vertToIndexMap:
            self.vertToIndexMap[vert] = len(self.verts)
            self.verts.append(vert)
        return self.vertToIndexMap[vert]

    def addEdge(self, startVert, endVert, label):
        startIndex = self.addVertex(startVert)
        endIndex = self.addVertex(endVert)
        self.edges.append( (startIndex, endIndex) )
        self.labels.append(label)

    def addHole(self, point):
        self.holes.append(point)

    def write(self, filename):

        with open(filename, 'w') as f:
            # Vertex section
            f.write('%d 2 0 0\n' % len(self.verts))
            for i,v in enumerate(self.verts):
                f.write('%d %g %g\n' % (i, v[0], v[1]) )

            # edge section
            f.write('%d 1\n' % len(self.edges))
            for i,e in enumerate(self.edges):
                f.write('%d %d %d %d\n' % (i, e[0], e[1], self.labels[i]))

            # hole section
            f.write('%d\n' % len(self.holes))
            for i,h in enumerate(self.holes):
                f.write('%d %g %g\n' % (i, h[0], h[1]))



def makeClosedPoly(pslg, verts, label):

    for n in range(len(verts)):
        if n == len(verts)-1:
            pslg.addEdge(verts[n], verts[0], label)
        else:
            pslg.addEdge(verts[n], verts[n+1], label)


def makeCircle(pslg, center, radius, label, nPts=180):

    verts = []
    for n in range(nPts):
        t = n*2.0*pi/nPts
        x = center[0] + radius*cos(t)
        y = center[1] + radius*sin(t)
        verts.append( (x, y) )

    makeClosedPoly(pslg, verts, label)


if __name__=='__main__':

    pslg = PSLG()
    makeClosedPoly(pslg, [(0,0), (2,0), (2,1), (0,1)], 1)
    makeCircle(pslg, (0.5,0.5), 0.2, 2, 45)
    makeCircle(pslg, (1.5,0.5), 0.2, 3, 45)
    pslg.addHole((0.5,0.5))
    pslg.addHole((1.5,0.5))
    pslg.write('twoHoles.poly')

    pslg = PSLG()
    makeClosedPoly(pslg, [(0,0), (2,0), (2,2), (0,2)], 1)
    makeClosedPoly(pslg, [(0.5,0.5), (1.5,0.5), (1.5,1.5), (0.5,1.5)], 2)
    pslg.addHole((1,1))
    pslg.write('oneHole.poly')
