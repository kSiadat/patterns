from pygame import display, draw, event, QUIT, time, mouse, KEYUP, KEYDOWN
from pygame import init as pgInit, quit as pgQuit

from template import to_bool
from settings import evaluator, init, rule, scale, size
from simulation import r_to_set, update
from simulation import evaluate_complete, evaluate_outer, evaluate_outer_distinct, evaluate_total



def init_single(size):
    grid = [[0  for y in range(size[1])]  for x in range(size[0])]
    centre = [X // 2  for X in size]
    grid[centre[0]][centre[1]] = 1
    return grid

if __name__ == "__main__":
    pgInit()
    screen = display.set_mode([X * scale  for X in size])
    clock = time.Clock()
    fps = 1
    print(rule)

    if init == "single":
        grid = init_single(size)

    if evaluator == "complete":
        rule = r_to_set(to_bool(rule, 32))
        evaluator = evaluate_complete
    if evaluator == "outer":
        rule = to_bool(rule, 10)
        evaluator = evaluate_outer
    if evaluator == "outer_distinct":
        rule = to_bool(rule, 12)
        evaluator = evaluate_outer_distinct
    if evaluator == "total":
        rule = to_bool(rule, 6)
        evaluator = evaluate_total

    done = False
    while not done:
        for E in event.get():
            if E.type == QUIT:
                done = True
        grid = update(rule, grid, evaluator)
        screen.fill([255,255,255])
        for x in range(len(grid)):
            for y in range(len(grid[0])):
                if grid[x][y] == 1:
                    draw.rect(screen, [0,0,0], [x * scale, y * scale, scale, scale])
        display.update()
        #clock.tick(fps)
    pgQuit()
        
    
            
