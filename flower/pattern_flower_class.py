#================================================== Imports

import pygame as pg
from math import pi, sin, cos


class pattern_flower():
    def __init__(self, sides, radius, unit, lineColour=(0,0,0), fillStart=(0,0,0), fillEnd=(255,255,255), screenDim=None):
        self.n = sides
        self.r = radius
        self.unit = unit
        self.lineColour = lineColour
        self.fillStart = fillStart
        self.fillEnd = fillEnd
        if screenDim is None:
            pass
        self.screenDim = screenDim
        self.create_pattern()

    @staticmethod
    def hyp(pos1, pos2):
        return (((pos1[0]-pos2[0])**2) + ((pos1[1]-pos2[1])**2)) ** (1/2)

    @staticmethod
    def midway(pos1, pos2):
        return [(pos1[x] + pos2[x]) // 2   for x in range(2)]

    @staticmethod
    def partway(pos1, pos2, unit):
        diff = [pos2[x] - pos1[x]   for x in range(2)]
        hyp = ((diff[0]**2) + (diff[1]**2)) ** (1/2)
        ratio = unit / hyp
        return [pos1[x] + (ratio * diff[x])   for x in range(2)]

    @staticmethod
    def add_layer(indieOutline, unit, centre):
        newOutline = [0 for x in range(4)]
        newOutline[0] = partway(indieOutline[0], indieOutline[2], unit)
        newOutline[1] = partway(indieOutline[1], indieOutline[0], unit)
        newOutline[2] = [X for X in indieOutline[2]]
        newOutline[3] = partway(indieOutline[3], indieOutline[0], unit)
        if hyp(newOutline[0], centre) <= hyp(newOutline[1], centre):
            return False, newOutline
        else:
            return True, newOutline

    @staticmethod
    def all_layers(indieOutlineList, unit, centre):
        done = False
        while not done:
            done, outline = add_layer(indieOutlineList[-1], unit, centre)
            if not done:
                indieOutlineList.append(outline)
        return indieOutlineList

    def create_pattern(self):
        mainOutline = [[sin((2*pi*x)/self.n), cos((2*pi*x)/self.n)]   for x in range(self.n)]
        mainOutline = [[round((self.r*Y)+(dim[y]//2))  for y, Y in enumerate(X)]  for X in mainOutline]

        subOutline = [self.midway(mainOutline[x], mainOutline[(x+1)%len(mainOutline)])   for x in range(n)]

        self.indieOutlines = [[[centre, subOutline[x-1], mainOutline[x], subOutline[x]]]   for x in range(n)]

        for x, X in enumerate(indieOutlines):
            self.indieOutlines[x] = self.all_layers(X, unit, centre)

    def draw_lines(self, screen=None):
        for X in self.indieOutlines:
            for Y in X:
                for z in range(len(Y)):
                    pg.draw.line(screen, lineColour, Y[z], Y[z-1])


#================================================== Functions

def hyp(pos1, pos2):
    return (((pos1[0]-pos2[0])**2) + ((pos1[1]-pos2[1])**2)) ** (1/2)

def midway(pos1, pos2):
    return [(pos1[x] + pos2[x]) // 2   for x in range(2)]

def partway(pos1, pos2, unit):
    diff = [pos2[x] - pos1[x]   for x in range(2)]
    hyp = ((diff[0]**2) + (diff[1]**2)) ** (1/2)
    ratio = unit / hyp
    return [pos1[x] + (ratio * diff[x])   for x in range(2)]

def add_layer(indieOutline, unit, centre):
    newOutline = [0 for x in range(4)]
    newOutline[0] = partway(indieOutline[0], indieOutline[2], unit)
    newOutline[1] = partway(indieOutline[1], indieOutline[0], unit)
    newOutline[2] = [X for X in indieOutline[2]]
    newOutline[3] = partway(indieOutline[3], indieOutline[0], unit)
    if hyp(newOutline[0], centre) <= hyp(newOutline[1], centre):
        return False, newOutline
    else:
        return True, newOutline

def all_layers(indieOutlineList, unit, centre):
    done = False
    while not done:
        done, outline = add_layer(indieOutlineList[-1], unit, centre)
        if not done:
            indieOutlineList.append(outline)
    return indieOutlineList


#================================================== User setup

dim = (1920, 1080)
dim = (800, 800)
n = 8
r = 350
unit = 20
fill = True
split = True
lineColour = [0,0,0]
fillColour = [1,1,1]
startBrightness = 255
endBrightness = 0


#================================================== Program setup

screen = pg.display.set_mode(dim)
centre = [X//2 for X in dim]


#================================================== Create pattern

mainOutline = [[sin((2*pi*x)/n), cos((2*pi*x)/n)]   for x in range(n)]
mainOutline = [[round((r*Y)+(dim[y]//2))  for y, Y in enumerate(X)]  for X in mainOutline]

subOutline = [midway(mainOutline[x], mainOutline[(x+1)%len(mainOutline)])   for x in range(n)]

indieOutlines = [[[centre, subOutline[x-1], mainOutline[x], subOutline[x]]]   for x in range(n)]

for x, X in enumerate(indieOutlines):
    indieOutlines[x] = all_layers(X, unit, centre)


#================================================== Draw pattern

screen.fill((255,255,255))

if fill:
    gradient = (endBrightness - startBrightness) // len(indieOutlines[0])
    for X in indieOutlines:
        for y, Y in enumerate(X):
            tempColour = [255 - (startBrightness + (Z * y * gradient))   for Z in fillColour]
            pg.draw.polygon(screen, tempColour, [[round(B)   for B in A]   for A in Y])
            if split:
                tempColour = [255 - Z   for Z in tempColour]
                if y != len(X)-1:
                    points = [Y[0], X[y+1][1], X[y+1][0], X[y+1][3]]
                else:
                    points = [Y[0], Y[1], Y[3]]
                points = [[round(B)   for B in A]   for A in points]
                pg.draw.polygon(screen, tempColour, points)

else:
    for X in indieOutlines:
        for Y in X:
            for z in range(len(Y)):
                pg.draw.line(screen, lineColour, Y[z], Y[z-1])

pg.display.update()
done = False
while not done:
    for E in pg.event.get():
        if E.type == pg.QUIT:
            done = True
pg.quit()
