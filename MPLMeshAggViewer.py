import matplotlib.pyplot as plt
import numpy as np
from math import sqrt
from LoadableMesh2D import *
import random

# --------------------------------------------------------------------------
# A class for writing annotated meshes to Matplotlib.
#
# Katharine Long, Sep 2020
# For Math 5344
# --------------------------------------------------------------------------

def getDistinctColors(n):
    colors = []
    for i in range(n):
        color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])]
        colors.append(color[0])
    return colors

class MPLMeshAggViewer:

    def __init__(self, aggregates=[], fontSize=16, vertRad=0.06, colors=None):
        self.fontSize = fontSize
        self.vertRad = vertRad
        self.aggregates = aggregates
        if colors is None:
            self.colors = getDistinctColors(len(aggregates))
        else:
            self.colors = colors

    def show(self, mesh):
        ax = plt.axes()

        for i,v in enumerate(mesh.verts):
            vertColor = 'lightgray'
            # Calculate vertColor
            for j,c in enumerate(self.aggregates):
                if i in c:
                    vertColor = self.colors[j]

            self.addVert(ax, i, v, vertColor=vertColor)

        for i,e in enumerate(mesh.elems):
            self.addElem(ax, mesh, i, e)

        ax.set_aspect('equal')
        ax.autoscale_view()

        plt.show()

    def save(self, mesh, fname):
        ax = plt.axes()

        for i,v in enumerate(mesh.verts):
            vertColor = 'white'
            # Calculate vertColor
            for j,c in enumerate(self.aggregates):
                if i in c:
                    vertColor = self.colors[j]

            self.addVert(ax, i, v, vertColor=vertColor)

        for i,e in enumerate(mesh.elems):
            self.addElem(ax, mesh, i, e)

        ax.set_aspect('equal')
        ax.autoscale_view()
        figure = plt.gcf()
        figure.set_size_inches(8,8)
        plt.savefig(fname, dpi=100)

    def addVert(self, ax, index, xy, vertColor='lightgray'):
        circle = plt.Circle(xy, radius=self.vertRad, fc=vertColor, ec='black')
        ax.add_patch(circle)
        ax.annotate(index.__str__(), xy, ha='center',
            va='center', fontsize=self.fontSize)

    def addElem(self, ax, mesh, index, abc):
        A = np.array(mesh.verts[abc[0]])
        B = np.array(mesh.verts[abc[1]])
        C = np.array(mesh.verts[abc[2]])

        pairs = [[abc[0], abc[1]], [abc[1], abc[2]], [abc[2], abc[0]]]

        for p in pairs:
            p.sort()
            q = tuple(p)
            # label = mesh.getSideLabel(q)

            P1 = np.array(mesh.verts[q[0]])
            P2 = np.array(mesh.verts[q[1]])
            P12 = P2-P1
            PUnit = P12/sqrt(np.dot(P12,P12))
            p1 = P1 + self.vertRad*PUnit
            p2 = P2 - self.vertRad*PUnit
            line = plt.Line2D((p1[0],p2[0]), (p1[1], p2[1]),color='black')
            ax.add_line(line)


if __name__=='__main__':

    mesh = TwoElemSquare()

    agg = [{0}, {1}, {2}, {3}]
    viewer = MPLMeshAggViewer(aggregates=agg, vertRad=0.05, fontSize=14)
    viewer.show(mesh)
