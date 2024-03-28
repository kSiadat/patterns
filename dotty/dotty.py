from matplotlib import image as matImg

def create_pattern(maxWidth):
    centre1 = round((maxWidth - 1) // 2)
    centre2 = round(maxWidth // 2)
    n = round((maxWidth ** (1/2)) // 1) - 1

    current = 0
    baseLine = [0]
    for x in range(2, n+2):
        current += x
        baseLine.append(current)
    for x in range(n-1):
        current += n - x
        baseLine.append(current)
    print(baseLine)

    dotPlot = []
    dotPlot.append(baseLine)
    for x in range(1, n+4):
        line = []
        for y in range(n):
            line.append(dotPlot[x-1][y] + x)
        for y in range(n, 2*n):
            line.append(dotPlot[x-1][y] - x)
        dotPlot.append(line)

    image = [[1 for y in range(maxWidth)] for x in range((2*n)+9)]
    for x, line in enumerate(dotPlot):
        for Y in line[:n]:
            if Y <= centre1:
                image[n+5+x][Y] = 0
                image[n+5-x][Y] = 0
        for Y in line[n:]:
            if Y >= centre2:
                image[n+5+x][Y] = 0
                image[n+5-x][Y] = 0

    return image

image = create_pattern(128)
print(image)

matImg.imsave("dotty.png", image, cmap="gray")
