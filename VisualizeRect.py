from cmath import rect
import os, sys
import math
from PIL import Image, ImageDraw
from DistantRepresentatives import LInf, LOne
from DistantRepresentativesRectangles import DistantRepresentativesRectangles

import argparse

R = [(100, 100, 30, 30), (50,50, 20, 20), (100, 150, 3, 3), (30, 150, 3, 3)]
W, H = 300, 300

norm = LOne
dr = DistantRepresentativesRectangles(norm)

placement = False
drawGrid = True

#parser = argparse.ArgumentParser*(decription="A distant representatives approximation visualizer.")
#parser.add_argument('--show-grid')

class Visualizer:
    pass



def acceptInput():
    n = input("Enter the number of rectangles")
    assert(type(n) is int)
    
    rects = []
    for i in range(n):
        cx,cy = input(f"Please enter the centre coordinates of rectangle #{i}.")
        w = input(f"Please enter the width of rectangle #{i}.")
        h = input(f"Please enter the height of rectangle #{i}.")
        
        rects.append((cx,cy,w/2,h/2))

    print("Setup is complete.")

    #TODO 


    show_grid = False
    for i in range(len(sys.argv)):
        if (sys.argv[i] == "--show-grid"):
            i+=1
            if (sys.argv[i] in {"True", "true", "T", "t"}):
                show_grid = True
            else:
                show_grid = False

    print("Computing optimal solution....")
    DELTA_RET, p = dr.getDistantRepresentatives(rects)
    delta = DELTA_RET

    print("Optimal delta = ", delta)

    # creating new Image object
    img = Image.new("RGB", (W, H))

    img1 = ImageDraw.Draw(img)

    for r in R:
        cx, cy, w, h = r

        shape = [(cx-w, H-(cy-h)), (cx+w, H-(cy+h))]

        img1.rectangle(shape, fill =(255,0,0), outline ="red")


    if delta < 5 and drawGrid:
        print("The Grid is too small to be drawn, so it won't be drawn as requested.")

    if delta >= 5 and drawGrid:

        # (0,0)
        #img1.rectangle([(-1, H-(-1)), (1,H-(1))], fill=(0,0,255))

        # 
        #img1.rectangle([(delta*0-1, H-(delta*1-1)), (delta*0+1,H-(delta*1+1))], fill=(0,255,0))
        #img1.rectangle([(delta*1-1, H-(delta*0-1)), (delta*1+1,H-(delta*0+1))], fill=(0,255,0))
        #img1.rectangle([(delta*1-1, H-(delta*1-1)), (delta*1+1,H-(delta*1+1))], fill=(0,255,0))


        # Draw a grid
        for i in range(0, math.floor(W / delta) + 1):
            for j in range(0, math.floor(H / delta) + 1):

                if not( (i == 0 or i==1) and (j==1 or j==0)):
                    img1.rectangle([(delta*i-1, H-(delta*j-1)), (delta*i+1,H-(delta*j+1))], fill=(0,255,0))

        # Draw plus blockers
        for i in range(-1, math.floor(W / delta) + 2):
            for j in range(-1, math.floor(H / delta) + 2):
                if (i+j) % 4 == 0 and i % 2 ==0 and j % 2 ==0: # isPlusBlockerCentre in DistantRepresentativesRectangles
                    img1.rectangle([(delta*i-1, H-(delta*(j+1)-1)), (delta*i+1,H-(delta*(j-1)+1))], fill=(0,255,0))
                    img1.rectangle([(delta*(i+1)-1, H-(delta*j-1)), (delta*(i-1)+1,H-(delta*j+1))], fill=(0,255,0))
                    pass


    # Draw the representative points.
    if p is not None:
        for (x,y) in p:
            img1.rectangle([(x-2, H-(y-2)), (x+2,H-(y+2))], fill=(255,255,0))

    img.show()
