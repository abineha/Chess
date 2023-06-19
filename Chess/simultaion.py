import pygame as p
from Chess import main,Chessengine
from Chess.main import drawGameState
import sys

wid=hei=512
dim=8
sq_size=hei//dim
max_fps=15
images={}


def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(dim):
        for c in range(dim):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * sq_size, r * sq_size, sq_size, sq_size))


def drawPieces(screen, board):
    for r in range(dim):
        for c in range(dim):
            piece = board[r][c]
            if piece != "--":
                screen.blit(images[piece], p.Rect(c * sq_size, r * sq_size, sq_size, sq_size))

def loadimages():
    piece = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bN', 'bB', 'bK', 'bQ', 'bR']
    for i in piece:
        images[i] = p.transform.scale(p.image.load("Chess/images/" + i + ".png"), (sq_size, sq_size))


class gamestate():
    def __init__(self):
        self.board= [ ["bR","bN","bB","bQ","bK","bB","bN","bR"],
                      ["bp","bp","bp","bp","bp","bp","bp","bp",],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                      ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.map={"The Italian Game":0,"The Sicilian Defense":1,"The French Defense":2,"The Ruy-Lopez":3,"The Slav Defense":4}
        n1=SLinkedList()
        n2 = SLinkedList()
        n3 = SLinkedList()
        n4 = SLinkedList()
        n5 = SLinkedList()
        n1.headval=Node("6444")
        n1.AtEnd("1434")
        n1.AtEnd("7655")
        n1.AtEnd("0122")
        n1.AtEnd("7542")
        n2.headval = Node("6444")
        n2.AtEnd("1232")
        n3.headval=Node("6444")
        n3.AtEnd("1424")
        n3.AtEnd("6343")
        n3.AtEnd("1333")
        n4.headval = Node("6444")
        n4.AtEnd("1434")
        n4.AtEnd("7655")
        n4.AtEnd("0122")
        n4.AtEnd("7531")
        n5.headval = Node("6343")
        n5.AtEnd("1333")
        n5.AtEnd("6242")
        n5.AtEnd("1222")

        self.map["The Italian Game"]=n1
        self.map["The Sicilian Defense"] = n2
        self.map["The French Defense"] = n3
        self.map["The Ruy-Lopez"] = n4
        self.map["The Slav Defense"] = n5

        loadimages()
    def pri(self):
        print(self.map.keys())
        return

    def choice(self,ch,p,screen):
        p.time.wait(1000)
        if ch=="The Italian Game":
            self.map["The Italian Game"].listprint(self.board,p,screen)
        elif ch=="The Sicilian Defense":
            self.map["The Sicilian Defense"].listprint(self.board, p, screen)
        elif ch=="The French Defense":
            self.map["The French Defense"].listprint(self.board, p, screen)
        elif ch=="The Ruy-Lopez":
            self.map["The Ruy-Lopez"].listprint(self.board, p, screen)
        else:
            self.map["The Slav Defense"].listprint(self.board, p, screen)


class Node:
   def __init__(self, dataval=None):
      self.dataval = dataval
      self.nextval = None

class SLinkedList:
   def __init__(self):
      self.headval = None

   def listprint(self,board,p,screen):
      printval = self.headval
      while printval is not None:
        print (printval.dataval)
        pi=board[int(printval.dataval[0])][int(printval.dataval[1])]
        print(pi)
        board[int(printval.dataval[0])][int(printval.dataval[1])] = '--'
        board[int(printval.dataval[2])][int(printval.dataval[3])] = pi
        print(board)
        drawBoard(screen)
        drawPieces(screen, board)
        p.display.flip()
        p.time.wait(5000)
        printval = printval.nextval

   def AtEnd(self, newdata):
       NewNode = Node(newdata)
       if self.headval is None:
           self.headval = NewNode
           return
       laste = self.headval
       while (laste.nextval):
           laste = laste.nextval
       laste.nextval = NewNode




