import math

class Disc:
    def __init__(self, cx, cy, r, inf=True):
        self.cx = cx
        self.cy = cy
        self.r = r
        self.inf = True

class _Node:

    def __init__(self, value):
        self.value = value
        self.adj = []

class BipartiteGraph:
    """
    An undirected bipartite graph class.
    """
    def __init__(self, n, m):

        self.matrix = [[0]*m for i in range(n)]
        self.n = n # left size
        self.m = m # right size

    def __str__(self):
        graph_string=""
        for i in range(self.n):
            l=[]
            for j in range(self.m):
                if self.matrix[i][j] == 1:
                    l.append(j)
            graph_string=graph_string+str(l)+"\n"
        return graph_string

    def degreeLeft(self, x):
        return sum(self.matrix[x])

    def addEdge(self, a, b):
        self.matrix[a][b] = 1
        # TODO: not bothering with symmetry?

    def matching(self):

        # Adjacency matrix representing the matching.
        M = [[0]*self.m for i in range(self.n)]
        p = self.augmentingPath(M)
        #assert False
        while p is not None:
            M = self.updateMatching(p, M)
            p = self.augmentingPath(M)
        return M

    def updateMatching(self, p, M):
        M_new = M.copy()
        # len(p) is even
        #print("len", len(p)//2 - 1)

        for i in range(len(p)//2 - 1):
            x = p[2*i]
            y = p[2*i+1]
            z = p[2*i+2]

            M_new[x][y] = 1
            M_new[z][y] = 0

        x = p[len(p)-2]
        y = p[len(p)-1]
        M_new[x][y] = 1
        #print("...")
        return M_new

    def augmentingPath(self, M):
        """
        Returns an augmenting path in this bipartite graph given matching M.

        An augmenting path is an odd length path of the graph starting from the left side to the right side of the graph,
        so that the start and end vertices of the path are unmatched in M
        and every L->R edge doesn't belong to M
        and every R->L edge does belong to M

        Eg. A -> 2 -> B -> 3, where --- are edges not in M, === are in M.

        A --------- 1                                 A  -------------- 1
            -                                            ===
              -                                             ===
                -                                               ===
                  - 2          "flip this path"                    ===  2
                ===                                                 -
             ===                                               -
          ===                                               -
        B  --------- 3                                B  =============  3



        """
        


        # Perform dfs starting from any unmatched vertex of left side. 
        for k in range(self.n):
            # Check if k is unmatched.
            if not any(M[k]):
                
                # Start dfs from k
                stack = [(k, True)]

                #dL = [None]*self.n
                #dR = [None]*self.m

                # Determines whether node has been discovered yet during dfs.
                colorL = [0]*self.n
                colorR = [0]*self.m

                # parent of each node in dfs tree.
                parL = [None]*self.n
                parR = [None]*self.m

                #dL[k] = 0
                colorL[k] = 1

                while len(stack) != 0:
                    (x, left) = stack.pop()

                    if left:
                        for i in range(self.m):
                            if self.matrix[x][i] and not M[x][i] and colorR[i] == 0:
                                #print("neigh", x, "->", i)
                                colorR[i] = 1
                                stack.append((i, False))
                                parR[i] = x
                        colorL[x] = 2

                    if not left:
                        endPath = True
                        for i in range(self.n):
                            if self.matrix[i][x] and M[i][x] and colorL[i] == 0:
                                #print("neigh", x, "->", i)
                                colorL[i] = 1
                                stack.append((i, True))
                                parL[i] = x
                                endPath = False
                            if M[i][x]:
                                endPath = False

                        if endPath:
                            #print("A", k, x)
                            p = [x]
                            x = parR[x]
                            p.append(x)
                            while parL[x] is not None:
                                x = parL[x]
                                p.append(x)
                                x = parR[x]
                                p.append(x)
                            p.reverse()
                            #print(p)
                            #print()
                            return p

                        colorR[x] = 2
            #else:
            #    print("no using k = ", k)
        return None


def hitsEdge(d, delta):
    pass

def small(d, delta):
    cx, cy, r = d

    # bottom left of square/disc
    bl = (cx-r, cy-r)
    # top right
    tr = (cx+r, cy+r)

    # grid element that is left and below of bl
    blg = (delta*math.floor(bl[0]/delta), delta*math.floor(bl[1]/delta))

    return blg[0] < bl[0] and blg[1] < bl[1] and tr[0] < blg[0] + delta and tr[1] < blg[1] + delta



def printBinMatrix(M):
    for x in M:
        print(x)

# test
"""
b = BipartiteGraph(3, 5)
b.addEdge(0, 1)
b.addEdge(1, 1)
b.addEdge(2,1)
b.addEdge(2,3)
printBinMatrix(b.matrix)
M = b.matching()

printBinMatrix(M)
"""
