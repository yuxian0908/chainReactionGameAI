class ChessPiece:
    def __init__(self, margin, row, col):
        self.margin = margin # attr which controls the point of explosion
        self.point = 0
        self.row = row
        self.col = col
        self.color = "w"

    # copy constructor
    def copy(self, base):
        self.margin = base.margin
        self.point = base.point
        self.row = base.row
        self.col = base.col
        self.color = base.color
        return self

    # return whether the piece should explode
    def addOne(self):
        self.point = self.point+1
        return self.point >= self.margin

    def reset(self):
        self.color = "w"
        self.point = 0
    
    def setColor(self, color):
        self.color = color


    
    