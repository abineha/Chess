# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pygame as p
from Chess import Chessengine


wid=hei=512
dim=8
sq_size=hei//dim
max_fps=15
images={}


def loadimages():
    piece=['wp','wR','wN','wB','wK','wQ','bp','bN','bB','bK','bQ','bR']
    for i in piece:
        images[i] = p.transform.scale(p.image.load("Chess/images/"+i+".png"),(sq_size,sq_size))
    print(images)

def main():
    print('hello')
    p.init()
    screen=p.display.set_mode((wid,hei))
    clock=p.time.Clock()
    screen.fill(p.Color("white"))
    gs=Chessengine.GameState()
    validmoves=gs.getvalidmoves()
    movemade=False
    loadimages()
    running=True
    sqselected=() #row,col
    playerclicks=[] # (6,4) to (4,4) movement
    while running:
        for e in p.event.get():
            if e.type==p.QUIT:
                running= False
            elif e.type==p.MOUSEBUTTONDOWN:
                loc=p.mouse.get_pos() #(x,y) of mouse
                col= loc[0]//sq_size
                row=loc[1]//sq_size
                if sqselected==(row,col):
                    sqselected=()
                    playerclicks=[]
                else:
                    sqselected=(row,col)
                    playerclicks.append(sqselected)
                if len(playerclicks)==2:
                    move=Chessengine.move(playerclicks[0],playerclicks[1],gs.board)
                    for i in range(len(validmoves)):
                        if move==validmoves[i]:
                            gs.makemove(move)
                            movemade=True
                            sqselected=()
                            playerclicks=[]
                    if not movemade: #invalid move 2 click
                        playerclicks=[sqselected]
            #undo
            elif e.type==p.KEYDOWN:
                if e.key==p.K_z:
                    gs.undo()
                    movemade=True


        if movemade:
            validmoves=gs.getvalidmoves()
            movemade=False


        drawGameState(screen, gs)
        clock.tick(max_fps)
        p.display.flip()


def drawGameState(screen,gs):
    drawBoard(screen)
    drawPieces(screen,gs.board)


def drawBoard(screen):
    colors=[p.Color("white"),p.Color("gray")]
    for r in range(dim):
        for c in range(dim):
            color=colors[((r+c)%2)]
            p.draw.rect(screen,color,p.Rect(c*sq_size,r*sq_size,sq_size,sq_size))


def drawPieces(screen,board):
    for r in range(dim):
        for c in range(dim):
            piece=board[r][c]
            if piece!="--":
                screen.blit(images[piece],p.Rect(c*sq_size,r*sq_size,sq_size,sq_size))


if __name__=="__main__":
    main()
