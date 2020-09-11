from DistantRepresentatives import LInf, LOne, LTwoSquared
import math
from Matching import BipartiteGraph

class Rectangle(object):
    """A Rectangle class."""

    def __init__(self, b, h, c):
        super(Rectangle, self).__init__()
        self.b = b
        self.h = h
        self.cx=c[0]
        self.cy=c[1]


class DistantRepresentativesRectangles:

    def __init__(self, norm):
        self.norm = norm

    #TODO BLOCKERS!!!!
    def contains_point(self, d, delta):

        raise NotImplementedError

        """
        For the given rectangle d, returns whether grid delta*LAMBDA intersects d
        (as defined in 'Cabello's Approximation Algorithms for Spreading Points',
        LAMBDA is a unit grid, and delta*LAMBDA is the grid with point spread out
        delta apart, i.e. { delta*p : p in LAMBDA }). Can think of p as 'moving
        through time' as we increase/decrease delta.

        Returns:
        (0,None) - If d contains a grid point. Such point is not needed now, so None
                    is returned along with indicator 0.
        (1,p, Q) - If d hits a grid edge. p is a point that intersects d and the
                    grid edge. Q containts the two grid points that make this grid
                    edge.
        (2, p, Q) - Othwerwise, meaning d is contained within a grid cell.
                    p is the center of disc, and Q consists of the 4 corners of the
                    grid cell.

        For Q above, since they are grid points, they return the points in grid
        LAMBDA, as opposed to delta*LAMBDA, which is the relevant grid (this ensures
        the points are integer points, saving the need to convert to the
        delta*LAMBDA grid until later. This helps avoid any arithmetic errors).

        We do not this for p, because it is part of the disc, and not a grid point.
        Discs are fixed size, grids are not.
        """

        cx, cy, W, H = d

        # Outside the square/disc, or touching the edge
        verticalGridLineLeft = math.floor((cx-W) / delta)
        verticalGridLineRight = math.ceil((cx+W) / delta)

        # Outside the square/disc, or touching the edge
        horizontalGridLineBelow = math.floor((cy-H) / delta)
        horizontalGridLineAbove = math.ceil((cy+H) / delta)

        # touching the edge case vertically
        if (cx-W) % delta == 0 or (cx+W) % delta == 0:

            # touching the edge case horizontally
            if (cy-H) % delta == 0 or (cy+H) % delta == 0:
                return (0,None) # corner of the square is a grid point

            # Both outside the square/disc, and at least one horizontal line
            # exists in between.
            if not(horizontalGridLineBelow + 1 < horizontalGridLineAbove):
                return (0, None) # One of the vertical edges has a grid point

            # Hits grid edge, but had no grid points inside
            if (cx-W) % delta == 0:
                return (1, (cx-W, cy+H),
                        [(d[0]-d[2], horizontalGridLineBelow),
                         (d[0]-d[2], horizontalGridLineBelow + 1)]  )
            else:    #if(d[1]+d[2]) % delta == 0:
                return (1, (d[0]+d[2], d[1]+d[2]),
                        [(d[0]+d[2], horizontalGridLineBelow),
                         (d[0]+d[2], horizontalGridLineBelow + 1)]  )

        elif verticalGridLineLeft + 1 < verticalGridLineRight: # MIDDLE vertical line exists

            # touching the edge case horizontally
            if (d[1]-d[2]) % delta == 0 or (d[1]+d[2]) % delta == 0:
                return (0, None)# MIDDLE vertical lines intersect horizontalGridLine, which
                # hits the disc edge

            # Both outside the square/disc, and at least one horizontal line
            # exists in between.
            if horizontalGridLineBelow + 1 < horizontalGridLineAbove:
                return (0, None) # One of the vertical edges has a grid point

            return (1, (delta*(verticalGridLineLeft + 1), d[1]+d[2]), # Hits grid edge
                        [( verticalGridLineLeft + 1, horizontalGridLineBelow ),
                         ( verticalGridLineLeft + 1, horizontalGridLineAbove ) ] )

        else: #Neither vertical lines touch disc, and nothing inbetween these two lines

            # touching the edge case horizontally
            if (d[1]-d[2]) % delta == 0:
                return (1, (d[0]-d[2] , d[1]-d[2]),
                        [(verticalGridLineLeft,  horizontalGridLineBelow ),
                         (verticalGridLineRight, horizontalGridLineBelow ) ])

            if (d[1]+d[2]) % delta == 0:
                return (1, (d[0]-d[2] , d[1]+d[2]),
                        [(verticalGridLineLeft,  horizontalGridLineAbove ),
                         (verticalGridLineRight, horizontalGridLineAbove ) ])

            if horizontalGridLineBelow + 1 < horizontalGridLineAbove:
                return (1, (d[0]-d[2] , delta*(horizontalGridLineBelow + 1)),
                        [( verticalGridLineLeft,  horizontalGridLineBelow + 1 ),
                         ( verticalGridLineRight, horizontalGridLineBelow + 1 )])

            return (2, (d[0], d[1]),
                          [
                           (verticalGridLineLeft,  horizontalGridLineBelow),
                           (verticalGridLineRight, horizontalGridLineBelow),
                           (verticalGridLineRight, horizontalGridLineAbove),
                           (verticalGridLineLeft,  horizontalGridLineAbove)
                          ])

        return False


    def inRect(self, p, r):
        """Returns true iff p is in rectangle r"""
        x, y = p
        cx, cy, W, H = r
        return cx - W  <= x and x <= cx + W and cy - H  <= y and y <= cy + H

    def plusBlockerIntersectsRect(self, r, b, delta):
        x,y = b
        l = [(x,y), (x+1,y), (x-1,y), (x,y+1), (x,y-1)]
        if any(self.inRect(z, r)  for z in l):
            return True

        cx, cy, W, H = r
        if ((cx - W <= delta*x and cx+W >= delta*x) and ((cy - H >= delta*(y-1) and cy-H <= delta*(y+1)) or (cy + H >= delta*(y-1) and cy+H <= delta*(y+1)))):
                return True

        if ((cy - H <= delta*y and cy+H >= delta*y)
            and   ((cx - W >= delta*(x-1) and cx-W <= delta*(x+1))
                or (cx + W >= delta*(x-1) and cx+W <= delta*(x+1)))):
                return True

        return False


    def LBlockerIntersectsRect(self, r, b, delta):

        raise NotImplementedError

        # TODO!

        x,y = b
        l = [(x,y), (x+1,y), (x-1,y), (x,y+1), (x,y-1)]
        if any(self.inRect(z, r)  for z in l):
            return True

        cx, cy, W, H = r
        if ((cx - W <= delta*x and cx+W >= delta*x)
            and   ((cy - H >= delta*(y-1) and cy-H <= delta*(y+1))
                or (cy + H >= delta*(y-1) and cy+H <= delta*(y+1)))):
                return True

        if ((cy - H <= delta*y and cy+H >= delta*y)
            and   ((cx - W >= delta*(x-1) and cx-W <= delta*(x+1))
                or (cx + W >= delta*(z-1) and cx+W <= delta*(x+1)))):
                return True

        return False

    def isPlusBlockerCentre(self, b):
        i,j=b
        assert type(i) == int and type(j) == int

        #return (i+j) % 4 == 0
        return (i+j) % 4 == 0 and i % 2 == 0 and j % 2 == 0

    def isLBlockerCentre(self, b):
        i,j=b
        assert type(i) == int and type(j) == int

        return (-i+j) % 3 == 0

    # + blockers determined by centre grid points
    def getPlusBlockersInDiscStupid(self, r, delta, n, Q):
        """In a brute force fashion, finds all + blocker shapes that intersect
        the rectangle, excluding blockers of Q."""
        cx, cy, W, H = r
        xmin = math.floor((cx-W)/delta)
        xmax = math.ceil((cx+W)/delta)
        ymin = math.floor((cy-H)//delta)
        ymax = math.ceil((cy+H)/delta)

        S = set()
        for i in range(xmin, xmax+1):

            for j in range(ymin, ymax+1):

                if not self.isPlusBlockerCentre((i,j)):
                    continue

                if (i, j) not in Q and self.plusBlockerIntersectsRect(r, (i, j), delta):
                    S = S.union({(i, j)})

                    # THIS is probably a bad idea!
                    #if len(S) >= n:
                    #    return S

        return S


    def getGridPointsInRect(self):
        # TODO what is our approach here?
        """In a smart way, find all the blocker shapes that intersect the rectangle."""
        raise NotImplementedError


    def inPlus(self, b, p, delta,err=0.00001):
        x,y=b
        a,b=p
        if (delta*(x-1) <= a and a <= delta*(x+1) and abs(delta*y-b) < err):
            return True

        return (delta*(y-1) <= b and b <= delta*(y+1) and abs(delta*x-a) < err)


    def plusBlockerAndRectFarApart(self, r, b, delta):
        """
        Given rectangle r and plus blocker b, returns false if the blocker
        and rectangle are minimum distance strictly less than delta.

        """

        cx,cy,w,h = r
        rect_corners=[(cx-w,cy-h), (cx+w,cy-h), (cx-w,cy+h), (cx+w,cy+h)]
        x,y=b
        blocker_points=[(x-1,y),(x,y),(x+1,y),(x,y-1),(x,y+1)]
        blocker_points = [(delta*a, delta*b) for a,b in blocker_points]

        mindist = 100000000000
        for p in rect_corners:
            for q in blocker_points:
                mindist = min(mindist, self.norm(p, q))
                if self.inRect((q[0],p[1]) , r):
                    mindist = min(mindist, self.norm((q[0],p[1]), q))
                if self.inRect((p[0],q[1]) , r):
                    mindist = min(mindist, self.norm((p[0],q[1]), q))

                if self.inPlus(b, (p[0],q[1]), delta):
                    mindist = min(mindist, self.norm((p[0],q[1]), p))

                if self.inPlus(b, (q[0],p[1]), delta):
                    mindist = min(mindist, self.norm((p[0],q[1]), p))

        return mindist >= delta

    def findRectAndPlusIntersectionPoint(self, r, b, delta,err=0.001):
        x,y=b
        cx,cy,w,h=r

        # if being true means (at least one of the top/bottom edges touch the vertical part):
        #               |
        #          _____|______
        #               |
        #            ---|----
        #           |        |
        #            --------
        if (cx-w <= delta*x and delta*x <= cx+w):
            if delta*(y-1)<= cy+h and cy+h <= delta*(y+1):
                return (delta*x, cy+h)
            elif delta*(y-1)<= cy-h and cy-h <= delta*(y+1):
                return (delta*x, cy-h)
            else:
                return None

        if (cy-h <= delta*y and delta*y <= cy+h):
            if delta*(x-1)<= cx+w and cx+w <= delta*(x+1):
                return (cx+w, delta*y)
            elif delta*(x-1)<= cx-w and cx-w <= delta*(x+1):
                return (cy-w, delta*x)
            else:
                return None
        return None
        # cannot touch otherwise!

    def Placement(self, R, delta):
        """
        Given a set of rectangles R=[r1,r2,r3,...,rn], and real value delta.

        Returns a placement of representatives p=(p1,p2,...,pn), which satisfies:
        - d_l(pi,pj) >= delta    for all i != j, where l is 1,2,inf

        This will always succeed when delta <= delta*/f_l, where delta* is the largest
        value for which you can find a placement, and

        f_1 = fill in  in the L1 norm
        f_2 =
        f_inf =

        This may succeed when delta*/f_l < delta <= delta*, but this is not
        guaranteed. This will fail when delta > delta*, as no such placement exists.
        """

        Q = set()
        p = [None] * len(R)

        # Finds all blocker shapes that touch the rectangle.
        blockers = [self.getPlusBlockersInDiscStupid(r, delta, len(R), set()) for r in R]

        # These rectangles contain no blocker shapes, so their representatives
        # are the centre.
        # The centres may be too close to each other, this will be
        # checked later.
        num_small_discs = len(R)
        for i,r in enumerate(R):

            if len(blockers[i]) == 0:
                num_small_discs -= 1
                cx, cy, w, h = r
                p[i] = (cx, cy)

                # Adds blockers to Q
                xmin = math.floor(cx/delta)-2
                xmax = math.floor(cx/delta)+3

                ymin = math.floor(cy/delta)-2
                ymax = math.floor(cy/delta)+3

                for x in range(xmin, xmax+1):
                    for y in range(ymin, ymax+1):
                        if self.isPlusBlockerCentre((x,y)):
                            if not self.plusBlockerAndRectFarApart(r, (x,y), delta):
                                Q = Q.union({(x,y)})

        P = set()
        #Pi = [set()]*len(D) # now called blockers

        # The remaining rectangles:
        # Find all the blockers within each rectangle, subtract Q.
        for i,d in enumerate(R):
            blockers[i] = blockers[i].difference(Q)
            P = P.union(blockers[i])

        # Enumerate all the blockers.
        P = list(P)
        P_index = dict()
        for i,x in enumerate(P):
            P_index[x] = i

        n = len(R)
        m = len(P)
        print(n,m)

        # Create a bipartite graph between all the discs (L) and all the grid points (R)
        # within the discs. Add an edge between a disc and a grid point iff the grid
        # point is in that disc.
        G = BipartiteGraph(n, m)
        for i,d in enumerate(R):
            for x in blockers[i]:
                G.addEdge(i, P_index[x])

        # Find a maximal matching that tries to ensure everything on the left side
        #  is matched.
        M = G.matching()
        if M is None:
            print("1. FAIL: no matching")
            return None

        print(M)
        numMatchingEdges = sum([sum(x) for x in M])

        print(numMatchingEdges, num_small_discs, n)
        # Assert all discs get matched to a grid point.
        if numMatchingEdges < n - num_small_discs:
            print("2. FAIL: no matching")
            return None

        # Convert grid points to corresponding point in delta sized grid.
        for i in range(n):
            for j in range(m):
                if M[i][j] == 1:

                    # TODO
                    #p[i]=(delta*P[j][0], delta*P[j][1])
                    p[i] = self.findRectAndPlusIntersectionPoint(R[i], P[j], delta)
                    assert p[i] is not None
                    break

        if any(x is None for x in p):
            print("3. Fail: no matching")
            return None

        # Ensure all points are >= delta distance apart.
        for i in range(n):
            for j in range(i+1, n):
                dist = self.norm(p[i], p[j])
                if dist < delta:
                    print("FAIL: points are not far apart")
                    return p
        print("SUCCESS")
        return p

    def getDistantRepresentatives(self, D):
        """
        Given a set of discs D, tries to find a placement of representatives points
        in each disc so that all points are as far apart as possible.

        This algorithm will succeed at finding points that are >= 0.5 delta* apart,
        where delta* is the distance between the closest pair of points in the
        optimal solution. In other words, this returns a 2-Approximation.
        """

        assert(len(D) >=  1)
        if len(D) == 1:
            pass

        # The optimal solutions takes on a special form. Generates all deltas
        # that the optimal could be. Takes O(n^3) space/time.
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

        # Perform a binary Search
        # Find delta_i where Placement(delta_i /2) succeeds but
        #  Placement(delta_{i+1} /2) fails. The solution for delta_i/2 is a
        #   2-Approximation.
        p_best = None
        while i >= l and i <= u and not (u - l <= 1):

            p = self.Placement(D, deltas[i]/2)

            if p is not None:
                p_best = p
                l = i
            else:
                u = i
            i = (u+l) // 2

        return self.Placement(D, deltas[l]/2)
