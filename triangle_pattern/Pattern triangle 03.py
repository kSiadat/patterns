#================================================== Imports
import pygame as pg
from math import log2
from matplotlib import image as matImg


#================================================== Functions
def hyp(pos1, pos2):
    '''Returns hypotenuse of a right angle triangle given the other sides'''
    return (((pos1[0]-pos2[0])**2)+((pos1[1]-pos2[1])**2))**(1/2)

def start(old):
    '''Creates the first triangle'''
    return [avg(old[0],old[2]),avg(old[1],old[2]),old[1]]

def reflect(point, reflect, factor=1):
    '''Reflects 1 point across another and can multiply the distance on the other side by a factor'''
    newPoint = point[:]
    for x in range(2):
        newPoint[x] += (1+factor)*(reflect[x]-point[x])
    return newPoint

def add(old):
    '''Starts a new set of triangles'''
    new = [0,0,0]
    new[0] = reflect(old[1],avg(old[0],old[2]))
    new[1] = reflect(avg(old[1],old[2]),avg(old[0],old[2]),2)
    new[2] = old[0]
    return new

def repeat(old):
    '''Continues a set of triangles'''
    new = [0,0,0]
    new[0] = reflect(avg(old[0],old[2]),avg(old[0],old[1]))
    new[1] = reflect(reflect(old[2],avg(old[0],old[2]),0.5), avg(old[0],old[1]),2)
    new[2] = old[1]
    return new

def avg(pos1, pos2):
    '''Returns the midpoint between 2 other points'''
    return [round((pos1[0]+pos2[0])/2), round((pos1[1]+pos2[1])/2)]

def size(triangle, size):
    '''Checks to see if the triangle is less than the size limit'''
    for x in range(2):
        if hyp(triangle[0], triangle[x+1])<=size:
            return True
    return False

def create_pattern(limit, startLength, initial=None):
    '''Creates 1 pattern'''
    colMod = 255/(2*(log2(startLength)-1-log2(limit)))
    if initial == None:
        initial = [[0,0],[0,startLength],[startLength,startLength]]
    triangles = []
    triangles.append([start(initial)])
    while not size(triangles[0][-1],limit):
        triangles[0].append(repeat(triangles[0][-1]))
    count = 0
    new = add(triangles[0][0])
    while not size(new,limit):
        triangles.append([])
        for x in range(len(triangles[-2])):
            subNew = add(triangles[-2][x])
            if not size(subNew,limit):
                triangles[-1].append(subNew)
            while not size(triangles[-1][-1],limit*2):
                triangles[-1].append(repeat(triangles[-1][-1]))
        new = add(triangles[-1][0])
        count+=1
    return triangles, colMod

def draw(triangles, colMod, mod, col, line=False):
    '''Draws 1 pattern, can do different colours and translations'''
    for x,X in enumerate(triangles):
        for Y in X:
            for z, Z in enumerate(Y):
                coordinates = [[Z[0]+mod[0], Z[1]+mod[1]] for Z in Y]
            if line:
                for i in range(3):
                    pg.draw.line(screen, (0,0,0), Y[i], Y[i-1])
            else:
                if col[0][0]:
                    pg.draw.polygon(screen, (255-round((x+1)*colMod), 255-round((x+1)*colMod), 255-round((x+1)*colMod)), [[round(P) for P in pair] for pair in coordinates])
                elif col[0][1]:
                    pg.draw.polygon(screen, (round((x+1)*colMod),round((x+1)*colMod),round((x+1)*colMod)), [[round(P) for P in pair] for pair in coordinates])
                else:
                    colour = [0,0,0]
                    colour[col[1][0]] = 255-(x*colMod)
                    colour[col[1][1]] = x*colMod
                    pg.draw.polygon(screen, (colour), coordinates)
    pg.display.update()


#================================================== Setup
pg.init()
screenX = 1920
screenY = 1080
screen = pg.display.set_mode((screenX,screenY))
col = [[True, False], [0,2]]
limit = 4
startLength = 1024


#================================================== Main
screen.fill((255,255,255))
triangles, colMod = create_pattern(limit, startLength, [[0,0],[0,startLength],[startLength,startLength]])
draw(triangles, colMod, (0,0), col)
triangles, colMod = create_pattern(limit, startLength, [[0,startLength],[0,0],[-startLength,0]])
draw(triangles, colMod, (screenX,0), col)
image = pg.PixelArray(screen)
matImg.imsave("desktop.png", image, cmap="gray")
pg.quit()
