from matplotlib import image

live = 0
dead = 1 - live

def left(plane):
    if plane[0] == 0:
        return [-plane[1], 0]
    return [0, plane[0]]

def right(plane):
    if plane[0] == 0:
        return [plane[1], 0]
    return [0, -plane[0]]

def step(pos, plane, scale):
    if scale > 1:
        diff = [plane[x] * scale  for x in range(2)]
        end = [pos[x] + diff[x] - plane[x]  for x in range(2)]
        lines = [[pos[:], diff[:]]]
        new_scale = scale // 2
        lines += step(end, left(plane), new_scale)
        lines += step(end, plane, new_scale)
        lines += step(end, right(plane), new_scale)
        return lines
    return []

def full(scale, centre):
    lines = step(centre, [-1, 0], scale)
    lines += step(centre, [1, 0], scale)
    lines += step(centre, [0,-1], scale)
    lines += step(centre, [0, 1], scale)
    return lines

def full_full(scale):
    centre = [2 * scale  for x in range(2)]
    lines = []
    while scale > 1:
        lines += full(scale, centre)
        scale //= 2
    return lines

def mark(data, line):
    i = (line[1][0] == 0)
    sign = 2 * (line[1][i] > 0) - 1
    for x in range(abs(line[1][i])):
        a = line[0][0] + (x * sign * (1 - i))
        b = line[0][1] + (x * sign * i)
        data[a][b] = live

def assemble(lines, scale):
    dim = 4 * scale
    data = [[dead  for y in range(dim)]  for x in range(dim)]
    for X in lines:
        mark(data, X)
    return data

def draw(lines, scale):
    image.imsave("bloom.png", assemble(lines, scale), cmap="gray")

if __name__ == "__main__":
    scale = 1024
    lines = full_full(scale)
    draw(lines, scale)
