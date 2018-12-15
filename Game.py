from Board import Board
from Player import Player

class Game:
    def __init__(self, row, col):
        self.row = row
        self.col = col

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
            print(players[(playerIndex+1)%len(players)].color+"'s turn")
            inp = input()
        

if __name__ == '__main__':
    game = Game(7,6)
    game.go()