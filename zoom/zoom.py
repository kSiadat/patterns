from math import cos, pi, sin
from pygame import display, draw, event, QUIT, init as pg_init, quit as pg_quit


def distance(pos1, pos2):
    return (((pos2[0] - pos1[0]) ** 2) + ((pos2[1] - pos1[1]) ** 2)) ** 0.5

def extrapolate(pos1, pos2, diff):
    dist = distance(pos1, pos2)
    return [pos1[x] + (diff * ((pos2[x] - pos1[x]) / dist))  for x in range(2)]

def step(layers, diff):
    new = []
    if distance(layers[-1][0], layers[-1][1]) > 2 * diff:
        for x in range(len(layers[-1])):
            new.append(extrapolate(layers[-1][x-1], layers[-1][x], diff))
        layers.append(new)
        return step(layers, diff)
    return layers

def clean(pos, scale, centre):
    return [round((pos[x] * scale) + centre[x])  for x in range(2)]

def draw_zoom(screen, scale, dim, layers):
    centre = [dim[x] // 2  for x in range(2)]
    for X in layers:
        corners = [clean(Y, scale, centre)  for Y in X]
        for y in range(len(X)):
            draw.line(screen, (0,0,0), corners[y], corners[y-1])

def init_shape(sides, centre, r, rotate=False):
    angle = (2 * pi) / sides
    offset = rotate * (angle / 2)
    return [[centre[0] + r * sin(offset + angle * x),
             centre[1] + r * cos(offset + angle * x)]  for x in range(sides)]

def init_hexagon_triangle(centre, r, rotate=False):
    corners = init_shape(6, centre, r, rotate)
    triangles = []
    for x in range(len(corners)):
        triangles.append([centre[:], corners[x-1][:], corners[x][:]])
    return triangles


if __name__ == "__main__":
    pg_init()
    dim = [1000, 1000]
    screen = display.set_mode(dim)
    screen.fill((255,255,255))

    shapes = []
    everything = []
    
    centres = init_shape(6, [0, 0], 2 * 8.660254038)
    for X in centres:
        shapes += init_hexagon_triangle(X, 10, True)
    shapes += init_hexagon_triangle([0, 0], 10, True)
    
    for X in shapes:
        everything.append(step([X], 0.6666))
    for X in everything:
        draw_zoom(screen, 18, dim, X)
    display.update()

    done = False
    while not done:
        for E in event.get():
            if E.type == QUIT:
                done = True
    pg_quit()
