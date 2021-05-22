from multiprocessing import Process, Array, Value
from math import inf as infinity

def checkVictory(grid):
    for i in range(3):
        for j in range(2):
            if grid[i][j] == "-" or grid[i][j] != grid[i][j + 1]:
                break
        else:
            return grid[i][0]

    for i in range(3):
        for j in range(2):
            if grid[j][i] == "-" or grid[j][i] != grid[j + 1][i]:
                break
        else:
            return grid[0][i] 

    for i in range(2):
        if grid[i][i] == "-" or grid[i][i] != grid[i + 1][i + 1]:
            break
    else:
        return grid[0][0] 

    for i in range(2):
        if grid[2 - i][i] == "-" or grid[2 - i][i] != grid[2 - i - 1][i + 1]:
            break
    else:
        return grid[2][0] 

    draw = True
    for i in range(3):
        for j in range(3):
            if grid[i][j] == '-':
                draw = False
    
    if draw:
        return "0-0" 

    return "-"



def possibleMoves(grid):
    moves = []

    for i in range(3):
        for j in range(3):
            if grid[i][j] == "-":
                moves.append((i, j))

    return moves

def getOutcome(grid, am_i_a_cross):
    result = checkVictory(grid)
            
    if result == "X":
        if am_i_a_cross:
            outcome = 1
        else:
            outcome = -1
    elif result == "O":
        if am_i_a_cross:
            outcome = -1
        else:
            outcome = 1
    elif result == "0-0":
        outcome = 0
    else: 
        return False

def getTheBestMove(grid, moves, cross_move, am_i_a_cross):
    best = []

    if cross_move == am_i_a_cross:
        best = [(-1, -1), -infinity]
    else:
        best = [(-1, -1), +infinity]


    for x, y in moves:
        if cross_move:
            grid[x][y] = "X"
        else:
            grid[x][y] =  "O"

        result = checkVictory(grid)
            
        if result == "X":
            if am_i_a_cross:
                outcome = 1
            else:
                outcome = -1
        elif result == "O":
            if am_i_a_cross:
                outcome = -1
            else:
                outcome = 1
        elif result == "0-0":
            outcome = 0
        elif result == "-":
            outcome = getTheBestMove(grid, possibleMoves(grid), not cross_move, am_i_a_cross)[1]

        grid[x][y] = "-"

        if cross_move == am_i_a_cross:
            if outcome > best[1]:
                best = [(x, y), outcome]
        else:
            if outcome < best[1]:
                best = [(x, y), outcome]

    return best

def parallelProcess(grid, moves, cross_move, am_i_a_cross, pos, out):
    result = getTheBestMove(grid, moves, cross_move, am_i_a_cross)
    pos[0] = result[0][0]
    pos[1] = result[0][1]
    out.value = result[1]