import os, sys
import math
from PIL import Image, ImageDraw
from DistantRepresentatives import LInf
from DistantRepresentativesDiscs import DistantRepresentativesDiscs

D = [(100, 100, 30), (50,50, 20), (100, 150, 3), (30, 150, 3)]
w, h = 1000, 700

dr = DistantRepresentativesDiscs(LInf)
assert (dr is not None)

placement = True
drawGrid = True


if placement:

    delta = 26
    assert(delta >= 5)

    p = dr.Placement(D, delta)

    if p is None:
        exit()

    # creating new Image object
    img = Image.new("RGB", (w, h))

    img1 = ImageDraw.Draw(img)

    for d in D:
        cx, cy, R = d

        shape = [(cx-R, h-(cy-R)), (cx+R, h-(cy+R))]

        img1.rectangle(shape, fill =(255,0,0), outline ="red")

    # (0,0)
    img1.rectangle([(-1, h-(-1)), (1,h-(1))], fill=(0,0,255))

    img1.rectangle([(delta*0-1, h-(delta*1-1)), (delta*0+1,h-(delta*1+1))], fill=(0,255,0))
    img1.rectangle([(delta*1-1, h-(delta*0-1)), (delta*1+1,h-(delta*0+1))], fill=(0,255,0))
    img1.rectangle([(delta*1-1, h-(delta*1-1)), (delta*1+1,h-(delta*1+1))], fill=(0,255,0))

    for i in range(0, math.floor(w / delta) + 1):
        for j in range(0, math.floor(h / delta) + 1):

            if not( (i == 0 or i==1) and (j==1 or j==0)):
                img1.rectangle([(delta*i-1, h-(delta*j-1)), (delta*i+1,h-(delta*j+1))], fill=(0,255,0))

    for (x,y) in p:
        img1.rectangle([(x-2, h-(y-2)), (x+2,h-(y+2))], fill=(0,0,255))

    img.show()

else:

    p = dr.getDistantRepresentatives(D)

    delta = 100000000000

    for i in range(len(D)):
        for j in range(i+1, len(D)):

            delta = min(delta, LInf(p[i], p[j]))

    print("Optimal delta = ", delta)

    # creating new Image object
    img = Image.new("RGB", (w, h))

    img1 = ImageDraw.Draw(img)

    for d in D:
        cx, cy, R = d

        shape = [(cx-R, h-(cy-R)), (cx+R, h-(cy+R))]

        img1.rectangle(shape, fill =(255,0,0), outline ="red")


    if delta < 5 and drawGrid:
        print("The Grid is too small to be drawn, so it won't be drawn as requested.")

    if delta >= 5 and drawGrid:

        # (0,0)
        img1.rectangle([(-1, h-(-1)), (1,h-(1))], fill=(0,0,255))

        img1.rectangle([(delta*0-1, h-(delta*1-1)), (delta*0+1,h-(delta*1+1))], fill=(0,255,0))
        img1.rectangle([(delta*1-1, h-(delta*0-1)), (delta*1+1,h-(delta*0+1))], fill=(0,255,0))
        img1.rectangle([(delta*1-1, h-(delta*1-1)), (delta*1+1,h-(delta*1+1))], fill=(0,255,0))

        for i in range(0, math.floor(w / delta) + 1):
            for j in range(0, math.floor(h / delta) + 1):

                if not( (i == 0 or i==1) and (j==1 or j==0)):
                    img1.rectangle([(delta*i-1, h-(delta*j-1)), (delta*i+1,h-(delta*j+1))], fill=(0,255,0))

    for (x,y) in p:
        img1.rectangle([(x-2, h-(y-2)), (x+2,h-(y+2))], fill=(255,255,0))

    img.show()
