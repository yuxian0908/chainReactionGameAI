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
    
    def goAI(self):

        # initialize chess board
        board = Board(self.row, self.col)
        board.printBoard()

        # initialize players
        players = [Player("P"), AI("C")]
        playerIndex = 0
        
        # get user input
        print(players[playerIndex].color+"'s turn")
        inp = input()

        # user movement
        while(inp!= "q"):
            try:
                move = [int(n) for n in inp.split()]
                # player makes move
                players[0].makeMove(board, move[0], move[1])
                players[1].think(board)

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

if __name__ == '__main__':
    init = sys.argv

    if init[1]=="People" :
        # for multiple user
        game = Game(int(init[1]),int(init[2]))
        people = [n for n in input().split()]
        game.goPeople(people)

    elif(init[1]=="AI"):
        # for AI
        game = Game(5,6)
        game.goAI()
    