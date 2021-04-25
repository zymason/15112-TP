from cmu_112_graphics import *
import time
import math as m
import copy

def appStarted(app):
    app.timerDelay = 30
    app.cos30 = m.cos(m.pi/6)
    col = [None, None, None]
    app.bigBoard = [col[:], col[:], col[:]]
    app.currBigPlayer = True   # True is P1, False is P2/AI
    app.mode = "start"
    app.bigXCtr = app.width * 3/4
    app.bigYCtr = app.height/2
    app.bigOffA = app.height/6
    app.bigOffB = app.bigOffA/6

def start_mousePressed(app, event):
    if event.y > app.width/7:
        if event.x < app.width/2:
            app.numPlayers = 1
        else:
            app.numPlayers = 2
        app.mode = "square"

def start_redrawAll(app, canvas):
    canvas.create_rectangle(0,app.height/7,app.width/2,app.height,
            width=0,fill='#a00')
    canvas.create_rectangle(app.width,app.height/7,app.width/2,app.height,
            width=0,fill='#00a')
    canvas.create_text(app.width/2,50,
            text="Welcome to Ultimate 3D Tic Tac Toe!",font='Arial 50 bold')
    canvas.create_text(app.width/4,app.width/3,text="Single Player",
            font='Arial 60 bold')
    canvas.create_text(app.width*3/4,app.width/3,text="Two Player",
            font='Arial 60 bold',fill='#fff')

class LargeBoard(object):
    def __init__(self, board, winner):
        self.board = board
        self.winner = winner

def miniMax2():
    pass

def checkWin2(app):
    pass

