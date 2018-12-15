class ChessPiece:
    def __init__(self, margin, row, col):
        self.margin = margin # attr which controls the point of explosion
        self.point = 0
        self.row = row
        self.col = col
        self.color = "w"

    # return whether the piece should explode
    def addOne(self):
        self.point = self.point+1
        return self.point >= self.margin

    def explosion(self):
        self.color = "w"
        self.point = 0
    
    def setColor(self, color):
        self.color = color

    

    
    