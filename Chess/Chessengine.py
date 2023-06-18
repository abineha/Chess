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

        self.movefnct={'p':self.getpawnmoves,'R':self.getrookmoves,'N':self.getknightmoves,'Q':self.getqueenmoves,'B':self.getbishopmoves,'K':self.getkingmoves}
        self.whitemove= True
        self.movelog=[]
        # track king position
        self.wking=(7,4)
        self.bking = (0, 4)
        self.checkmate=False
        self.stalemate=False
        self.pins=[]
        self.checks=[]
        self.incheck=False


    def makemove(self,move):
        self.board[move.startrow][move.startcol] = '--'
        self.board[move.endrow][move.endcol] = move.piecemoved
        self.movelog.append(move)
        self.whitemove = not(self.whitemove)
        # track king position
        if move.piecemoved=="wk":
            self.wking=(move.endrow,move.endcol)
        elif move.piecemoved=="bk":
            self.bking = (move.endrow, move.endcol)

        if move.pawnpromotion:
            self.board[move.endrow][move.endcol] = move.piecemoved[0] + "Q"


    def undo(self):
        if len(self.movelog):
            move=self.movelog.pop()
            self.board[move.startrow][move.startcol]=move.piecemoved
            self.board[move.endrow][move.endcol]=move.piececaptured
            self.whitemove=not(self.whitemove)
            #track king position
            if move.piecemoved=="wk":
                self.wking=(move.startrow,move.startcol)
            elif move.piecemoved=="bk":
                self.bking = (move.startrow, move.startcol)

        self.checkmate = False
        self.stalemate = False

    def getvalidmoves(self):
        moves=[]
        self.incheck,self.pins,self.checks=self.checkforpinsandchecks()
        if self.whitemove:
            kingrow=self.wking[0]
            kingcol=self.wking[1]
        else:
            kingrow = self.bking[0]
            kingcol = self.bking[1]
        if self.incheck:
            if len(self.checks)==1:  # 1 check => block or move
                moves=self.getallpossiblemoves()
                #to block a check move a piece in btw
                check=self.checks[0]
                checkrow=check[0]
                checkcol=check[1]
                piecechecking=self.board[checkrow][checkcol]
                validsqs=[]
                if piecechecking[1]=='N':
                    validsqs=[(checkrow,checkcol)]
                else:
                    for i in range(1,8):
                        validsq=(kingrow+check[2]*i,kingcol+check[3]*i) #both checl[2][3] are check dirs
                        validsqs.append(validsq)
                        if validsq[0]==checkrow and validsq[1]==checkcol:
                            break

                for i in range(len(moves)-1,-1,-1):
                    if moves[i].piecemoved[1]!='K':
                        if not (moves[i].endrow,moves[i].endcol) in validsqs:
                            moves.remove(moves[i])
            else:  #double check king has to move
                self.getkingmoves(kingrow,kingcol,moves)
        else:
            moves=self.getallpossiblemoves()

        if len(moves) == 0:
            if self.inCheck():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False

        return moves

    def inCheck(self):
        if self.whitemove:
            return self.squnderattk(self.wking[0], self.wking[1])
        else:
            return self.squnderattk(self.bking[0], self.bking[1])



    def checkforpinsandchecks(self):
        pins=[]
        checks=[]
        incheck=False
        if self.whitemove:
            enemycolor="b"
            allycolor="w"
            startrow=self.wking[0]
            startcol=self.wking[1]
        else:
            enemycolor = "w"
            allycolor = "b"
            startrow = self.bking[0]
            startcol = self.bking[1]
        dir=((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(dir)):
            d=dir[j]
            possiblepin=()
            for i in range(1,8):
                endrow=startrow+d[0]*i
                endcol = startcol + d[1] * i
                if 0<=endrow<8 and 0<=endcol<8:
                    endpiece=self.board[endrow][endcol]
                    if endpiece[0]==allycolor and endpiece[1]!='K':
                        if possiblepin==():
                            possiblepin=(endrow,endcol,d[0],d[1])
                        else: # 2 ally piece so no check
                            break
                    elif endpiece[0]==enemycolor:
                        type=endpiece[1]
                        # 5 possibilities
                        #1: orthogonally away from king and piece is a rook
                        #2: diagonally from king and is bishop
                        #3: diagonally 1 sq from king and is pawn
                        #4: any dir from king and is qween
                        #5: any direction 1 sq away and piece is king (prevent a king to move to a sq controlled by another king
                        if (0<=j<=3 and type=='R') or (4<=j<=7 and type=='B') or (i==1 and type=='p' and ((enemycolor=='w' and 6<=j<=7) or (enemycolor=='b' and 4<=j<=5))) or(type=='Q') or (i==1 and type=='K'):
                            if possiblepin==():
                                incheck=True
                                checks.append((endrow,endcol,d[0],d[1]))
                                break
                            else:
                                pins.append(possiblepin)
                                break
                        else:
                            break
                else:
                    break

        knightmoves=((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))
        for m in knightmoves:
            endrow=startrow+m[0]
            endcol=startcol+m[1]
            if 0<=endrow<8 and 0<=endcol<8:
                endpiece=self.board[endrow][endcol]
                if endpiece[0]==enemycolor and endpiece[1]=='N':
                    incheck=True
                    checks.append((endrow,endcol,m[0],m[1]))
        return incheck,pins,checks



    def squnderattk(self,r,c):
        self.whitemove=not(self.whitemove)  #opp turn
        oppmoves= self.getallpossiblemoves()
        self.whitemove = not (self.whitemove)  # opp turn
        for move in oppmoves:
            if move.endrow==r and move.endcol==c:   #sq under attk
                return True
        return False


    def getallpossiblemoves(self):
        moves=[]
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn=self.board[r][c][0]
                if (turn=='w' and self.whitemove) or (turn=='b' and not(self.whitemove)):
                    piece=self.board[r][c][1]
                    self.movefnct[piece](r,c,moves)

        return moves

    def getpawnmoves(self,r,c,moves):
        piecepinned=False
        pindir=()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0]==r and self.pins[i][1]==c:
                piecepinned=True
                pindir=(self.pins[i][2],self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.whitemove:
            move_amount = -1
            start_row = 6
            enemy_color = "b"
            king_row, king_col = self.wking
        else:
            move_amount = 1
            start_row = 1
            enemy_color = "w"
            king_row, king_col = self.bking

        if self.board[r+move_amount][c] == "--":  # 1 square pawn advance
            if not piecepinned or pindir == (move_amount, 0):
                moves.append(move((r, c), (r + move_amount, c), self.board))
                if r == start_row and self.board[r + 2 * move_amount][c] == "--":  # 2 square pawn advance
                    moves.append(move((r, c), (r + 2 * move_amount, c), self.board))
        if c - 1 >= 0:  # capture to the left
            if not piecepinned or pindir == (move_amount, -1):
                if self.board[r + move_amount][c - 1][0] == enemy_color:
                    moves.append(move((r, c), (r + move_amount, c - 1), self.board))

        if c + 1 <= 7:  # capture to the right
            if not piecepinned or pindir == (move_amount, +1):
                if self.board[r + move_amount][c + 1][0] == enemy_color:
                    moves.append(move((r, c), (r + move_amount, c + 1), self.board))



    def getrookmoves(self,r,c,moves):
        piecepinned=False
        pindir=()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0]==r and self.pins[i][1]==c:
                piecepinned=True
                pindir=(self.pins[i][2],self.pins[i][3])
                if self.board[r][c][1]!='Q': #cant remove queen from pin on rook moves only remove it on bishop moves
                    self.pins.remove(self.pins[i])
                break


        dir=((-1,0),(0,-1),(0,1),(1,0))
        if self.whitemove:
            enemycolor='b'
        else:
            enemycolor='w'

        for d in dir:
            for i in range(1,8): # + breaks this loop
                endrow=r+d[0]*i
                endcol=c+d[1]*i
                if (0<=endrow<8 and 0<=endcol<8):
                    if not piecepinned or pindir==d or pindir==(-d[0],-d[1]):
                        endpiece=self.board[endrow][endcol]
                        if endpiece=="--": #empty sq
                            moves.append(move((r,c),(endrow,endcol),self.board))
                        elif endpiece[0]==enemycolor:
                            moves.append(move((r, c), (endrow, endcol), self.board))
                            break
                        else:  #same color piece
                            break
                else:   #off board
                    break




    def getknightmoves(self,r,c,moves):
        piecepinned=False
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0]==r and self.pins[i][1]==c:
                piecepinned=True
                self.pins.remove(self.pins[i])
                break

        dir = ((-2, -1),(-2, 1), (-1, -2), (-1, 2), (1, -2),(1,2),(2,-1),(2,1))
        if self.whitemove:
            allycolor = 'w'
        else:
            allycolor = 'b'

        for d in dir:
            endrow = r + d[0]
            endcol = c + d[1]
            if 0<=endrow<8 and 0<=endcol<8:
                if not piecepinned:
                    endpiece=self.board[endrow][endcol]
                    if endpiece[0]!=allycolor: #empty or enemy
                        moves.append(move((r,c),(endrow,endcol),self.board))


    def getbishopmoves(self,r,c,moves):
        piecepinned=False
        pindir=()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0]==r and self.pins[i][1]==c:
                piecepinned=True
                pindir=(self.pins[i][2],self.pins[i][3])
                self.pins.remove((self.pins[i]))
                break
        dir = ((-1, 1), (1, -1), (1, 1), (-1, -1))
        if self.whitemove:
            enemycolor = 'b'
        else:
            enemycolor = 'w'

        for d in dir:
            for i in range(1, 8):  # + breaks this loop
                endrow = r + d[0] * i
                endcol = c + d[1] * i
                if (0 <= endrow < 8 and 0 <= endcol < 8):
                    if not piecepinned or pindir==d or pindir==(-d[0],-d[1]):
                        endpiece = self.board[endrow][endcol]
                        if endpiece == "--":  # empty sq
                            moves.append(move((r, c), (endrow, endcol), self.board))
                        elif endpiece[0] == enemycolor:
                            moves.append(move((r, c), (endrow, endcol), self.board))
                            break
                        else:  # same color piece
                            break
                else:  # off board
                    break


    def getqueenmoves(self,r,c,moves):
        self.getrookmoves(r,c,moves)
        self.getbishopmoves(r, c, moves)


    def getkingmoves(self,r,c,moves):
        dir=((-1,-1),(-1,0),(-1,1),(1,1),(1,-1),(1,0),(0,1),(0,-1))
        if self.whitemove:
            allycolor = 'w'
        else:
            allycolor = 'b'
        for i in range(8):
            endrow=r+dir[i][0]
            endcol=c+dir[i][1]
            if 0<=endrow<8 and 0<=endcol<8:
                endpiece=self.board[endrow][endcol]
                if endpiece[0]!=allycolor: #eempty or enemy
                    if allycolor=='w':
                        self.wking=(endrow,endcol)
                    else:
                        self.bking=(endrow,endcol)
                    incheck,pins,checks = self.checkforpinsandchecks()
                    if not incheck:
                        moves.append(move((r,c),(endrow,endcol),self.board))
                    if allycolor=='w':
                        self.wking=(r,c)
                    else:
                        self.bking=(r,c)


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
        self.moveid =(self.startrow*1000)+(self.startcol*100)+(self.endrow*10)+(self.endcol) #hash function 0-7777
        self.pawnpromotion=False
        if (self.piecemoved=='wp' and self.endrow==0) or (self.piecemoved=='bp' and self.endrow==7):
            print('tru')
            self.pawnpromotion = True



    def __eq__(self,other):
        if isinstance(other,move):
            return self.moveid==other.moveid

    def getchessnotation(self):
        return self.getrankfile(self.startrow,self.startcol)+self.getrankfile(self.endrow,self.endcol)

    def getrankfile(self,r,c):
        return self.colstofiles[c]+self.rowstorank[r]