def square_mousePressed(app,event):
    if (app.bigXCtr - app.bigOffA <= event.x < app.bigXCtr + app.bigOffA and
        app.bigYCtr - app.bigOffA <= event.y < app.bigYCtr + app.bigOffA):
        row = int((-app.bigYCtr+event.y-app.bigOffB) // (app.bigOffA*2/3)) + 1
        col = int((-app.bigXCtr+event.x-app.bigOffB) // (app.bigOffA*2/3)) + 1
        if app.bigBoard[row][col] == None:
            print(row, col)
            app.currBigPos = [row, col]
            app.bigBoard[row][col] = True
            # initCube(app)
    pass

def square_keyPressed(app, event):
    if event.key == 'q':
        appStarted(app)
    pass

def drawLargeGrid(app, canvas):
    xCtr = app.bigXCtr
    yCtr = app.bigYCtr
    offA = app.bigOffA
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
    pass

def drawBigPieces(app, canvas):
    dPos = app.bigOffA * 2/3
    for row in range(len(app.bigBoard)):
        for col in range(len(app.bigBoard[0])):
            player = app.bigBoard[row][col]
            if player != None:
                x = app.bigXCtr + ((col-1) * dPos)
                y = app.bigYCtr + ((row-1) * dPos)
                if player:
                    text = 'O'
                    fill = '#00a'
                elif not player:
                    text = 'X'
                    fill = '#a00'
                canvas.create_text(x,y,text=text,fill=fill,
                        font='Arial 40 bold')
    pass

def square_redrawAll(app, canvas):
    drawLargeGrid(app, canvas)
    drawBigPieces(app, canvas)
    pass

def initCube(app):
    col = [None, None, None]
    row1 = [col[:], col[:], col[:]]
    row2 = [col[:], col[:], col[:]]
    row3 = [col[:], col[:], col[:]]
    app.board = [row1[:], row2[:], row3[:]]
    app.xCtrTri = 3*app.width // 4
    app.offATri = app.height // 10
    app.yCtrTri = [int((app.height * (1+(2*i))/6)) for i in range(3)]
    app.winCoords = [None, None]
    app.currPlayer = app.currBigPlayer
    app.winnerSmall = None
    app.rotateStarted = False
    app.dTheta = m.pi/360
    app.paused = False
    app.smallGameOver = False
    app.smallGOTime = False
    app.smallMsg = None
    app.cubeSide = 400
    app.timeInit = time.time()
    app.cubA = [app.cubeSide/2,app.cubeSide/6,app.cubeSide/6]
    app.cubB = [app.cubeSide/2,-app.cubeSide/6,app.cubeSide/6]
    app.cubZ = [app.cubeSide/6,app.cubeSide/6,app.cubeSide/2]
    app.cubeA = copy.copy(app.cubA)
    app.cubeB = copy.copy(app.cubB)
    app.cubeZ = copy.copy(app.cubZ)
    app.cubeCtr = [app.width/3,app.height * 7/12]
    app.theta = 0
    app.numMoves = 0
    app.winPos = []
    checkWin3(app)
    app.mode = "cube"

def playPiece(app, pos):
    if app.board[pos[0]][pos[1]][pos[2]] == None:
        app.board[pos[0]][pos[1]][pos[2]] = app.currPlayer
        app.currPlayer = not app.currPlayer
        app.numMoves += 1
    pass

def miniMax3(app):
    pass

def getOppPos(pos, index=0):
    pos = list(pos)
    output = []
    if index == len(pos):
        return []
    else:
        output += getOppPos(pos, index+1)
        if pos[index]%2 == 0:
            newPos = copy.copy(pos)
            newPos[index] = abs(2-pos[index])
            output += [newPos]
            output += getOppPos(newPos, index+1)
        return output

def checkWin3(app):
    midPos = [0,0,0]
    winPoint = {(0,0,0), (0,0,1), (0,1,0), (0,1,1), (0,2,0),
                (1,0,0), (1,0,1), (1,1,0), (1,2,0),
                (2,2,2), (2,0,2), (2,1,2), (2,2,1)}
    if app.numMoves == 27:
        app.winnerSmall = None
        app.smallGameOver = True
        return
    for pos in winPoint:
        player = app.board[pos[0]][pos[1]][pos[2]]
        if player != None:
            for oppPos in getOppPos(pos):
                if (player == app.board[oppPos[0]][oppPos[1]][oppPos[2]] and 
                    player != None):
                    for i in range(len(midPos)):
                        midPos[i] = int((pos[i] + oppPos[i]) / 2)
                    if app.board[midPos[0]][midPos[1]][midPos[2]] == player:
                        app.winnerSmall = player
                        app.currPlayer = None
                        app.winPos = [pos, midPos, oppPos]
                        app.smallGameOver = True
                        return
    pass

def cube_mousePressed(app, event):
    if not app.rotateStarted:
        return
    if (app.xCtrTri - app.offATri) <= event.x < (app.xCtrTri + app.offATri):
        gridNum = int(event.y // (app.height/3))
        if (app.yCtrTri[gridNum] - app.offATri <= event.y < 
            app.yCtrTri[gridNum] + app.offATri):
            gridXRef = app.xCtrTri - app.offATri
            gridYRef = app.yCtrTri[gridNum] - app.offATri
            gridRow = int((event.y - gridYRef) // (app.offATri*2/3))
            gridCol = int((event.x - gridXRef) // (app.offATri*2/3))
            pos = (gridNum, gridRow, gridCol)
            playPiece(app, pos)
            checkWin3(app)
    pass

def cube_keyPressed(app, event):
    if event.key == "r":
        initCube(app)
    elif event.key == "p":
        app.paused = not app.paused
    elif event.key == "Up":
        app.dTheta += m.pi/360
        if app.dTheta > m.pi/36:
            app.dTheta = m.pi/36
    elif event.key == "Down":
        app.dTheta -= m.pi/360
        if app.dTheta < -m.pi/36:
            app.dTheta = -m.pi/36
    elif event.key == 'q':
        appStarted(app)
    elif event.key == 'e' and app.smallGameOver:
        app.bigBoard[app.currBigPos[0]][app.currBigPos[1]] = app.winnerSmall
        app.mode = 'square'
    pass

def cube_timerFired(app):
    if time.time() - app.timeInit >= 2 and not app.rotateStarted:
        app.rotateStarted = True
    if app.rotateStarted:
        x1, x2 = app.cubA[0], app.cubB[0]
        y1, y2 = app.cubA[1], app.cubB[1]
        x3, y3 = app.cubZ[0], app.cubZ[1]
        app.cubeA[0] = x1*m.cos(app.theta) - y1*m.sin(app.theta)
        app.cubeA[1] = x1*m.sin(app.theta) + y1*m.cos(app.theta)
        app.cubeB[0] = x2*m.cos(app.theta) - y2*m.sin(app.theta)
        app.cubeB[1] = x2*m.sin(app.theta) + y2*m.cos(app.theta)
        app.cubeZ[0] = x3*m.cos(app.theta) - y3*m.sin(app.theta)
        app.cubeZ[1] = x3*m.sin(app.theta) + y3*m.cos(app.theta)
        app.theta += app.dTheta
        app.theta %= 2*m.pi
    pass

def drawSingleGrid(app, canvas, i):
    xCtr = app.width * 3/4
    yCtr = (app.height * (1+(2*i))/6)
    offA = app.height / 10
    offB = offA / 3

    L1x = app.xCtrTri - offB
    L2x = app.xCtrTri + offB
    LVyU = yCtr - offA
    LVyD = yCtr + offA

    LHxL = app.xCtrTri - offA
    LHxR = app.xCtrTri + offA
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
    dPos = app.offATri * 2/3
    for grid in range(len(app.board)):
        for row in range(len(app.board[0])):
            for col in range(len(app.board[0][0])):
                player = app.board[grid][row][col]
                if player != None:
                    x = app.xCtrTri + ((col-1) * dPos)
                    y = app.yCtrTri[grid] + ((row-1) * dPos)
                    if player:
                        text = 'O'
                        fill = '#00a'
                    elif not player:
                        text = 'X'
                        fill = '#a00'
                    canvas.create_text(x,y,text=text,fill=fill,
                            font='Arial 20 bold')
    if app.winnerSmall != None:
        for pos in app.winPos:
            x = app.xCtrTri + ((pos[2]-1) * dPos)
            y = app.yCtrTri[pos[0]] + ((pos[1]-1) * dPos)
            canvas.create_text(x,y,text='O',fill='#0a0',font='Arial 50 bold')
    pass

def drawCubeLines(app, canvas, xList, yList, z):
    for i in [-1,1]:
        for j in range(len(xList[1])):
            x0 = app.cubeCtr[0] - xList[0][j]*app.cos30 + yList[0][j]*app.cos30
            y0 = app.cubeCtr[1] - z*i + xList[0][j]/2 + yList[0][j]/2
            x1 = app.cubeCtr[0] - xList[1][j]*app.cos30 + yList[1][j]*app.cos30
            y1 = app.cubeCtr[1] - z*i + xList[1][j]/2 + yList[1][j]/2
            canvas.create_line(x0,y0,x1,y1,width=2)
    pass

def drawVertLines(app, canvas, xList, yList):
    z = app.cubeZ[2]
    for i in range(len(xList)):
        x0 = app.cubeCtr[0] - xList[i]*app.cos30 + yList[i]*app.cos30
        y0 = app.cubeCtr[1] - z + xList[i]/2 + yList[i]/2
        x1 = app.cubeCtr[0] - xList[i]*app.cos30 + yList[i]*app.cos30
        y1 = app.cubeCtr[1] + z + xList[i]/2 + yList[i]/2
        canvas.create_line(x0,y0,x1,y1,width=2)

def drawCube(app, canvas):
    xList = [[app.cubeA[0], -app.cubeA[0], app.cubeA[1], -app.cubeA[1]],
            [-app.cubeB[0], app.cubeB[0], -app.cubeB[1], app.cubeB[1]]]
    yList = [[app.cubeA[1], -app.cubeA[1], -app.cubeA[0], app.cubeA[0]],
            [-app.cubeB[1], app.cubeB[1], app.cubeB[0], -app.cubeB[0]]]
    drawCubeLines(app, canvas, xList, yList, app.cubeA[2])

    xList = [app.cubeZ[0], app.cubeZ[1], -app.cubeZ[0], -app.cubeZ[1]]
    yList = [app.cubeZ[1], -app.cubeZ[0], -app.cubeZ[1], app.cubeZ[0]]
    drawVertLines(app, canvas, xList, yList)
    pass

def drawCurrPlayerMsg(app, canvas):
    r = 50
    xCtr = app.width/3
    yCtr = app.height/10 + r
    if app.currPlayer:
        text = "Player 1: Your Turn"
        fill = "#00a"
        canvas.create_text(xCtr,yCtr,text="O",fill=fill,font="Arial 40 bold")
    elif app.currPlayer == False:
        text = "Player 2: Your Turn"
        fill = "#a00"
        canvas.create_text(xCtr,yCtr,text="X",fill=fill,font="Arial 40 bold")
    elif app.winnerSmall:
        text = "Player 1 Wins!!!"
        fill = "#00a"
    elif app.winnerSmall == False:
        text = "Player 2 Wins!!!"
        fill = "#a00"
    else:
        text = "It's a Tie!"
        fill = "#000"
    if app.smallGameOver:
        canvas.create_text(xCtr,app.height/10+30,text=app.smallMsg,
            font="Arial 15")
    canvas.create_text(xCtr,app.height/10,text=text,font="Arial 30 bold",
            fill=fill)
    pass

def cube_redrawAll(app, canvas):
    for i in range(3):
        drawSingleGrid(app, canvas, i)
    drawPieces(app, canvas)
    drawCurrPlayerMsg(app, canvas)
    drawCube(app, canvas)
    pass

runApp(width=1000,height=700)