from ChessPiece import ChessPiece

class Board:
    def __init__(self, row, col):
        self.row = row
        self.col = col

        self.table = []

        # initialize board table
        for i in range(row):
            r = []
            for j in range(col):
                if( (i==0 and j==0) or (i==0 and j==col-1) or (i==row-1 and j==0) or (i==row-1 and j==col-1) ):
                    r.append(ChessPiece(2,i,j))
                elif( i==0 or i==row-1 or j==0 or j==col-1 ):
                    r.append(ChessPiece(3,i,j))
                else:
                    r.append(ChessPiece(4,i,j))
            self.table.append(r)

    
    def printBoard(self):
        for i in range(self.row):
            temp = ""
            for j in range(self.col):
                temp = temp+" "+self.table[i][j].color+"-"+str(self.table[i][j].point)
            print(temp)