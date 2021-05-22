from tictactoe import *
from engine import *

inp = input("Do you want to play X? y/n:")

ttt = tictactoe(comp_cross=inp!='y')

while ttt.gameGoes():
    if ttt.isCompMove():
        ttt.compMove()
    else:
        is_legit = False
        while not is_legit:
            x = int(input("X: "))
            y = int(input("Y: "))
            is_legit = ttt.makeMove((x, y))

    ttt.printGrid()
