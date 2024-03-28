from matplotlib import image

live = 0
dead = 1 - live
flip = False

size = 128
start = [0, 0]
data = [[dead for y in range(size)] for x in range(size)]

def xor(a, b):
    return (a and not b) or (b and not a)

data[0][0] = live
if flip:
    data[size-1][size-1] = live
for l in range(1, size):
    for x in range(l+1):
        y = l - x
        if (x == 0) and (data[x][y-1] == live):
            data[x][y] = live
        elif (y == 0) and (data[x-1][y] == live):
            data[x][y] = live
        elif xor(data[x-1][y] == live, data[x][y-1] == live):
            data[x][y] = live
        if flip:
            data[size-x-1][size-y-1] = data[x][y]

degree = [[dead for y in range(size)] for x in range(size)]
for y in range(size):
    index = 1
    for x in range(size):
        if data[x][y] == live:
            degree[size-index][y] = live
            index += 1
image.imsave("graph.png", degree, cmap="gray")

image.imsave("rule_90.png", data, cmap="gray")
