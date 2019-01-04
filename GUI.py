import pygame as pg
import sys
from Board import Board
from Player import Player
from AI import AI

xlist = [73,133,193,253,313,373,433]
ylist = [70,128,186,242,302,360,418,476,534,592]

class Game:
    row = len(xlist)
    col = len(ylist)
    count = 0
    def __init__(self):
        return
    def judge(self, board):
        winner = ""
        for i in range(row):
            for j in range(col):
                if winner != "" and winner!= board.table[i][j].color and board.table[i][j].color!="w":
                    return ""
                if winner == "" and board.table[i][j].color != "w":
                    winner = board.table[i][j].color
        return winner


class GUI:
    def __init__(self):
        pg.init()
        # setup window
        width, height = 560, 710                      
        self.screen = pg.display.set_mode((width, height)) 
        pg.display.set_caption("Sean's game")        
        # setup image
        self.image = pg.image.load("./start.png")
        self.image = pg.transform.scale(self.image, (560, 710 ))
        self.image.convert()
        # display
        self.screen.blit(self.image, (0,0))
        pg.display.update()
        # init game
        self.initGame()

    def initGame(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            if self.firstbutton(135,472,280,42,"play") == True:       
                break	
            pg.display.update()
        self.beginGame()
    
    def beginGame(self):
        # initialize game GUI
        image = self.image
        screen = self.screen
        image = pg.image.load("./background.png")
        image = pg.transform.scale(image, (560, 710))
        image.convert()
        screen.blit(image, (0,0))
        pg.display.update()


        # initialize chess board
        board = Board(Game.row, Game.col)
        self.drawboard(50,50,board.table)

        # initialize players
        p1 = Player("P")
        players = [p1, AI("C", p1, 0, 0)]
        playerIndex = 0

        print(players[playerIndex].color+"'s turn")

            
        
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False	
                
                if event.type == pg.MOUSEBUTTONUP:
                    mouse = pg.mouse.get_pos()
                    move = GUI.getMousePos(mouse[0],mouse[1],50,50)
                    players[playerIndex].makeMove(board, move[0], move[1])
                    playerIndex = (playerIndex+1)%len(players)
                    self.drawboard(50,50,board.table)
                    print(move)

    def firstbutton(self,x,y,width,height,action = None):
        screen = self.screen
        image = self.image
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        if x + width > mouse[0] > x and y + height > mouse[1] > y:
            pg.draw.rect(screen, (255,255,255),((x,y),(width,height)), 2)
            if click[0] == 1 and action == "play":	
                return True
        else:
            screen.blit(image, (0,0))
        smallText = pg.font.Font("freesansbold.ttf",22)
        return False

    def drawboard(self,width,height,ary):
        for i in range(len(xlist)):
            for j in range(len(ylist)):
                if ary[i][j].color=="w":
                    pg.draw.rect(self.screen, (255,255,255),((xlist[i],ylist[j]),(width,height)), 2)
                else:
                    picture = pg.image.load("./test.png")
                    picture = pg.transform.scale(picture, (50, 50))
                    rect = picture.get_rect()
                    rect = rect.move((xlist[i],ylist[j]))
                    self.screen.blit(picture, rect)
        pg.display.update()

    @staticmethod
    #利用這個function去辨別以及抓取位置
    def getMousePos(x,y,width,height):
        xposition = -1  # -1代表沒有在任何方格之內
        yposition = -1
        for i in range(len(xlist)):
            if xlist[i] + width > x > xlist[i]:
                for j in range(len(ylist)):
                    if ylist[j] + height > y > ylist[j]:
                        xposition = i					
                        yposition = j
                        break
                break
        return [xposition, yposition]

    @staticmethod
    def quit(self):
        pg.quit() 
        sys.exit()

if __name__ == '__main__':
    t = GUI()
