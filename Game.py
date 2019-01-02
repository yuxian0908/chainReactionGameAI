import sys
from Board import Board
from Player import Player
from AI import AI

class Game:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.count = 0

    def judge(self, board):
        winner = ""
        row = self.row
        col = self.col
        for i in range(row):
            for j in range(col):
                if winner != "" and winner!= board.table[i][j].color and board.table[i][j].color!="w":
                    return ""
                if winner == "" and board.table[i][j].color != "w":
                    winner = board.table[i][j].color
        return winner

    def goPeople(self, people):

        # initialize chess board
        board = Board(self.row, self.col)
        board.printBoard()

        # initialize players
        players = []
        playerIndex = 0
        for i in people:
            players.append(Player(i))

        # get user input
        print(players[playerIndex].color+"'s turn")
        inp = input()

        # user movement
        while(inp!= "q"):
            try:
                move = [int(n) for n in inp.split()]
                # get nth player and make move
                players[playerIndex].makeMove(board, move[0], move[1])
                playerIndex = (playerIndex+1)%len(players)
            except Exception as error:
                self.count = self.count-1
                print(repr(error))

            board.printBoard()

            # count the round and judge the game
            self.count = self.count+1
            j = self.judge(board)
            if j!="" and self.count>1:
                print(j+" wins!")
                return
            # next round
            print(players[playerIndex].color+"'s turn")
            inp = input()
    
    def goAI(self, difficulty):

        # setup difficulty
        beginHard = 0
        nextHard = 50
        if difficulty==0:
            beginHard = 0
            nextHard = 50
        elif difficulty==1:
            beginHard = 0
            nextHard = 20
        elif difficulty==2:
            beginHard = 1
            nextHard = 40
        elif difficulty==3:
            beginHard = 1
            nextHard = 20
        elif difficulty==4:
            beginHard = 2
            nextHard = 40
        elif difficulty==5:
            beginHard = 2
            nextHard = 20

        # initialize chess board
        board = Board(self.row, self.col)
        board.printBoard()

        # initialize players
        p1 = Player("P")
        players = [p1, AI("C", p1, beginHard, nextHard)]
        playerIndex = 0
        
        # get user input
        print(players[playerIndex].color+"'s turn")
        inp = input()

        # user movement
        while(inp!= "q"):
            try:
                move = [int(n) for n in inp.split()]

                try:
                    # player makes move
                    players[0].makeMove(board, move[0], move[1])
                    board.printBoard()
                    # count the round and judge the game
                    self.count = self.count+1
                    j = self.judge(board)
                    if j!="" and self.count>1:
                        print(j+" wins!")
                        return
                    print(players[1].color+"'s turn")

                except RecursionError as error:
                    print(players[0].color+" wins!")

                try:
                    # AI make move
                    players[1].think(board, self.count)
                    board.printBoard()
                    # count the round and judge the game
                    self.count = self.count+1
                    j = self.judge(board)
                    if j!="" and self.count>1:
                        print(j+" wins!")
                        return
                    print(players[0].color+"'s turn")
                
                except RecursionError as error:
                    print(players[1].color+" wins!")

            except ValueError as error:
                self.count = self.count-1
                print(repr(error))


            inp = input()

    def goAI_GAME(self, dif1, dif2):
        # setup difficulty
        beginHard1 = 0
        nextHard1 = 50
        if dif1==0:
            beginHard1 = 0
            nextHard1 = 50
        elif dif1==1:
            beginHard1 = 0
            nextHard1 = 20
        elif dif1==2:
            beginHard1 = 1
            nextHard1 = 40
        elif dif1==3:
            beginHard1 = 1
            nextHard1 = 20
        elif dif1==4:
            beginHard1 = 2
            nextHard1 = 40
        elif dif1==5:
            beginHard1 = 2
            nextHard1 = 20

        beginHard2 = 0
        nextHard2 = 50
        if dif2==0:
            beginHard2 = 0
            nextHard2 = 50
        elif dif2==1:
            beginHard2 = 0
            nextHard2 = 20
        elif dif2==2:
            beginHard2 = 1
            nextHard2 = 40
        elif dif2==3:
            beginHard2 = 1
            nextHard2 = 20
        elif dif2==4:
            beginHard2 = 2
            nextHard2 = 40
        elif dif2==5:
            beginHard2 = 2
            nextHard2 = 20
            
        # initialize chess board
        board = Board(self.row, self.col)
        board.printBoard()

        # initialize players
        p1 = AI("P", Player("C"), beginHard1, nextHard1)
        p2 = AI("C", p1, beginHard2, nextHard2)
        players = [p1, p2]
        playerIndex = 0
        
        # get user input
        print(players[playerIndex].color+"'s turn")

        # user movement
        while(True):
            try:
                # player makes move
                players[0].think(board, self.count)
                board.printBoard()
                # count the round and judge the game
                self.count = self.count+1
                j = self.judge(board)
                if j!="" and self.count>1:
                    print(j+" wins!")
                    break
                print(players[1].color+"'s turn")

            except RecursionError as error:
                print(players[0].color+" wins!")
                break

            try:
                # AI make move
                players[1].think(board, self.count)
                board.printBoard()
                # count the round and judge the game
                self.count = self.count+1
                j = self.judge(board)
                if j!="" and self.count>1:
                    print(j+" wins!")
                    break
                print(players[0].color+"'s turn")
            
            except RecursionError as error:
                print(players[1].color+" wins!")
                break

if __name__ == '__main__':
    init = sys.argv

    if init[1]=="People" :
        # for multiple user
        game = Game(int(init[2]),int(init[3]))
        people = [n for n in input().split()]
        game.goPeople(people)

    elif(init[1]=="AI"):
        # for AI
        game = Game(5,6)
        game.goAI(int(init[2]))
    
    elif(init[1]=="AI_GAME"):
        game = Game(5,6)
        game.goAI_GAME(int(init[2]),int(init[3]))
