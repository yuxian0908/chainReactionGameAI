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
            gTree.makeChild([self, self.enemy], 0, self.beginHard, gTree)
        else:
            gTree.makeChild([self, self.enemy], 0, self.beginHard+1, gTree)
        
        print(str(gTree.coordinate[0])+" "+str(gTree.coordinate[1]))
        self.makeMove(board, gTree.coordinate[0], gTree.coordinate[1])

class GameTree:
    def __init__(self, root, AI, coorR=-1, coorC=-1):
        self.row = root.row
        self.col = root.col
        self.children = [[0 for x in range(self.col)] for y in range(self.row)]
        self.board = root
        self.AI = AI
        self.sitPoint = self.calSituation()
        self.coordinate = [coorR, coorC]
        self.curMax = -100000

    # make children game tree
    def makeChild(self, player, layer, limit, root):
        if layer>limit:
            return
        self.sitPoint = 100000
        count = 0
        for i in range(self.row):
            for j in range(self.col):
                if(player[layer%2].canMove(self.board, i, j)):
                    count = count+1

                    # default coordinate
                    if layer==0 and count==1:
                        self.coordinate = [i,j]
                    nB = Board(self.row, self.col).copy(self.board)

                    # prevent recursion error
                    try:
                        player[layer%2].makeMove(nB, i, j)
                    except RecursionError as error:
                        if layer%2==0:
                            self.curMax = 100000
                            self.coordinate = [i,j]
                            break
                        else:
                            self.sitPoint = -100000
                        continue

                    # recursive call
                    self.children[i][j] = GameTree(nB, self.AI, i, j)
                    self.children[i][j].makeChild(player, layer+1, limit, root)
                    self.sitPoint = min(self.sitPoint, self.children[i][j].sitPoint)

                    # cut tree
                    if layer==0:
                        if self.curMax<self.children[i][j].sitPoint:
                            self.curMax = self.children[i][j].sitPoint
                            self.coordinate = self.children[i][j].coordinate
                    elif self.children[i][j].sitPoint<=root.curMax:
                        return


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