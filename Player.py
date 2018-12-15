from Board import Board

direction = [[1,0],[-1,0],[0,1],[0,-1]]
class Player:
    def __init__(self, color):
        self.color = color

    def makeMove(self, board, row, col, explode=False):
        # check if move is out of board
        if not explode and (row>board.row or col>board.col or row<0 or col<0):
            raise ValueError('out of board.')

        # if is explode then do not throw exception
        if explode and (row>board.row or col>board.col or row<0 or col<0):
            return

        # if move is legal
        if board.table[row][col].color=="w" or board.table[row][col].color==self.color or explode:
            board.table[row][col].setColor(self.color)
            if board.table[row][col].addOne():
                board.table[row][col].explosion()
                for i in direction:
                    self.makeMove(board, row+i[0], col+i[1], True)
        else:
            raise ValueError('some one took this place.')
