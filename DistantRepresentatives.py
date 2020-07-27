import math
from Matching import BipartiteGraph


class Disc(object):
    """docstring for Disc."""

    def __init__(self, cx, cy, R):
        super(Disc, self).__init__()
        self.cx = cx
        self.cy = cy
        self.R = R

    def leftBorder(self):
        return ( self.cx - self.R  )

    def rightBorder(self):
        return ( self.cx + self.R  )

    def upperBorder(self):
        return ( self.cy + self.R  )

    def lowerBorder(self):
        return ( self.cy - self.R  )


#TODO!!!!!***************************
#
def contains_point(d, delta):
    """
    For the given disc d, returns whether grid delta*LAMBDA intersects d.

    Returns:
    (0,None) - if contains a point.
    (1,p, Q) - if hits a grid edge, and p is such a point of intersection
    (2, p, Q) - if within cell, p = d[0,1] = center of disc

    TODO Q are grid points, so make them not delta * point, but just point
    """

    # Outside the square/disc, or touching the edge
    verticalGridLineLeft = (d[0]-d[2]) // delta
    verticalGridLineRight = math.ceil((d[0]+d[2]) / delta)

    # Outside the square/disc, or touching the edge
    horizontalGridLineBelow = (d[1]-d[2]) // delta
    horizontalGridLineAbove = math.ceil((d[1]+d[2]) / delta)

    # touching the edge case vertically
    if (d[0]-d[2]) % delta == 0 or (d[0]+d[2]) % delta == 0:

        # touching the edge case horizontally
        if (d[1]-d[2]) % delta == 0 or (d[1]+d[2]) % delta == 0:
            return (0,None) # corner of the square is a grid point

        # Both outside the square/disc, and at least one horizontal line
        # exists in between.
        if not(horizontalGridLineBelow + 1 < horizontalGridLineAbove):
            return (0, None) # One of the vertical edges has a grid point

        # Hits grid edge, but had no grid points inside
        if (d[0]-d[2]) % delta == 0:
            return (1, (d[0]-d[2], d[1]+d[2]),
                    [(d[0]-d[2], delta*(horizontalGridLineBelow)),
                     (d[0]-d[2], delta*(horizontalGridLineBelow + 1))]  )
        else:    #if(d[1]+d[2]) % delta == 0:
            return (1, (d[0]+d[2], d[1]+d[2]),
                    [(d[0]+d[2], delta*(horizontalGridLineBelow)),
                     (d[0]+d[2], delta*(horizontalGridLineBelow + 1))]  )

    elif verticalGridLineLeft + 1 < verticalGridLineRight: # MIDDLE vertical line exists

        # touching the edge case horizontally
        if (d[1]-d[2]) % delta == 0 or (d[1]+d[2]) % delta == 0:
            return (0, None)# MIDDLE vertical lines intersect horizontalGridLine, which
            # hits the rectangle edge

        # Both outside the square/disc, and at least one horizontal line
        # exists in between.
        if horizontalGridLineBelow + 1 < horizontalGridLineAbove:
            return (0, None) # One of the vertical edges has a grid point

        return (1, (delta*(verticalGridLineLeft + 1), d[1]+d[2]), # Hits grid edge
                    [( delta*(verticalGridLineLeft + 1), delta*(horizontalGridLineBelow) ),
                     ( delta*(verticalGridLineLeft + 1), delta*(horizontalGridLineAbove) ) ] )

    else: #Neither vertical lines touch rect, and nothing inbetween these two lines

        # touching the edge case horizontally
        if (d[1]-d[2]) % delta == 0:
            return (1, (d[0]-d[2] , d[1]-d[2]),
                    [(delta*verticalGridLineLeft,  d[1]-d[2]),
                     (delta*verticalGridLineRight, d[1]-d[2]) ])
        if (d[1]+d[2]) % delta == 0:
            return (1, (d[0]-d[2] , d[1]+d[2]),
                    [(delta*verticalGridLineLeft,  d[1]+d[2]),
                     (delta*verticalGridLineRight, d[1]+d[2]) ])

        if horizontalGridLineBelow + 1 < horizontalGridLineAbove:
            return (1, (d[0]-d[2] , delta*(horizontalGridLineBelow + 1)),
                    [( delta*verticalGridLineLeft,  delta*(horizontalGridLineBelow + 1) ),
                     ( delta*verticalGridLineRight, delta*(horizontalGridLineBelow + 1) )])

        return (2, (d[0], d[1]),
                      [
                       (delta*verticalGridLineLeft,  delta*horizontalGridLineBelow),
                       (delta*verticalGridLineRight, delta*horizontalGridLineBelow),
                       (delta*verticalGridLineRight, delta*horizontalGridLineAbove),
                       (delta*verticalGridLineLeft,  delta*horizontalGridLineAbove)
                      ])

    return False


