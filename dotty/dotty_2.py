from matplotlib import image
from math import ceil

def layer(offset):
    data = [off for x in range(half)]
    index = offset
    step = 2
    while index < len(data):
        data[index] = on
        index += step
        step += 1
    return data

on = 0
off = 1 - on
size = 32
half = int(ceil(0.5*size*size) + size)

data = []
offset = 0
step = 1
while offset < half:
    data.append(layer(offset))
    offset += step
    step += 1

for x in range(len(data)):
    flip = data[x][:-(size%2)][:]
    flip.reverse()
    data[x] = data[x] + flip

for x in range(2, 2*len(data), 2):
    data = [data[x-1]] + data

image.imsave("dotty_2.png", data, cmap="gray")
