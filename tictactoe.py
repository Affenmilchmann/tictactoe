from engine import *
from time import time

class tictactoe:
    def __init__(self, comp_cross = True):
        self.grid = [ 
            ['-'] * 3,
            ['-'] * 3,
            ['-'] * 3
         ]

        self.cross_move = True
        self.comp_cross = comp_cross
        self.move_time = 0
        self.comp_predict = 0

        self.printGrid()

    def printGrid(self):
        print(chr(27) + "[2J")

        if self.comp_predict == -1:
            print("Damit! Im gonna lose!")
        elif self.comp_predict == 0:
            print("I wont lose. Its a draw at least. 100%")
        elif self.comp_predict == 1:
            print("I`m 100% sure Im gonna win!")

        print("It took me", self.move_time, "sec")

        for i in range(3):
            for j in range(3):
                print(self.grid[i][j], end=' ')
            print()
        print()

    def makeMove(self, pos):
        x = pos[0]
        y = pos[1]
        if x >= 0 and y >= 0 and x < 3 and y < 3:
            if self.grid[x][y] == "-":
                if self.cross_move:
                    self.grid[x][y] = "X"
                else:
                    self.grid[x][y] = "O"

                self.cross_move = not self.cross_move

                return True
            else:
                return False
        else:
            return False

    def compMove(self):
        t = time()

        arr0 = possibleMoves(self.grid)
        if (len(arr0) > 1):
            split_indx = int(len(arr0) / 2)
            arr1 = arr0[0:split_indx]
            arr2 = arr0[split_indx:len(arr0)]

            pos1 = Array('i', [-1, -1])
            out1 = Value('i', -2)
            pos2 = Array('i', [-1, -1])
            out2 = Value('i', -2)

            p1 = Process(target=parallelProcess, args=(self.grid, arr1, self.cross_move, self.comp_cross, pos1, out1))
            p2 = Process(target=parallelProcess, args=(self.grid, arr2, self.cross_move, self.comp_cross, pos2, out2))

            p1.start()
            p2.start()

            p1.join()
            p2.join()

            if out1.value > out2.value:
                res = [pos1[:], out1.value]
            else:
                res = [pos2[:], out2.value]

        else:
            res = getTheBestMove(self.grid, possibleMoves(self.grid), self.cross_move, self.comp_cross)
        self.move_time = round(time() - t, 3)
        self.makeMove(res[0])

        self.comp_predict = res[1]

    def isCompMove(self):
        return self.cross_move == self.comp_cross

    def gameGoes(self):
        res = checkVictory(self.grid)

        if res == "X":
            print("Cross wins!")
            return False
        elif res == "O":
            print("Circle wins!")
            return False
        elif res == "0-0":
            print("Draw!")
            return False
        else:
            return True

