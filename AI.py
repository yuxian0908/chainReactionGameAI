from Player import Player

class AI(Player):
    def __init__(self, name):
        super(AI, self).__init__(name)

    def think(self, board):
        self.makeMove(board,1,1)



class GameTree:
    def __init__(self, row, col, b, AI):
        self.children = [[0 for x in range(row)] for y in range(col)]
        self.board = Board(row, col).copy(b)
        self.row = row
        self.col = col
        self.AI = AI

    # make children game tree
    def makeChild(self):
        for i in range(self.row):
            for j in range(self.col):
                if(self.AI.canMove(self.board, i, j)):
                    nB = Board(row, col).copy(board)
                    self.AI.makeMove(nB, i, j)
                    self.children[i][j] = nB