def inDisc(p, d):
    x, y = p
    cx, cy, R = d
    return cx - R  <= x and x <= cx + R and cy- R  <= y and y <= cy + R

def getGridPointsInDiscStupid(d, delta, Q):
    cx, cy, R = d
    xmin = math.floor((cx-R)/delta)
    xmax = math.ceil((cx+R)/delta)
    ymin = math.floor((cy-R)//delta)
    ymax = math.ceil((cy+R)/delta)

    S = set()
    for i in range(xmin, xmax+1):

        for j in range(ymin, ymax+1):

            if (delta*i, delta*j) not in Q and inDisc((delta*i, delta*j), d):
                S = S.union({(i, j)})

    return S


def getGridPointsInDisc():
    # See Cabello for how to do this efficently
    raise NotImplementedError

def Placement(D, delta):
    Q = set()
    p = [None] * len(D)

    # Booleans telling us is square are "small" or not.
    contains_point_bools = [contains_point(d, delta) for d in D]

    for i,d in enumerate(D):

        if contains_point_bools[i][0] != 0:
            cx, cy, r = d

            if contains_point_bools[i][0] == 1: # Touches edge
                p[i] = contains_point_bools[i][1]
                Q = Q.union(set(contains_point_bools[i][2]))
                #TODO vertices of E to Q
            else: # Is a small rectangle,
                p[i] = (cx, cy)

                Q = Q.union(set(contains_point_bools[i][2]))

    P = set()
    Pi = [set()]*len(D)
    for i,d in enumerate(D):
        if contains_point_bools[i][0] == 0:
            Pi[i] = getGridPointsInDiscStupid(d, delta, Q)
            P = P.union(Pi[i])

    P = list(P)

    P_index = dict()
    for i,x in enumerate(P):
        P_index[x] = i


    num_small_discs = sum(1 if x[0] != 0 else 0 for x in contains_point_bools)

    n = len(D)
    m = len(P)
    G = BipartiteGraph(n, m)

    for i,d in enumerate(D):
        for x in Pi[i]:
            G.addEdge(i, P_index[x])


    M = G.matching()
    if M is None:
        print("FAIL: no matching")
        return None

    numMatchingEdges = sum([sum(x) for x in M])

    if numMatchingEdges < n - num_small_discs:
        print("FAIL: no matching")
        return None

    for i in range(n):
        for j in range(i+1, m):
            if M[i][j] == 1:
                p[i] = P[j]
                p[i] = (delta*p[i][0], delta*p[i][1])

    if any(x is None for x in p):
        print("Fail: no matching")
        return None

    for i in range(n):
        for j in range(n):
            if i !=j:
                dist = max(abs(p[i][0]-p[j][0]), abs(p[i][1]-p[j][1]) )
                if dist < delta:
                    print("FAIL: points are not far apart")
                    return p
    print("SUCCESS")
    return p

def DistantRepresentatives(D):


    assert(len(D) >=  1)
    if len(D) == 1:
        pass


    deltas = set()
    n = len(D)
    for i in range(n):
        for j in range(i+1, n):
            if i!=j:
                d1 = D[i]
                d2 = D[j]

                d1L = d1[0] - d1[2]
                d1R = d1[0] + d1[2]
                d2L = d2[0] - d2[2]
                d2R = d2[0] + d2[2]

                if d2R > d1L:
                        deltas = deltas.union({ (d2R - d1L) / k for k in range(1, n)})
                if d1R > d2L:
                        deltas = deltas.union({ (d1R - d2L) / k for k in range(1, n)})

                d1B = d1[1]-d1[2]
                d1T = d1[1]+d1[2]
                d2B = d2[1] - d2[2]
                d2T = d2[1] + d2[2]

                if d2T > d1B:
                        deltas = deltas.union({ (d2T - d1B) / k for k in range(1, n)})
                if d1T > d2B:
                        deltas = deltas.union({ (d1T - d2B) / k for k in range(1, n)})

    deltas = list(deltas)
    deltas.sort()

    L = len(deltas)
    assert(L >= 2)

    l = 0
    u = L-1

    i = (u+l) // 2

    print("L = ", L)

    p_best = None
    while i >= l and i <= u and not (u - l <= 1):

        p = Placement(D, deltas[i]/2)

        if p is not None:
            p_best = p
            l = i
        else:
            u = i
        i = (u+l) // 2

    return Placement(D, deltas[l]/2)
