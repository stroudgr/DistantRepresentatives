from DistantRepresentatives import LInf, LOne, LTwoSquared
import math
from Matching import BipartiteGraph

#class Rectangle(object):
#    """A Rectangle class."""

#    def __init__(self, b, h, c):
#        super(Rectangle, self).__init__()
#        self.b = b
#        self.h = h
#        self.cx=c[0]
#        self.cy=c[1]


class DistantRepresentativesRectangles:

    def __init__(self, norm):
        self.norm = norm


    def inRect(self, p, r):
        """Returns True iff p is in rectangle r
        """
        x, y = p
        cx, cy, W, H = r
        return cx - W  <= x and x <= cx + W and cy - H  <= y and y <= cy + H

    def plusBlockerIntersectsRect(self, r, b, delta):
        """
        For a grid with diagonal distance delta, with plusBlocker shape b
        connecting points as seen in Figure 1 of the paper:
        https://drops.dagstuhl.de/storage/00lipics/lipics-vol204-esa2021/LIPIcs.ESA.2021.17/LIPIcs.ESA.2021.17.pdf
        
        This function returns True iff rectangle r touches the plusBlocker b for this given delta.
        """
        x,y = b
        l = [(delta*x, delta*y), (delta*(x+1), delta*y), (delta*(x-1), delta*y), (delta*x,delta*(y+1)), (delta*x,delta*(y-1))]
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

    def isPlusBlockerCentre(self, b):
        """
        Returns True if grid point b is the centre of a plus blocker.
        We use the centre as the identifying point.
        """
        i,j=b
        assert type(i) == int and type(j) == int

        #return (i+j) % 4 == 0
        return (i+j) % 4 == 0 and i % 2 == 0 and j % 2 == 0

    # + blockers determined by centre grid points
    def getPlusBlockersInDiscBrute(self, r, delta, n, Q):
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

                    if len(S) >= n:
                        return S

        return S


    def inPlus(self, b, p, delta,err=0.00001):
        """
        Returns true if point p lies on the blocker b.
        """
        x,y=b
        a,c=p
        if (delta*(x-1) <= a and a <= delta*(x+1) and abs(delta*y-c) < err):
            return True

        return (delta*(y-1) <= c and c <= delta*(y+1) and abs(delta*x-a) < err)


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
        """
        Returns, if it exists, a point in the intersection of rectangle r and blockerShape b.
        """
        x,y=b
        cx,cy,w,h=r

        # if being true means (at least one of the top/bottom edges touch the vertical part):
        #               |
        #          _____|______
        #               |
        #            ---|----
        #           |        |
        #            --------

        # If vertical bar of plus shape lies between left/right boundaries of rect. 
        if (cx-w <= delta*x and delta*x <= cx+w):
            if delta*(y-1)<= cy+h and cy+h <= delta*(y+1): # touches top boundary?
                return (delta*x, cy+h)
            elif delta*(y-1)<= cy-h and cy-h <= delta*(y+1): # touches bottom boundary?
                return (delta*x, cy-h)
            elif (cy-h <= delta*(y-1) and delta*(y+1) <= cy+h): # in-between top and bottom boundary. Can choose any point. 
                return (delta*x, delta*y)

        # Symmetric to above case

        if (cy-h <= delta*y and delta*y <= cy+h):
            if delta*(x-1)<= cx+w and cx+w <= delta*(x+1):
                return (cx+w, delta*y)
            elif delta*(x-1)<= cx-w and cx-w <= delta*(x+1):
                return (cx-w, delta*y)
            elif (cx-w <= delta*(x-1) and delta*(x+1) <= cx+w): 
                return (delta*x, delta*y)
        return None
        # cannot touch otherwise!

    def Placement(self, R, delta):
        """
        Given a set of rectangles R=[r1,r2,r3,...,rn], and real value delta.

        Returns a placement of representatives p=(p1,p2,...,pn), which satisfies:
        - d_l(pi,pj) >= delta    for all i != j, where l is 1,2,inf

        This will always succeed when delta <= delta*/f_l, where delta* is the largest
        value for which you can find a placement, and

        f_1 = 5     in the L1 norm
        f_2 = 5.83  in the L2 norm
        f_inf = 6   in the L infinity norm

        For now the algorithm is just implemented/optimized for the L1 norm. 
        It will be constant-approximation algorithm for other Lp norms, since all norms
        are equivalent in R^2.

        This may succeed when delta*/f_l < delta <= delta*, but this is not
        guaranteed. This will fail when delta > delta*, as no such placement exists.
        """

        Q = set()
        p = [None] * len(R)

        # Finds all blocker shapes that touch the rectangle.
        blockers = [self.getPlusBlockersInDiscBrute(r, delta, len(R), set()) for r in R]

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

        numMatchingEdges = sum([sum(x) for x in M])

        # Assert all discs get matched to a grid point.
        if numMatchingEdges < n - num_small_discs:
            print("2. FAIL: no matching")
            return None

        # Convert grid points to corresponding point in delta sized grid.
        for i in range(n):
            for j in range(m):
                 
                if M[i][j] == 1:

                    p[i] = self.findRectAndPlusIntersectionPoint(R[i], P[j], delta)
                    
                    if p[i] is None:
                        raise NotImplementedError

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

    def getDistantRepresentatives(self, R):
        """
        Given a set of rects R, tries to find a placement of representatives points
        in each disc so that all points are as far apart as possible.

        This algorithm will succeed at finding points that are >= c delta* apart,
        where delta* is the distance between the closest pair of points in the
        optimal solution. In other words, this returns a c-Approximation. c depends on the norm.
        For now, only the L1 norm case is implemented. But technically, since all p-norms
        values are within a constant multiple of each other, then this is also a constant factor
        approximation algorithm for any Lp norm, just not necessarily the best one.
        """

        if (len(R) <= 0):
            return -1, []
        
        if len(R) == 1:
            return -1, [(R[0][0], R[0][1])]

        n = len(R)


        print("Rectangles:")
        for r in R:
            cx, cy, w, h = r
            print(f"[({cx}, {cy}), w={w}, h={h}]")

        # Let's just assume the input is always integer
        #self.convertToInteger(R)

        D = max(max(abs(r[0]+r[2]), abs(r[0]-r[2]), abs(r[1]+r[3]), abs(r[1]-r[3])) for r in R)

        lb = 1/n
        ub = 2*D
        delta = 1/n
        p_success = self.Placement(R, 1/n)


        print("*********************************", 2*D, " ", 1/n)

        if p_success is None:
            # TODO: return a solution when delta=1/n"
            # This failure only happens when the rectangles are extraordinaly small and close together.
            # This shouldn't be an issue with the visualization tool.
            raise NotImplementedError

        while ub-lb > 1/ (n*n*D):
            delta = (lb+ub)/2
            p = self.Placement(R, delta)
            if p is None:
                ub = delta
            else:
                lb = delta
                p_success=p

        return delta, p_success
