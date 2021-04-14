from cmu_112_graphics import *
import time
import math as m

def appStarted(app):
    # Consider a dictionary for board
    col = [None, None, None]
    row1 = [col[:], col[:], col[:]]
    row2 = [col[:], col[:], col[:]]
    row3 = [col[:], col[:], col[:]]
    app.board = [row1[:], row2[:], row3[:]]
    app.message = "null"
    app.xCtr = 3*app.width // 4
    app.offA = app.height // 10
    app.yCtr = [int((app.height * (1+(2*i))/6)) for i in range(3)]
    app.currPlayer = True   # True is P1, False is P2(AI)
    app.winCoords = [None, None]
    app.gameOver = False
    app.winner = None
    pass

def playPiece(app, pos):
    if app.board[pos[0]][pos[1]][pos[2]] == None:
        app.board[pos[0]][pos[1]][pos[2]] = app.currPlayer
        app.currPlayer = not app.currPlayer
    pass

# Need to check all opposites, not just pure opposite
def checkWin(app):
    oppPos = [0,0,0]
    midPos = [0,0,0]
    winPoint = {(0,0,0), (0,0,1), (0,1,0), (0,1,1), (0,2,0),
                (1,0,0), (1,0,1), (1,1,0), (1,2,0),
                (2,2,2), (2,0,2), (2,1,2), (2,2,1)}
    for pos in winPoint:
        for i in range(len(pos)):
            oppPos[i] = pos[i] + 2*(1 - pos[i])

        player = app.board[pos[0]][pos[1]][pos[2]]

        if (player == app.board[oppPos[0]][oppPos[1]][oppPos[2]] and 
            player != None):
            for i in range(len(midPos)):
                midPos[i] = int((pos[i] + oppPos[i]) / 2)
            if app.board[midPos[0]][midPos[1]][midPos[2]] == player:
                app.gameOver = True
                app.winner = player
                app.message = f"{str(player)} won!!"
    pass

def mousePressed(app, event):
    if (app.xCtr - app.offA) <= event.x < (app.xCtr + app.offA):
        gridNum = int(event.y // (app.height/3))
        if (app.yCtr[gridNum] - app.offA <= event.y < 
            app.yCtr[gridNum] + app.offA):
            gridXRef = app.xCtr - app.offA
            gridYRef = app.yCtr[gridNum] - app.offA
            gridRow = int((event.y - gridYRef) // (app.offA*2/3))
            gridCol = int((event.x - gridXRef) // (app.offA*2/3))
            app.message = f"{gridNum} | {gridRow}, {gridCol}"
            pos = (gridNum, gridRow, gridCol)
            playPiece(app, pos)
            checkWin(app)
    pass

def keyPressed(app, event):
    appStarted(app)
    pass

def timerFired(app):
    pass

def drawSingleGrid(app, canvas, i):
    xCtr = app.width * 3/4
    yCtr = (app.height * (1+(2*i))/6)
    offA = app.height / 10
    offB = offA / 3

    L1x = xCtr - offB
    L2x = xCtr + offB
    LVyU = yCtr - offA
    LVyD = yCtr + offA

    LHxL = xCtr - offA
    LHxR = xCtr + offA
    L3y = yCtr - offB
    L4y = yCtr + offB
    
    width = 2
    canvas.create_line(L1x,LVyU,L1x,LVyD,width=width)
    canvas.create_line(L2x,LVyU,L2x,LVyD,width=width)
    canvas.create_line(LHxL,L3y,LHxR,L3y,width=width)
    canvas.create_line(LHxL,L4y,LHxR,L4y,width=width)
    
    text = ['Top Slice', 'Middle Slice', 'Lower Slice']
    canvas.create_text(app.width * 29/32,yCtr,text=text[i],font='Arial 15 bold')
    pass

def drawPieces(app, canvas):
    dPos = app.offA * 2/3
    for grid in range(len(app.board)):
        for row in range(len(app.board[0])):
            for col in range(len(app.board[0][0])):
                player = app.board[grid][row][col]
                if player != None:
                    x = app.xCtr + ((col-1) * dPos)
                    y = app.yCtr[grid] + ((row-1) * dPos)
                    if player:
                        text = 'O'
                        fill = '#00f'
                    elif not player:
                        text = 'X'
                        fill = '#f00'
                    canvas.create_text(x,y,text=text,fill=fill,
                            font='Arial 20 bold')
    pass

def drawCurrPlayer(app, canvas):
    r = 50
    xCtr = app.width/3
    yCtr = app.height/10 + 100
    if app.currPlayer:
        text = "Player 1: Your Turn"
        fill = "#00f"
        canvas.create_text(xCtr,yCtr,text="O",fill=fill,font="Arial 40 bold")
    else:
        text = "Player 2: Your Turn"
        fill = "#f00"
        canvas.create_text(xCtr,yCtr,text="X",fill=fill,font="Arial 40 bold")
    canvas.create_text(xCtr,app.height/10,text=text,font="Arial 30 bold",
            fill=fill)
    pass
    

def redrawAll(app, canvas):
    for i in range(3):
        drawSingleGrid(app, canvas, i)
    drawPieces(app, canvas)
    drawCurrPlayer(app, canvas)
    canvas.create_text(app.width/3, app.height*7/12, text=app.message,
            font='Arial 15 bold')
    pass

runApp(width=1000,height=700)