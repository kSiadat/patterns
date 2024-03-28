from matplotlib import image as matImg


def create_pattern(m, size, colourMap):
    if size % m != 0:
        size = m * (round(size // m) + 1)

    unit = size // m

    field = [[((x * y) % m) / (m-1)   for y in range(m)]   for x in range(m)]

    image = [[0   for y in range(size)]   for x in range(size)]

    for x, X in enumerate(field):
        for y, Y in enumerate(X):
            for a in range(unit):
                for b in range(unit):
                    image[(x*unit)+a][(y*unit)+b] = Y

    matImg.imsave(f"Field_{m}.png", image, cmap=colourMap)


for x in range(1, 12):
    print(2**x)
    create_pattern(2**x, 2000, "RdPu")
