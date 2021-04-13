from cmu_112_graphics import *
import time
import math as m

def appStarted(app):
    app.gameOver = False
    app.currPlayer = True
    app.board = [[[[None]*3]*3]*3]
    app.menuScreen = True
    app.gameScreen = False
    app.gridDrawn = False
    app.cubeChangeCurr = -1
    app.cubeChangeOld = -1
    pass

def keyPressed(app, event):
    if event.key == 'p':
        if app.cubeChangeCurr == 0:
            app.cubeChangeCurr = app.cubeChangeOld
        else:
            app.cubeChangeOld = app.cubeChangeCurr
            app.cubeChangeCurr = 0
    pass

def mousePressed(app, event):
    pass

def mouseDragged(app, event):
    print(event.x, event.y)
    pass

def mouseReleased(app, event):
    print()
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

def redrawAll(app, canvas):
    for i in range(3):
        drawSingleGrid(app, canvas, i)
    pass

runApp(width=1000,height=700)