from matplotlib import image

live = 1
dead = 1 - live

size = [33, 67]
centre = (size[1] // 2)
start = [0, centre]
data = [[dead for y in range(size[1])] for x in range(size[0])]

def xor(a, b):
    return (a and not b) or (b and not a)

def is_odd(a, b, c):
    return (a + b + c) % 2

data[start[0]][start[1]] = live
for l in range(1, size[0]):
    for x in range(1, size[1]-1):
        #data[l][x] = is_odd(data[l-1][x-1], data[l-1][x], data[l-1][x+1])
        if xor(data[l-1][x-1] == live, data[l-1][x+1] == live):
            data[l][x] = live

image.imsave("rule_90_2.png", data, cmap="gray")
