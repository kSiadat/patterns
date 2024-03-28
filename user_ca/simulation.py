from matplotlib import image
from random import randint

from template import r_to_bool, t


# gets population of grid
def get_population(grid):
    return sum([sum(grid[x])  for x in range(size)])

# returns new cell state given neighbourhood and templates tha map to 1
def evaluate_complete(rule, border, centre):
    data = border + [centre]
    for X in rule:
        live = True
        for y in range(5):
            if data[y] != X[y]:
                live = False
        if live:
            return 1
    return 0

# updates cell state given custom outer-totalistic rule
def evaluate_outer_distinct(rule, border, centre):
    half = centre * 6
    total = sum(border)
    if (total == 4 and rule[half]) or (total == 3 and rule[half+1]) or (total == 2 and rule[half+2] and border[0] == border[2]) or (total == 2 and rule[half+3] and border[0] != border[2]) or (total == 1 and rule[half+4]) or (total == 0 and rule[half+5]):
        return 1
    return 0

# updates cell state given pure outer-totalistic rule
def evaluate_outer(rule, border, centre):
    half = centre * 5
    total = sum(border)
    if (total == 4 and rule[half]) or (total == 3 and rule[half+1]) or (total == 2 and rule[half+2]) or (total == 1 and rule[half+3]) or (total == 0 and rule[half+4]):
        return 1
    return 0

# updates cell state gicen totalistic rule
def evaluate_total(rule, border, centre):
    total = sum(border) + centre
    return rule[5-total]

# gets neighbours of a cell
def neighbours(grid, x, y):
    n = x - 1
    e = (y + 1) % len(grid[0])
    s = (x + 1) % len(grid)
    w = y - 1
    return [grid[n][y], grid[x][e], grid[s][y], grid[x][w]]

# updates entire grid
def update(rule, grid, evaluator):
    new = [[0  for y in range(len(grid[x]))]  for x in range(len(grid))]
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            new[x][y] = evaluator(rule, neighbours(grid, x, y), grid[x][y])
    return new

# prints grid
def display(grid):
    for X in grid:
        print(X)
    print()

# converts bit-array rule to list of templates that map to 1
def r_to_set(rule):
    new = [t[31-x]  for x, X in enumerate(rule)  if X]
    return new

if __name__ == "__main__":
    print(evaluate_outer([0, 0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1], 0))
