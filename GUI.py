import pygame as pg
import time
import sys
from Board import Board
from Player import Player
from AI import AI

xlist = [73,133,193,253,313,373,433]
ylist = [70,128,186,242,302,360,418,476,534,592]
clock = pg.time.Clock()

class Game:
    row = len(xlist)
    col = len(ylist)
    difficulty = 3
    count = 0
    def __init__(self):
        return
    def judge(board):
        winner = ""
        for i in range(Game.row):
            for j in range(Game.col):
                if winner != "" and winner!= board.table[i][j].color and board.table[i][j].color!="w":
                    return ""
                if winner == "" and board.table[i][j].color != "w":
                    winner = board.table[i][j].color
        return winner
    def setupDif(difficulty):
        # setup difficulty
        beginHard = 0
        nextHard = 50
        if difficulty==0:
            beginHard = 0
            nextHard = 50
        elif difficulty==1:
            beginHard = 1
            nextHard = 20
        elif difficulty==2:
            beginHard = 2
            nextHard = 20
        elif difficulty==3:
            beginHard = 3
            nextHard = 30
        elif difficulty==4:
            beginHard = 4
            nextHard = 40
        elif difficulty==5:
            beginHard = 5
            nextHard = 50
        return [beginHard, nextHard]


class GUI:
    def __init__(self):
        pg.init()
        # setup window
        width, height = 560, 710                      
        self.screen = pg.display.set_mode((width, height)) 
        pg.display.set_caption("CHAIN REACTION GAME")        
        # setup image
        self.image = pg.image.load("./images/start.png")
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
        image = pg.image.load("./images/background.png")
        image = pg.transform.scale(image, (560, 710))
        image.convert()
        screen.blit(image, (0,0))
        pg.display.update()


        # initialize chess board
        board = Board(Game.row, Game.col)
        GUI.drawboard(self.screen,50,50,board.table)

        # initialize players
        p1 = Player("P")
        dif = Game.setupDif(Game.difficulty)
        players = [p1, AI("C", p1, dif[0], dif[1])]
        playerIndex = 0
        print(players[playerIndex].color+"'s turn")
        GUI.setText(screen,players[0].color+"'s turn")

        # run game
        running = True
        begin = False
        while running:
            skip = False
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False	
                
                if event.type == pg.MOUSEBUTTONUP and Game.count%2==0:
                    if not begin:
                        begin = True
                        continue
                    try:
                        mouse = pg.mouse.get_pos()
                        move = GUI.getMousePos(mouse[0],mouse[1],50,50)
                        try:
                            # player makes move
                            players[0].makeMove(board, move[0], move[1])
                            board.printBoard()
                            GUI.drawboard(self.screen, 50,50,board.table)
                            # count the round and judge the game
                            Game.count = Game.count+1
                            j = Game.judge(board)
                            if j!="" and Game.count>1:
                                if j=="P":
                                    self.final(True)
                                else:
                                    self.final(False)
                                print(j+" wins!")
                                break
                            GUI.setText(screen,players[1].color+"'s turn")
                            skip = True
                            print(players[1].color+"'s turn")

                        except RecursionError as error:
                            self.final(True)
                            print(players[0].color+" wins!")
                            break
                    except ValueError as error:
                        Game.count = Game.count-1
                        print(repr(error))

            if Game.count%2==1 and not skip:        
                try:
                    try:
                        # AI make move
                        players[1].think(board, Game.count)
                        board.printBoard()
                        GUI.drawboard(self.screen, 50,50,board.table)
                        # count the round and judge the game
                        Game.count = Game.count+1
                        j = Game.judge(board)
                        if j!="" and Game.count>1:
                            if j=="P":
                                self.final(True)
                            else:
                                self.final(False)
                            print(j+" wins!")
                            break
                        print(players[0].color+"'s turn")
                        GUI.setText(screen,players[0].color+"'s turn")
                    
                    except RecursionError as error:
                        self.final(False)
                        print(players[1].color+" wins!")
                        break
                except ValueError as error:
                    Game.count = Game.count-1
                    print(repr(error))

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

    @staticmethod
    def drawboard(screen,width,height,ary):
        for i in range(len(xlist)):
            for j in range(len(ylist)):
                head = pg.Rect((xlist[i],ylist[j]),(width,height))
                screen.fill((255,255,255), head)
                picture = pg.image.load("./images/blank.jpg")
                if ary[i][j].color=="P":
                    if ary[i][j].point==ary[i][j].margin-3:
                        picture = pg.image.load("./images/P_1.png")
                    elif ary[i][j].point==ary[i][j].margin-2:
                        picture = pg.image.load("./images/P_2.png")
                    elif ary[i][j].point==ary[i][j].margin-1:
                        picture = pg.image.load("./images/P_3.png")
                elif ary[i][j].color=="C":
                    if ary[i][j].point==ary[i][j].margin-3:
                        picture = pg.image.load("./images/C_1.png")
                    elif ary[i][j].point==ary[i][j].margin-2:
                        picture = pg.image.load("./images/C_2.png")
                    elif ary[i][j].point==ary[i][j].margin-1:
                        picture = pg.image.load("./images/C_3.png")
                if ary[i][j].color!="w":
                    picture = pg.transform.scale(picture, (50, 50))
                    rect = picture.get_rect()
                    rect = rect.move((xlist[i],ylist[j]))
                    screen.blit(picture, rect)
        pg.display.update()

    @staticmethod
    def setText(screen,text):
        top = 5
        left = 180
        head = pg.Rect((left,top),(200,40))
        screen.fill((255,255,0), head)
        pg.font.init()
        font = pg.font.SysFont('Comic Sans MS', 50)
        textsurface = font.render(text, False, (0, 0, 0))
        screen.blit(textsurface,(left+30,top))
        pg.display.update()

    def final(self, isWin):
        # initialize game GUI
        picture = pg.image.load("./images/VICTORY.png")
        if isWin:
            picture = pg.image.load("./images/VICTORY.png")
        else:
            picture = pg.image.load("./images/FAIL.png")
        picture = pg.transform.scale(picture, (400, 200))
        rect = picture.get_rect()
        rect = rect.move((100,300))
        self.screen.blit(picture, rect)
        pg.display.update()

    @staticmethod
    # get mouse position
    def getMousePos(x,y,width,height):
        xposition = -1
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

    def quit(self):
        pg.quit() 
        sys.exit()

if __name__ == '__main__':
    t = GUI()
