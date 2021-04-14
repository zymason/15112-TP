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
    pass

def keyPressed(app, event):
    pass

def playPiece(app, pos):
    if app.board[pos[0]][pos[1]][pos[2]] == None:
        app.board[pos[0]][pos[1]][pos[2]] = app.currPlayer
        app.currPlayer = not app.currPlayer


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
    pass

def mouseDragged(app, event):
    pass

def mouseReleased(app, event):
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
                if app.board[grid][row][col] != None:
                    x = app.xCtr + ((col-1) * dPos)
                    y = app.yCtr[grid] + ((row-1) * dPos)
                    canvas.create_text(x,y,text=str(app.board[grid][row][col]),
                            font='Arial 10 bold')


def redrawAll(app, canvas):
    for i in range(3):
        drawSingleGrid(app, canvas, i)


    drawPieces(app, canvas)
    canvas.create_text(app.width/3, app.height/2, text=app.message,
            font='Arial 15 bold')
    pass

runApp(width=1000,height=700)