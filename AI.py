from Player import Player
from Board import Board

class AI(Player):
    def __init__(self, name, enemy):
        super(AI, self).__init__(name)
        self.enemy = enemy

    def think(self, board):
        self.makeMove(board,1,1)
        test = GameTree(board, self)
        test.makeChild()
        test.printGameTree()


class GameTree:
    def __init__(self, root, AI):
        self.row = root.row
        self.col = root.col
        self.children = [[0 for x in range(self.col)] for y in range(self.row)]
        self.board = Board(self.row, self.col).copy(root)
        self.AI = AI

    # make children game tree
    def makeChild(self):
        for i in range(self.row):
            for j in range(self.col):
                if(self.AI.canMove(self.board, i, j)):
                    nB = Board(self.row, self.col).copy(self.board)
                    self.AI.makeMove(nB, i, j)
                    self.children[i][j] = nB

    def printGameTree(self):
        print("root:")
        self.board.printBoard()
        print("children:")
        print(self.children)
        for i in range(0, self.row):
            for j in range(0, self.col):
                if(self.children[i][j] != 0):
                    self.children[i][j].printBoard()
                    print()
