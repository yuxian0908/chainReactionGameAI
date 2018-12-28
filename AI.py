from Player import Player
from Board import Board

class AI(Player):
    def __init__(self, name, enemy, beginHard, nextHard):
        super(AI, self).__init__(name)
        self.enemy = enemy
        self.beginHard = beginHard
        self.nextHard = nextHard
        
    def think(self, board, count):
        nB = Board(board.row, board.col).copy(board)
        gTree = GameTree(nB, self)
        if count<self.nextHard:
            gTree.makeChild([self, self.enemy], 0, self.beginHard)
        else:
            gTree.makeChild([self, self.enemy], 0, self.beginHard+1)

        maxCor = [0, 0]
        maxi = -100000
        for i in range(gTree.row):
            for j in range(gTree.col):
                if gTree.children[i][j] != 0 and maxi < gTree.children[i][j].sitPoint:
                    maxi = gTree.children[i][j].sitPoint
                    maxCor = gTree.children[i][j].coordinate
        
        self.makeMove(board, maxCor[0], maxCor[1])

class GameTree:
    def __init__(self, root, AI, coorR=-1, coorC=-1):
        self.row = root.row
        self.col = root.col
        self.children = [[0 for x in range(self.col)] for y in range(self.row)]
        self.board = root
        self.AI = AI
        self.sitPoint = self.calSituation()
        self.coordinate = [coorR, coorC]

    # make children game tree
    def makeChild(self, player, layer, limit):
        if layer>limit:
            return
        mini = 100000
        for i in range(self.row):
            for j in range(self.col):
                if(player[layer%2].canMove(self.board, i, j)):
                    nB = Board(self.row, self.col).copy(self.board)
                    player[layer%2].makeMove(nB, i, j)
                    self.children[i][j] = GameTree(nB, self.AI, i, j)
                    self.children[i][j].makeChild(player, layer+1, limit)
                    mini = min(mini, self.children[i][j].sitPoint)
        self.sitPoint = mini

    def calSituation(self):
        alliance = 0
        enemy = 0
        for i in range(self.row):
            for j in range(self.col):
                if self.board.table[i][j].color == self.AI.color:
                    alliance = alliance+self.board.table[i][j].point
                else:
                    enemy = enemy+self.board.table[i][j].point
        return alliance-enemy

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
