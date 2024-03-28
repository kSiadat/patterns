from math import sin, cos, pi
from matplotlib import image as matImg
import pygame as pg


def roundList(L):
    return [round(X)   for X in L]


class Shape_Alternate():
    def __init__(self, fieldSize, sides):
        pg.init()
        self.fieldSize = fieldSize
        self.field = pg.Surface(self.fieldSize)
        self.field.fill((255,255,255))
        self.temp = pg.Surface(self.fieldSize)
        self.n = sides
        if self.fieldSize[0] < self.fieldSize[1]:
            self.r = self.fieldSize[0] / 2
        else:
            self.r = self.fieldSize[1] / 2
        self.calc_corners()

    def calc_corners(self):
        def calcX(x):
            return (self.fieldSize[0] / 2) + (sin((2*pi*x + pi) / self.n) * self.r)
        def calcY(x):
            return (self.fieldSize[1] / 2) + (cos((2*pi*x + pi) / self.n) * self.r)
        self.corners = [[calcX(x), calcY(x)]   for x in range(self.n)]

    def draw_transparent(self, start, end):
        def line(x):
             for y in range(self.fieldSize[1]):
                 if self.temp.get_at((x, y)) == (0,0,0,255):
                     old = self.field.get_at((x, y))
                     old[0] -= 1
                     self.field.set_at((x, y), old)
                     return None
        self.temp.fill((255,255,255))
        pg.draw.line(self.temp, (0,0,0), roundList(start), roundList(end))
        for x in range(self.fieldSize[0]):
            line(x)

    def plot_outline(self):
        for x in range(len(self.corners)):
            pg.draw.line(self.field, (0,0,0), roundList(self.corners[x]), roundList(self.corners[x-1]))

    def plot_allLines(self, transparent=False):
        global index
        for x in range(len(self.corners)):
            for y in range(len(self.corners) - x - 1):
                if transparent:
                    self.draw_transparent(self.corners[-x], self.corners[(-x-y-1)%self.n])
                else:
                    pg.draw.line(self.field, (0,0,0), roundList(self.corners[-x]), roundList(self.corners[(-x-y-1)%self.n]))
                #self.save_demo()

    def plot_fill(self):
        def line(start, col=0):
            colours = ((255,255,255,255), (0,0,0,255))
            pos = roundList(start)
            inShape = False
            while 0 <= pos[0] < self.fieldSize[0]  and  0 <= pos[1] < self.fieldSize[1]:
                posCol = self.field.get_at((pos[0], pos[1]))
                if posCol[0] < 255:
                    col = (col + (255 - posCol[0])) % 2
                    inShape = True
                elif inShape:
                    self.field.set_at((pos[0], pos[1]), colours[col])
                pos[1] += 1

        def whiteLine(start):
            pos = roundList(start[:])
            for x in range(self.fieldSize[1]):
                if self.field.get_at(pos)[0] > 0:
                    return None
                else:
                    self.field.set_at(pos, (255,255,255,255))
                pos[1] -= 1

        self.plot_allLines(True)
        index = (self.n // 4) - 1
        for x in range((self.n//2)-1):
            for y in range(round(self.corners[index-x-1][0]), round(self.corners[index-x][0])):
                line([y, 0], x%2)
                #self.save_demo()
        for x in range(self.fieldSize[0]):
            whiteLine([x, self.fieldSize[1]-1])
            #self.save_demo()
        self.plot_allLines()

    def save(self, file, cmap="gray"):
        matImg.imsave(file+".png", pg.PixelArray(self.field), cmap=cmap)

    def save_demo(self):
        global index
        self.save(f"demonstration_{index}")
        index += 1


if __name__ == "__main__":
    """
    index = 0
    shape = Shape_Alternate([400, 400], 8)
    shape.plot_fill()
    """
    for x in range(2, 10):
        n = 4*x
        shape = Shape_Alternate([400, 400], n)
        shape.plot_fill()
        shape.save(f"Shape alternate {n}")
        print(n)
