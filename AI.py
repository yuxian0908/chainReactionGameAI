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
        GameTree.minimax(gTree, [self, self.enemy], 0, self.beginHard, -100000, 100000)
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

    @staticmethod
    def minimax(node, player, layer, limit, alpha, beta):
        if layer==limit:
            return node.sitPoint
        
        if layer==0:
            try:
                count=0
                for i in range(node.row):
                    for j in range(node.col):
                        if(player[layer%2].canMove(node.board, i, j)):
                            count = count+1
                            if count==1:
                                node.coordinate = [i,j]
                            nB = Board(node.row, node.col).copy(node.board)
                            try:
                                player[layer%2].makeMove(nB, i, j)
                                node.children[i][j] = GameTree(nB, node.AI, i, j)
                                v = GameTree.minimax(node.children[i][j], player, layer+1, limit, alpha, beta)
                                if alpha<v:
                                    alpha = v
                                    node.coordinate = [i,j]
                                if beta <= alpha:
                                    node.coordinate = [i,j]
                                    raise GetOutOfLoop
                            except RecursionError as error:
                                alpha = 100000
                                node.coordinate = [i,j]
                                raise GetOutOfLoop
            except GetOutOfLoop:
                pass
            node.sitPoint = alpha
            return alpha

        if layer!=0 and layer%2==0:
            try:
                for i in range(node.row):
                    for j in range(node.col):
                        if(player[layer%2].canMove(node.board, i, j)):
                            nB = Board(node.row, node.col).copy(node.board)
                            # prevent recursion error
                            try:
                                player[layer%2].makeMove(nB, i, j)
                                node.children[i][j] = GameTree(nB, node.AI, i, j)
                                alpha = max(alpha,GameTree.minimax(node.children[i][j], player, layer+1, limit, alpha, beta))
                                if beta <= alpha:
                                    raise GetOutOfLoop
                            except RecursionError as error:
                                alpha = 100000
                                raise GetOutOfLoop
            except GetOutOfLoop:
                pass

            node.sitPoint = alpha
            return alpha

        if layer%2==1:
            try:
                for i in range(node.row):
                    for j in range(node.col):
                        if(player[layer%2].canMove(node.board, i, j)):
                            nB = Board(node.row, node.col).copy(node.board)
                            # prevent recursion error
                            try:
                                player[layer%2].makeMove(nB, i, j)
                                node.children[i][j] = GameTree(nB, node.AI, i, j)
                                beta = min(beta,GameTree.minimax(node.children[i][j], player, layer+1, limit, alpha, beta))
                                if beta <= alpha:
                                    raise GetOutOfLoop
                            except RecursionError as error:
                                beta = -100000
                                raise GetOutOfLoop
            except GetOutOfLoop:
                pass

            node.sitPoint = beta
            return beta

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

    def printSituation(self):
        for i in range(0, self.row):
            temp = ""
            for j in range(0, self.col):
                if self.children[i][j]==0:
                    temp = temp+" "+"n"
                else:    
                    temp = temp+" "+str(self.children[i][j].sitPoint)
            print(temp)

class GetOutOfLoop( Exception ):
    pass