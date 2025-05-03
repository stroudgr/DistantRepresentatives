import math
#from DistantRepresentativesDiscs import Disc
#from DistantRepresentativesRectangles import Rectangle
from Matching import BipartiteGraph

def LInf(a,b):
    return max(abs(a[0]-b[0]), abs(a[1]-b[1]))

def LOne(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def LTwoSquared(a,b):
    return (a[0]-b[0])**2 + (a[1]-b[1])**2



# Inheritance for the problem based off of the norm
# that did not get implemented.

"""
def getDistanceRepresentatives(O, norm=LInf):
    if type(O) == Discs:
        return DistantRepresentativesDiscs().getDistanceRepresentatives(O, norm)
    elif type(O) == Rectangle:
        return DistantRepresentativesRectangles().getDistanceRepresentatives(O, norm)
    else:
        raise NotImplementedError


class DistantRepresentatives(object):

    def __init__(self):
        pass

    def Placement(self, O, delta, norm=LInf):
        pass

    def getDistanceRepresentatives(O, norm=LInf):
        pass
"""