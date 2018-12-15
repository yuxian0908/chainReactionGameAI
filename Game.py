from Board import Board
from Player import Player

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

    def go(self):

        # initialize chess board
        board = Board(self.row, self.col)
        board.printBoard()

        # initialize players
        players = []
        playerIndex = 0
        players.append(Player("G"))
        players.append(Player("R"))

        # get user input
        print(players[(playerIndex+1)%len(players)].color+"'s turn")
        inp = input()

        # user move
        while(inp!= "q"):
            try:
                move = [int(n) for n in inp.split()]
                # get nth player and make move
                playerIndex = (playerIndex+1)%len(players)
                players[playerIndex].makeMove(board, move[0], move[1])
            except Exception as error:
                playerIndex = playerIndex-1
                print(repr(error))

            board.printBoard()
            
            # count the round and judge the game
            self.count = self.count+1
            j = self.judge(board)
            if j!="" and self.count>1:
                print(j+" wins!")
                return
            # next round
            print(players[(playerIndex+1)%len(players)].color+"'s turn")
            inp = input()
    

if __name__ == '__main__':
    game = Game(7,6)
    game.go()