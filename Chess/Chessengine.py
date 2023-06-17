class GameState():
    def __init__(self):
        self.board= [ ["bR","bN","bB","bQ","bK","bB","bN","bR"],
                      ["bp","bp","bp","bp","bp","bp","bp","bp",],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                      ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.whitemove= True
        self.movelog=[]

    def makemove(self,move):
        if self.board[move.startrow][move.startcol] != '--':
            self.board[move.startrow][move.startcol] = '--'
            self.board[move.endrow][move.endcol] = move.piecemoved
            self.movelog.append(move)
            self.whitemove = not(self.whitemove)

    def undo(self):
        if len(self.movelog):
            move=self.movelog.pop()
            self.board[move.startrow][move.startcol]=move.piecemoved
            self.board[move.endrow][move.endcol]=move.piececaptured
            self.whitemove=not(self.whitemove)

    def getvalidmoves(self):
        return self.getallpossiblemoves()

    def getallpossiblemoves(self):
        pass

class move():

    ranktorows={'1': 7,'2': 6,'3': 5,'4': 4, '5':3,'6': 2,'7': 1,'8':0}
    rowstorank={v: k for k,v in ranktorows.items()}
    filetocols={'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
    colstofiles={v:k for k,v in filetocols.items()}
    def __init__(self,startsq,endsq,board):
        self.startrow=startsq[0]
        self.startcol = startsq[1]
        self.endrow = endsq[0]
        self.endcol = endsq[1]
        self.piecemoved=board[self.startrow][self.startcol]
        self.piececaptured=board[self.endrow][self.endcol]

    def getchessnotation(self):
        return self.getrankfile(self.startrow,self.startcol)+self.getrankfile(self.endrow,self.endcol)

    def getrankfile(self,r,c):
        return self.colstofiles[c]+self.rowstorank[r]
