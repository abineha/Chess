# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pygame as p
from Chess import Chessengine,ai,simultaion
import sys
from multiprocessing import Process, Queue

wid=hei=512
dim=8
sq_size=hei//dim
max_fps=15
images={}


def loadimages():
    piece=['wp','wR','wN','wB','wK','wQ','bp','bN','bB','bK','bQ','bR']
    for i in piece:
        images[i] = p.transform.scale(p.image.load("Chess/images/"+i+".png"),(sq_size,sq_size))

def main():
    print('hello')
    p.init()
    screen=p.display.set_mode((wid,hei))
    clock=p.time.Clock()
    screen.fill(p.Color("white"))
    gs=Chessengine.GameState()
    sim=simultaion.gamestate()
    validmoves=gs.getvalidmoves()
    movemade=False
    loadimages()
    running=True
    sqselected=() #row,col
    playerclicks=[] # (6,4) to (4,4) movement
    game_over = False
    ai_thinking = False
    move_undone = False
    move_finder_process = None
    player_one = True  # human is playing whiteTrue
    player_two = False  # playing white  True
    print("MENU:")
    print("1. Chess opening simulations")
    print("2. Chess player vs ai")
    print("3. Chess graphs")
    choice=int(input("Enter choice:"))
    ans = True
    if choice==2:
        while running:
            human_turn = (gs.whitemove and player_one) or (not gs.whitemove and player_two)
            for e in p.event.get():
                if e.type==p.QUIT:
                    running= False
                    p.quit()
                    sys.exit()
                elif e.type==p.MOUSEBUTTONDOWN:
                    if not game_over:
                        loc=p.mouse.get_pos() #(x,y) of mouse
                        col= loc[0]//sq_size
                        row=loc[1]//sq_size
                        if sqselected==(row,col) or col>=8:
                            sqselected=()
                            playerclicks=[]
                        else:
                            sqselected=(row,col)
                            playerclicks.append(sqselected)

                        if len(playerclicks)==2 and human_turn:
                            move=Chessengine.move(playerclicks[0],playerclicks[1],gs.board)
                            print(move.getchessnotation())
                            for i in range(len(validmoves)):
                                if move==validmoves[i]:
                                    gs.makemove(validmoves[i])
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
                        game_over = False
                        if ai_thinking:
                            move_finder_process.terminate()
                            ai_thinking = False
                        move_undone = True

                    if e.key == p.K_r:  # reset the game when 'r' is pressed
                        gs = Chessengine.GameState()
                        validmoves= gs.getvalidmoves()
                        sqselected= ()
                        playerclicks = []
                        movemade= False
                        game_over = False
                        if ai_thinking:
                            move_finder_process.terminate()
                            ai_thinking = False
                        move_undone = True

            # AI
            if not game_over and not human_turn and not move_undone:
                if not ai_thinking:
                    ai_thinking = True
                    return_queue = Queue()  # used to pass data between threads
                    move_finder_process = Process(target=ai.findBestMove,args=(gs,validmoves, return_queue))
                    move_finder_process.start()

                if not move_finder_process.is_alive():
                    ai_move = return_queue.get()
                    if ai_move is None:
                        ai_move = ai.findRandomMove(validmoves)
                    gs.makemove(ai_move)
                    movemade = True
                    ai_thinking = False
            if movemade:
                validmoves=gs.getvalidmoves()
                movemade=False
                move_undone = False



            if gs.checkmate:
                game_over = True
                if gs.whitemove:
                    print( "Black wins by checkmate")
                else:
                    print("White wins by checkmate")

            elif gs.stalemate:
                game_over = True
                print("Stalemate")

            drawGameState(screen, gs)
            clock.tick(max_fps)
            p.display.flip()

    elif choice==1:
        while ans:
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
                    p.quit()
                    sys.exit()
                sim.pri()
                ch=input("enter opening:")
                sim.choice(ch,p,screen)
                a = input("continue? y/n")
                ans = True if a == 'y' else False
                p.time.wait(5000)
                del sim
                sim = simultaion.gamestate()
                print(sim.board)
                drawGameState(screen, sim)
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
