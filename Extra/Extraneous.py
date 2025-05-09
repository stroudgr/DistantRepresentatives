# Please ignore this file
# Code fragments that may be later useful if more specification is allowed.

class DistantRepresentativesRectangles:
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
        (2, p, Q) - Otherwise, meaning d is contained within a grid cell.
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
    

    def isLBlockerCentre(self, b):
        i,j=b
        assert type(i) == int and type(j) == int

        return (-i+j) % 3 == 0
    
     def getGridPointsInRect(self):
        # TODO what is our approach here?
        """In a smart way, find all the blocker shapes that intersect the rectangle."""
        raise NotImplementedError
    
    def getDistantRepresentativesLINF(self, D):
        """
        Given a set of discs D, tries to find a placement of representatives points
        in each disc so that all points are as far apart as possible.

        This algorithm will succeed at finding points that are >= 0.5 delta* apart,
        where delta* is the distance between the closest pair of points in the
        optimal solution. In other words, this returns a 2-Approximation.
        """
        raise NotImplementedError
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







# In Mathcing.py
def small(d, delta):
    cx, cy, r = d

    # bottom left of square/disc
    bl = (cx-r, cy-r)
    # top right
    tr = (cx+r, cy+r)

    # grid element that is left and below of bl
    blg = (delta*math.floor(bl[0]/delta), delta*math.floor(bl[1]/delta))

    return blg[0] < bl[0] and blg[1] < bl[1] and tr[0] < blg[0] + delta and tr[1] < blg[1] + delta

#class Disc:
#    def __init__(self, cx, cy, r, inf=True):
#        self.cx = cx
#        self.cy = cy
#        self.r = r
#        self.inf = True


class _Node:

    def __init__(self, value):
        self.value = value
        self.adj = []
