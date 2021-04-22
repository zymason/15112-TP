from cmu_112_graphics import *
import time
import math as m

class LargeBoard(object):
    def __init__(self, board, winner):
        self.board = board
        self.winner = winner

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
    app.gameOver = False
    app.winner = None
    app.theta = 45
    app.paused = False
    app.cubeSide = 400
    app.timeInit = time.time()
    app.cubeXY = [app.cubeSide/2,app.cubeSide/6,app.cubeSide/6]
    app.cubeZ = [app.cubeSide/6,app.cubeSide/6,app.cubeSide/2]
    app.cubeCtr = [app.width/3,app.height/2]

def appStarted(app):
    initCube(app)
    app.timerDelay = 30
    app.cos30 = m.cos(m.pi/6)
    col = [None, None, None]
    app.largeBoard = [col[:], col[:], col[:]]
    app.currBigPlayer = True   # True is P1, False is P2/AI
    app.currPlayer = app.currBigPlayer
    app.mode = "cube"

def playPiece(app, pos):
    if app.board[pos[0]][pos[1]][pos[2]] == None:
        app.board[pos[0]][pos[1]][pos[2]] = app.currPlayer
        app.currPlayer = not app.currPlayer
    pass

def miniMax3():
    # Before making move, delay move to mimic human
    # time.sleep(1.5)
    pass

def miniMax2():
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
    for pos in winPoint:
        player = app.board[pos[0]][pos[1]][pos[2]]
        if player != None:
            for oppPos in getOppPos(pos):
                if (player == app.board[oppPos[0]][oppPos[1]][oppPos[2]] and 
                    player != None):
                    for i in range(len(midPos)):
                        midPos[i] = int((pos[i] + oppPos[i]) / 2)
                    if app.board[midPos[0]][midPos[1]][midPos[2]] == player:
                        app.gameOver = True
                        app.winner = player
                        app.currPlayer = None
                        return
    pass

def cube_mousePressed(app, event):
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

def checkWin2(app):
    pass

def square_mousePressed(app,event):
    pass

def cube_keyPressed(app, event):
    if event.key == "r":
        appStarted(app)
    elif event.key == "p":
        app.paused = not app.paused
    elif event.key == "Up":
        app.dTheta += 1
    elif event.key == "Down":
        app.dTheta -= 1
    # elif event.key == "s":
        # app.mode = "start"
    pass

def square_keyPressed(app, event):
    pass

def start_keyPressed(app, event):
    pass

'''
def timerFired(app):
    if time.time() - app.timeInit >= 2:
        pass
    if not app.paused:
        app.theta += app.dTheta
    pass
'''

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
                        fill = '#00f'
                    elif not player:
                        text = 'X'
                        fill = '#f00'
                    canvas.create_text(x,y,text=text,fill=fill,
                            font='Arial 20 bold')
    pass

def drawCubeLines(app, canvas, xList, yList):
    z = app.cubeXY[2]
    for i in [-1,1]:
        for j in range(len(xList[1])):
            x0 = app.cubeCtr[0] - xList[0][j]*app.cos30 + yList[0][j]*app.cos30
            y0 = app.cubeCtr[1] - z*i + xList[0][j]/2 + yList[0][j]/2
            x1 = app.cubeCtr[0] - xList[1][j]*app.cos30 + yList[1][j]*app.cos30
            y1 = app.cubeCtr[1] - z*i + xList[1][j]/2 + yList[1][j]/2
            canvas.create_line(x0,y0,x1,y1,width=2,fill=f"#{3*j}00")
    pass

def drawCube(app, canvas):
    xList = [[app.cubeXY[0], app.cubeXY[1], -app.cubeXY[1], -app.cubeXY[0]],
            [-app.cubeXY[1], -app.cubeXY[0], app.cubeXY[0], app.cubeXY[1]]]
    yList = [[app.cubeXY[1], app.cubeXY[0], app.cubeXY[0], app.cubeXY[1]],
            [-app.cubeXY[0], -app.cubeXY[1], -app.cubeXY[1], -app.cubeXY[0]]]
    drawCubeLines(app, canvas, xList, yList)
    pass

def drawCurrPlayerMsg(app, canvas):
    r = 50
    xCtr = app.width/3
    yCtr = app.height/10 + r
    if app.currPlayer:
        text = "Player 1: Your Turn"
        fill = "#00f"
        canvas.create_text(xCtr,yCtr,text="O",fill=fill,font="Arial 40 bold")
    elif app.currPlayer == False:
        text = "Player 2: Your Turn"
        fill = "#f00"
        canvas.create_text(xCtr,yCtr,text="X",fill=fill,font="Arial 40 bold")
    elif app.winner != None:
        if app.winner:
            text = "Player 1 Wins!!!"
            fill = "#00a"
        elif not app.winner:
            text = "Player 2 Wins!!!"
            fill = "#a00"
        canvas.create_text(xCtr,app.height/10+30,text="Press any key to exit",
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

def drawLargeGrid(app, canvas):
    pass

def square_redrawAll(app, canvas):
    drawLargeGrid(app, canvas)
    drawCube(app, canvas, ctrPos)
    pass

runApp(width=1000,height=700)