# 15-112 Term Project
# Zachary Mason (zymason)
# 2D strategy adapted from: https://www.rd.com/article/how-to-win-tic-tac-toe/
# 3D strategy adapted from: 
#       https://everything2.com/title/How+to+always+win+at+3D+Tic-Tac-Toe

from cmu_112_graphics import *
import time
import math as m
import copy

# Class to keep track of past games
class LargeBoard(object):
    def __init__(self, board, winner):
        self.board = board

#
def changeAngle(app, dRho=0):
    if -m.pi*92/180 < app.angle+dRho < m.pi*92/180:
        app.angle += dRho
        app.cos = m.cos(app.angle)
        app.sin = m.sin(app.angle)
        if app.angle >= 0:
            app.angleMsg = "Viewing from top"
        else:
            app.angleMsg = "Viewing from bottom"

# Starts whole app
def appStarted(app):
    app.timerDelay = 30
    app.angle = m.pi*36/180
    app.cos = m.cos(m.pi/6)
    changeAngle(app)
    app.mode = "start"
    app.modeFrom = None

# Sets number of players
def start_mousePressed(app, event):
    if event.y > app.width/7:
        if event.x < app.width/2:
            app.numPlayers = 1
        else:
            app.numPlayers = 2
        initRules(app)
        
# Draws two halves
def start_redrawAll(app, canvas):
    canvas.create_rectangle(0,app.height/7,app.width/2,app.height,
            width=0,fill='#d00')
    canvas.create_rectangle(app.width,app.height/7,app.width/2,app.height,
            width=0,fill='#00d')
    canvas.create_text(app.width/2,50,
            text="Welcome to Ultimate 3D Tic Tac Toe!",font='Arial 50 bold')
    canvas.create_text(app.width/4,app.width/3,text="Single Player",
            font='Arial 60 bold')
    canvas.create_text(app.width*3/4,app.width/3,text="Two Player",
            font='Arial 60 bold',fill='#fff')

def initRules(app):
    app.modeFrom = app.mode
    app.rules = ["To view the rules at any point in the game, simply press 'm'",
            "If you view the rules mid-game, press 'm' to go back to the game",
            "In this game, your goal is to win 3-in-a-row on the 3x3 grid by playing sub-games",
            "Each sub-game is a 3x3x3 game (3D), where you play pieces against the opponent",
            "To select where you want to play the 3D game when it's your turn, simply click on the desired spot",
            "For piece placement, click on the desired spot on the right, keeping in mind that wins can occur in any dimension",
            "To win a 3x3x3 game, you need 3-in-a-row in any direction (horizontal, vertical, or upwards)",
            "In the 3D grid, an auto-rotating cube visualization is provided and it's orientation can be changed",
            "To rotate the cube up/down, use the Up/Down arrow keys",
            "To change the autorotation speed/direction, use the Left/Right arrow keys",
            "When on the main 2D grid, you can view the 3D visual of a finished sub-game by clicking on it's grid position",
            "This view has the same interaction features as the visual within a sub-game"
            "To hide this view, simply press 'x'",
            "For Single-Player, you need to press 's' to have the AI select a sub-game location",
            "Once a sub-game is finished, press 'e' to exit and return to the primary game board",
            "All controls except for 3D cube interactions are prompted beneath the current player",
            "At any time, press 'q' to restart the game",
            "If you are ready, press 's' to start the game! Good Luck!"]
    if app.modeFrom != "start":
        app.rules = app.rules[0:-1]
    app.mode = 'rules'

def rules_keyPressed(app, event):
    if event.key == "s" and app.modeFrom == "start":
        initSquare(app)
    elif event.key == 'm' and app.modeFrom != None:
        app.mode = app.modeFrom
        app.modeFrom = None
    elif event.key == 'q':
        appStarted(app)

def rules_redrawAll(app, canvas):
    canvas.create_text(app.width/2,app.height/10,text="Rules of the Game:",
            fill='black',font='Arial 40 bold')
    for i in range(len(app.rules)):
        canvas.create_text(app.width/10,app.height/5+i*24,anchor='w',
                text='- '+app.rules[i],fill='black',font='Arial 16')

# Initializes all variables for the large 2D grid, only called once
def initSquare(app):
    col = [LargeBoard(None,None), LargeBoard(None,None), LargeBoard(None,None)]
    app.bigBoard = [col[:], col[:], col[:]]
    col = [None, None, None]
    app.bigWinners = [col[:], col[:], col[:]]
    app.currBigPlayer = True   # True is P1, False is P2/AI
    app.bigXCtr = app.width * 3/4
    app.bigYCtr = app.height/2
    app.bigOffA = app.height/4
    app.bigOffB = app.bigOffA/3
    app.board = None
    app.mode = "square"
    app.bigGameOver = False
    app.winnerBig = None
    app.numBigMoves = 0
    app.p2Delay = 0
    app.bigMsg = None
    app.dTheta = m.pi/360
    app.theta = 0
    app.rotateStarted = True
    cubeDims(app, 250)
    app.angleMsg = None

# Checks if there are two pieces in a row for 2D, returns empty position or None
def pieces2(board, opponent):
    dPos = [-1,0,1]
    for row in range(len(board)):
        for col in range(len(board[0])):
            for dRow in dPos:
                if not (0 <= row+2*dRow <= 2):
                    continue
                for dCol in dPos:
                    if not (0 <= col+2*dCol <= 2) or (dRow == dCol == 0):
                        continue
                    count = 0
                    # Checks every position-direction combination
                    pos = [[row,col],[row+dRow,col+dCol],[row+2*dRow,col+2*dCol]]
                    i = 0
                    while i < len(pos):
                        piece = board[pos[i][0]][pos[i][1]]
                        if piece == opponent:
                            count += 1
                            pos.remove(pos[i])  # Remove pos if piece is there
                            continue
                        # Break if there is opponent piece in the 3-in-a-row
                        elif piece == (not opponent) and opponent != None:
                            break
                        i += 1
                    if count == 2 and board[pos[0][0]][pos[0][1]] == None:
                        return pos[0]
    return None

# Checks if there are any spots left on the board, used in recursive
def playable(board):
    for row in board:
        for item in row:
            if item == None:
                return True
    return False

# Recursive function for minimax algorithms (both 2D and 3D)
def miniFind(board,player):
    newBoard = copy.deepcopy(board)
    winner = checkWin2(newBoard)[0]
    winners = []
    spotLeft = playable(board)
    if winner == False:
        return winner
    elif not spotLeft:
        return None
    else:
        imperativePos = pieces2(newBoard, (not player))
        if imperativePos != None:
            newBoard[imperativePos[0]][imperativePos[1]] == player
            winner = miniFind(newBoard,(not player))
            return winner
        else:
            for row in range(len(newBoard)):
                for col in range(len(newBoard[0])):
                    if newBoard[row][col] == None:
                        newBoard = copy.deepcopy(board)
                        newBoard[row][col] = player
                        winner = miniFind(newBoard,(not player))
                        winners.append(winner)
            if winners.count(False) > 0:
                i = winners.index(False)
                return False
            elif winners.count(None) > 0:
                i = winners.index(None)
                return None
            else:
                i = winners.index(True)
                return True

# Wrapper function for miniMax, returns position that will end up as a win/tie
def miniMax2(app):
    if app.numBigMoves == 1:
        # P1 Center
        if app.currBigPos[0] == 1 and app.currBigPos[1] == 1:
            return (0,0)
        # P1 Corner
        elif not (app.currBigPos[0] == 1 or app.currBigPos[1] == 1):
            return (1,1)
        # P1 Edge
        elif app.currBigPos[0] == 1 ^ app.currBigPos[1] == 1:
            return (1,1)
    else:
        winners = []
        positions = []
        imperative1 = pieces2(app.bigWinners, True)
        imperative2 = pieces2(app.bigWinners, False)
        # If P2 is about to win, make P2 win
        if imperative2 != None:
            return imperative2
        # Prevents P1 from winning
        elif imperative1 != None:
            return imperative1
        else:
            for row in range(len(app.bigWinners)):
                for col in range(len(app.bigWinners[0])):
                    if app.bigWinners[row][col] == None:
                        inList = copy.deepcopy(app.bigWinners)
                        winner = miniFind(inList,app.currBigPlayer)
                        winners.append(winner)
                        positions.append((row,col))
        if winners.count(False) > 0:
            i = winners.index(False)
            return positions[i]
        elif winners.count(None) > 0:
            i = winners.index(None)
            return positions[i]

# Checks 2D win after cube game finished, goes back to square
def switchPlayer2(app):
    player, pos = checkWin2(app.bigWinners)
    if player != None:
        app.winnerBig = player
        app.currBigPlayer = None
        app.bigWinPos = copy.copy(pos)
        app.bigGameOver = True
        app.bigMsg = "Press q to exit..."
        app.mode = "win"
    elif app.numBigMoves == 9:
        app.currBigPlayer = None
        app.bigGameOver = True
        app.winnerBig = None
        app.mode = "win"
    else:
        app.currBigPlayer = not app.currBigPlayer
        if app.currBigPlayer == False and app.numPlayers == 1:
            app.bigMsg = "Press s for the next game..."
        else:
            app.bigMsg = None
        app.board = None
        app.mode = 'square'

# Checks for 2D win, returns player and winning position
def checkWin2(board):
    midPos = [0,0]
    winPoint = {(0,0), (1,0), (2,0), (0,1), (2,2)}
    for pos in winPoint:
        if board[pos[0]][pos[1]] != None:
            player = board[pos[0]][pos[1]]
            for oppPos in getOppPos(pos):
                if player == board[oppPos[0]][oppPos[1]]:
                    for i in range(len(midPos)):
                        midPos[i] = int((pos[i] + oppPos[i]) / 2)
                    if board[midPos[0]][midPos[1]] == player:
                        return player, [pos, midPos, oppPos]
    return None, None

# Places piece on 2D board, then moves to cube game
def playSquare(app, row, col):
    if app.bigWinners[row][col] == None:
        app.currBigPos = [row, col]
        board = copy.copy(app.bigWinners)
        app.numBigMoves += 1
        initCube(app)
    else:
        app.board = app.bigBoard[row][col].board
        app.bigMsg = "Press x to close 3D board..."

# Handles mouse clicks in 2D game
def square_mousePressed(app,event):
    if app.bigGameOver:
        return
    if (app.bigXCtr - app.bigOffA <= event.x < app.bigXCtr + app.bigOffA and
        app.bigYCtr - app.bigOffA <= event.y < app.bigYCtr + app.bigOffA):
        row = int((event.y-app.bigYCtr+app.bigOffA)/(app.bigOffB*2))
        col = int((event.x-app.bigXCtr+app.bigOffA)/(app.bigOffB*2))
        if app.numPlayers == 2 or app.currBigPlayer:
            playSquare(app, row, col)
        elif app.bigWinners[row][col] != None:
            app.board = app.bigBoard[row][col].board
            app.bigMsg = "Press x to close 3D board..."
            app.angle = m.pi*36/180
            if app.angle >= 0:
                app.angleMsg = "Viewing from top"
            else:
                app.angleMsg = "Viewing from bottom"
    pass

# Handles keypresses in 2D game
def square_keyPressed(app, event):
    if event.key == 'q':
        appStarted(app)
    elif event.key == 'x':
        app.board = None
        if app.numPlayers == 1:
            app.bigMsg = "Press s for the next game..."
        else:
            app.bigMsg = None
        app.angleMsg = None
    elif event.key == 's':
        if (app.currBigPlayer == False and app.numPlayers == 1 and 
                not app.bigGameOver):
            pos = miniMax2(app)
            playSquare(app, pos[0], pos[1])
    elif event.key == "Right":
        app.dTheta += m.pi/360
        if app.dTheta > m.pi/36:
            app.dTheta = m.pi/36
    elif event.key == "Left":
        app.dTheta -= m.pi/360
        if app.dTheta < -m.pi/36:
            app.dTheta = -m.pi/36
    elif event.key == "Up":
        changeAngle(app, m.pi/90)
    elif event.key == "Down":
        changeAngle(app, -m.pi/90)
    elif event.key == 'm':
        initRules(app)
    pass

def square_timerFired(app):
    transformCoords(app)

# Draws the 2D grid
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

# Draws 2D game pieces
def drawBigPieces(app, canvas):
    dPos = app.bigOffA * 2/3
    for row in range(len(app.bigWinners)):
        for col in range(len(app.bigWinners[0])):
            player = app.bigWinners[row][col]
            if player != None:
                x = app.bigXCtr + ((col-1) * dPos)
                y = app.bigYCtr + ((row-1) * dPos)
                if player:
                    text = 'O'
                    fill = '#00d'
                elif player == False:
                    text = 'X'
                    fill = '#d00'
                canvas.create_text(x,y,text=text,fill=fill,
                        font='Arial 40 bold')
    pass

# Writes text to show current player, and win state
def drawCurrPlayerMsg2(app, canvas):
    r = 30
    xCtr = app.width/3
    yCtr = app.height/20
    if app.currBigPlayer:
        text = "Player 1: Your Turn"
        fill = "#00d"
    elif app.currBigPlayer == False:
        fill = "#d00"
        if app.numPlayers == 2:
            text = "Player 2: Your Turn"
        else:
            text = "It's Player 2's Turn"
    canvas.create_text(xCtr,yCtr+30,text=app.bigMsg,
        font="Arial 15")
    canvas.create_text(xCtr,yCtr,text=text,font="Arial 30 bold",
            fill=fill)
    pass

def drawAngleMsg(app, canvas):
    canvas.create_text(app.width/10,app.height*9/10,text=app.angleMsg,
            font="Arial 12")

# Calls all 2D mode draw functions
def square_redrawAll(app, canvas):
    drawLargeGrid(app, canvas)
    drawBigPieces(app, canvas)
    drawCurrPlayerMsg2(app, canvas)
    if app.board != None:
        drawAngleMsg(app, canvas)
    if app.board != None:
        if app.angle >= 0:
            for grid in range(2*len(app.board)-2,-1,-1):
                if grid%2 == 0:
                    drawPieceLayer(app, canvas, grid//2)
                else:
                    drawCubeLines(app, canvas, 2-grid)
        else:
            for grid in range(2*len(app.board)-1):
                if grid%2 == 0:
                    drawPieceLayer(app, canvas, grid//2)
                else:
                    drawCubeLines(app, canvas, 2-grid)
        pass

# Sets dimensions of the 3D cube
def cubeDims(app, size):
    app.cubeSide = size
    app.cubA = [app.cubeSide/2,app.cubeSide/6,app.cubeSide/6]
    app.cubB = [app.cubeSide/2,-app.cubeSide/6,app.cubeSide/6]
    app.cubZ = [app.cubeSide/6,app.cubeSide/6,app.cubeSide/2]
    app.cubeA = copy.copy(app.cubA)
    app.cubeB = copy.copy(app.cubB)
    app.cubeZ = copy.copy(app.cubZ)
    app.cubeCtr = [app.width/3, app.height * 7/12]
    app.xDims = [-app.cubeZ[0], app.cubeZ[1], -app.cubeZ[1], app.cubeZ[0]]
    app.yDims = [-app.cubeZ[1], -app.cubeZ[0], app.cubeZ[0], app.cubeZ[1]]

# Initializes all variables for 3D game, called on every new 2D position
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
    cubeDims(app, 300)# Set Cube draw variables
    app.paused = False
    app.smallGameOver = False
    app.smallMsg = None
    app.timeInit = time.time()
    app.theta = 0
    app.winPos = []
    app.numSmallMoves = 0
    app.pieceOrder = [[(0,0)],[(1,0),(0,1)],[(2,0),(1,1),(0,2)],[(2,1),(1,2)],
                    [(2,2)]]
    checkWin3(app)
    app.mode = "cube"
    app.angle = m.pi*36/180
    if app.angle >= 0:
        app.angleMsg = "Viewing from top"
    else:
        app.angleMsg = "Viewing from bottom"

# Plays 3D piece at position, checks for win
def playPiece3(app, pos):
    if app.board[pos[0]][pos[1]][pos[2]] == None:
        app.board[pos[0]][pos[1]][pos[2]] = app.currPlayer
        app.currPlayer = not app.currPlayer
        app.numSmallMoves += 1
    checkWin3(app)
    pass

# Helper function for pieces3
def pieces3Help(board, opponent, grid, row, col):
    dPos = [-1,0,1]
    for dGrid in dPos:
        if not (0 <= grid+2*dGrid <= 2):
            continue
        for dRow in dPos:
            if not (0 <= row+2*dRow <= 2):
                continue
            for dCol in dPos:
                if not (0 <= col+2*dCol <= 2) or (dRow == dCol == 0):
                    continue
                count = 0
                # Checks every position-direction combination
                pos = [[grid,row,col],[grid+dGrid,row+dRow,col+dCol],[grid+2*dGrid,row+2*dRow,col+2*dCol]]
                i = 0
                while i < len(pos):
                    piece = board[pos[i][0]][pos[i][1]][pos[i][2]]
                    if piece == opponent:
                        count += 1
                        pos.remove(pos[i])  # Remove pos if piece is there
                        continue
                    # Break if there is opponent piece in the 3-in-a-row
                    elif piece == (not opponent) and opponent != None:
                        break
                    i += 1
                if count == 2 and board[pos[0][0]][pos[0][1]][pos[0][2]] == None:
                    return pos[0]
    return None

# Finds if 2-in-a-row on 3D grid, returns position of empty space or None
def pieces3(board, opponent):
    dPos = [-1,0,1]
    for grid in range(len(board)):
        for row in range(len(board[0])):
            for col in range(len(board[0][0])):
                output = pieces3Help(board, opponent, grid, row, col)
                if output != None:
                    return output
    return None

# 3D minimax, returns position to guarantee win. Same recursive function as 2D
def miniMax3(app):
    if app.board[1][1][1] == None:
        if app.numSmallMoves == 0 or app.numSmallMoves == 1:
            return (1,1,1)
    else:
        winners = []
        positions = []
        imperative1 = pieces3(app.board, True)
        imperative2 = pieces3(app.board, False)
        # If P2 is about to win, make P2 win
        if imperative2 != None:
            return imperative2
        # Prevents P1 from winning
        elif imperative1 != None:
            return imperative1
        else:
            for grid in range(len(app.board)):
                for row in range(len(app.board[0])):
                    for col in range(len(app.board[0][0])):
                        if app.board[grid][row][col] == None:
                            inList = copy.deepcopy(app.board)
                            winner = miniFind(inList,app.currPlayer)
                            winners.append(winner)
                            positions.append((grid,row,col))
        if winners.count(False) > 0:
            i = winners.index(False)
            return positions[i]
        elif winners.count(None) > 0:
            i = winners.index(None)
            return positions[i]
    pass

# Returns a list of all positions opposite to input position
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

# Checks for a win in the 3D game, updates conditions as necessary
def checkWin3(app):
    midPos = [0,0,0]
    winPoint = {(0,0,0), (0,0,1), (0,1,0), (0,1,1), (0,2,0), (0,0,2),
                (1,0,0), (1,0,1), (1,1,0), (1,2,0), (1,2,2),
                (2,0,0), (2,2,2), (2,0,2), (2,1,2), (2,2,1)}
    for pos in winPoint:
        player = app.board[pos[0]][pos[1]][pos[2]]
        if player != None:
            for oppPos in getOppPos(pos):
                if player == app.board[oppPos[0]][oppPos[1]][oppPos[2]]:
                    for i in range(len(midPos)):
                        midPos[i] = int((pos[i] + oppPos[i]) / 2)
                    if app.board[midPos[0]][midPos[1]][midPos[2]] == player:
                        app.winnerSmall = player
                        app.currPlayer = None
                        app.winPos = [pos, midPos, oppPos]
                        app.smallGameOver = True
                        return
    pass

# Handles mouse clicks for 3D game, primarily piece placement
def cube_mousePressed(app, event):
    if not app.rotateStarted:
        return
    if app.numPlayers == 2 or app.currPlayer:
        if (app.xCtrTri - app.offATri) <= event.x < (app.xCtrTri + app.offATri):
            gridNum = int(event.y // (app.height/3))
            if (app.yCtrTri[gridNum] - app.offATri <= event.y < 
                app.yCtrTri[gridNum] + app.offATri):
                gridXRef = app.xCtrTri - app.offATri
                gridYRef = app.yCtrTri[gridNum] - app.offATri
                gridRow = int((event.y - gridYRef) // (app.offATri*2/3))
                gridCol = int((event.x - gridXRef) // (app.offATri*2/3))
                pos = (gridNum, gridRow, gridCol)
                playPiece3(app, pos)
    pass

# Handles keypresses for 3D game
def cube_keyPressed(app, event):
    if event.key == "r":
        initCube(app)
    elif event.key == "Right":
        app.dTheta += m.pi/360
        if app.dTheta > m.pi/36:
            app.dTheta = m.pi/36
    elif event.key == "Left":
        app.dTheta -= m.pi/360
        if app.dTheta < -m.pi/36:
            app.dTheta = -m.pi/36
    elif event.key == "Up":
        changeAngle(app, m.pi/90)
    elif event.key == "Down":
        changeAngle(app, -m.pi/90)
    elif event.key == 'q':
        appStarted(app)
    elif event.key == 'e' and app.smallGameOver:
        app.bigBoard[app.currBigPos[0]][app.currBigPos[1]] = LargeBoard(
                    copy.copy(app.board), app.winnerSmall)
        app.bigWinners[app.currBigPos[0]][app.currBigPos[1]] = app.winnerSmall
        switchPlayer2(app)
        cubeDims(app, 300)
    elif event.key == 'm':
        initRules(app)
    pass

def switchOrder(app):
    check = app.theta + m.pi/4
    if check%(m.pi/2) - abs(app.dTheta) <= 0:
        if app.dTheta > 0:
            newOrder = copy.deepcopy(app.pieceOrder)
            newOrder[0][0] = copy.copy(app.pieceOrder[2][2])
            newOrder[2][0] = copy.copy(app.pieceOrder[0][0])
            newOrder[4][0] = copy.copy(app.pieceOrder[2][0])
            newOrder[2][2] = copy.copy(app.pieceOrder[4][0])
            newOrder[1][0] = copy.copy(app.pieceOrder[1][1])
            newOrder[3][0] = copy.copy(app.pieceOrder[1][0])
            newOrder[3][1] = copy.copy(app.pieceOrder[3][0])
            newOrder[1][1] = copy.copy(app.pieceOrder[3][1])
        elif app.dTheta < 0:
            newOrder = copy.deepcopy(app.pieceOrder)
            newOrder[0][0] = copy.copy(app.pieceOrder[2][0])
            newOrder[2][0] = copy.copy(app.pieceOrder[4][0])
            newOrder[4][0] = copy.copy(app.pieceOrder[2][2])
            newOrder[2][2] = copy.copy(app.pieceOrder[0][0])
            newOrder[1][0] = copy.copy(app.pieceOrder[3][0])
            newOrder[3][0] = copy.copy(app.pieceOrder[3][1])
            newOrder[3][1] = copy.copy(app.pieceOrder[1][1])
            newOrder[1][1] = copy.copy(app.pieceOrder[1][0])
        app.pieceOrder = copy.deepcopy(newOrder)
    pass

def transformCoords(app):
    x1, x2 = app.cubA[0], app.cubB[0]
    y1, y2 = app.cubA[1], app.cubB[1]
    x3, y3 = app.cubZ[0], app.cubZ[1]
    app.cubeA[0] = x1*m.cos(app.theta) - y1*m.sin(app.theta)
    app.cubeA[1] = x1*m.sin(app.theta) + y1*m.cos(app.theta)
    app.cubeB[0] = x2*m.cos(app.theta) - y2*m.sin(app.theta)
    app.cubeB[1] = x2*m.sin(app.theta) + y2*m.cos(app.theta)
    app.cubeZ[0] = x3*m.cos(app.theta) - y3*m.sin(app.theta)
    app.cubeZ[1] = x3*m.sin(app.theta) + y3*m.cos(app.theta)
    app.xDims = [-app.cubeZ[0], app.cubeZ[1], -app.cubeZ[1], app.cubeZ[0]]
    app.yDims = [-app.cubeZ[1], -app.cubeZ[0], app.cubeZ[0], app.cubeZ[1]]
    app.theta += app.dTheta
    app.theta %= 2*m.pi
    newX = [None, None, None, None]
    newY = [None, None, None, None]
    for i in range(len(app.xDims)):
        if app.xDims[i] >= 0 and app.yDims[i] >= 0:
            newX[3] = app.xDims[i]
            newY[3] = app.yDims[i]
        elif app.xDims[i] < 0 and app.yDims[i] < 0:
            newX[0] = app.xDims[i]
            newY[0] = app.yDims[i]
        elif app.xDims[i] >= 0 and app.yDims[i] < 0:
            newX[1] = app.xDims[i]
            newY[1] = app.yDims[i]
        elif app.xDims[i] < 0 and app.yDims[i] >= 0:
            newX[2] = app.xDims[i]
            newY[2] = app.yDims[i]
    app.xDims = copy.copy(newX)
    app.yDims = copy.copy(newY)
    switchOrder(app)

# Prevents movement/play before given time, updates rotating cube coordinates
def cube_timerFired(app):
    if time.time() - app.timeInit >= 1 and not app.rotateStarted:
        app.rotateStarted = True
    if app.rotateStarted:
        transformCoords(app)
        if (app.currPlayer == False and app.numPlayers == 1 and 
                not app.smallGameOver):
            pos = miniMax3(app)
            playPiece3(app, pos)
    pass

# Draws one 2D grid of 3 total
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

# Draws pieces on the 2D grid
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
                        fill = '#00d'
                    elif not player:
                        text = 'X'
                        fill = '#d00'
                    canvas.create_text(x,y,text=text,fill=fill,
                            font='Arial 20 bold')
    if app.winnerSmall != None:
        for pos in app.winPos:
            x = app.xCtrTri + ((pos[2]-1) * dPos)
            y = app.yCtrTri[pos[0]] + ((pos[1]-1) * dPos)
            canvas.create_text(x,y,text='O',fill='#0a0',font='Arial 50 bold')
    pass

def drawJack(app, canvas, xPos, yPos, grid):
    z = -app.cubeSide/3*(2**0.5)
    r = app.cubeSide/8
    dx = app.cubeZ[1]
    dy = app.cubeZ[0]
    xCtr = app.cubeCtr[0] - 2*xPos*dy + 2*yPos*dx
    yCtr = app.cubeCtr[1] - z*grid*app.cos + xPos*dx*app.sin*2 + yPos*dy*app.sin*2
    canvas.create_oval(xCtr-r,yCtr-r,xCtr+r,yCtr+r,fill="red")
    pass

def drawDot(app, canvas, xPos, yPos, grid):
    z = -app.cubeSide/3*(2**0.5)
    r = app.cubeSide/8
    dx = app.cubeZ[1]
    dy = app.cubeZ[0]
    xCtr = app.cubeCtr[0] - 2*xPos*dy + 2*yPos*dx
    yCtr = app.cubeCtr[1] - z*grid*app.cos + xPos*dx*app.sin*2 + yPos*dy*app.sin*2
    canvas.create_oval(xCtr-r,yCtr-r,xCtr+r,yCtr+r,fill="blue")
    pass

def drawPieceLayer(app, canvas, grid):
    for order in range(len(app.pieceOrder)):
        for pos in app.pieceOrder[order]:
            if app.board[grid][pos[0]][pos[1]]:
                drawDot(app, canvas, pos[0]-1, pos[1]-1, grid-1)
            elif app.board[grid][pos[0]][pos[1]] == False:
                drawJack(app, canvas, pos[0]-1, pos[1]-1, grid-1)
        if order < 4:
            drawVertLines(app, canvas, app.xDims, app.yDims, order, 1-grid)
    pass

# Draws horizontal wireframe lines for rotating cube
def drawCubeLines(app, canvas, i):
    xList = [[app.cubeA[0], -app.cubeA[0], app.cubeA[1], -app.cubeA[1]],
            [-app.cubeB[0], app.cubeB[0], -app.cubeB[1], app.cubeB[1]]]
    yList = [[app.cubeA[1], -app.cubeA[1], -app.cubeA[0], app.cubeA[0]],
            [-app.cubeB[1], app.cubeB[1], app.cubeB[0], -app.cubeB[0]]]
    z = app.cubeSide/6*(2**0.5)
    for j in range(len(xList[1])):
        x0 = app.cubeCtr[0] - xList[0][j] + yList[0][j]
        y0 = app.cubeCtr[1] - z*i*app.cos + xList[0][j]*app.sin + yList[0][j]*app.sin
        x1 = app.cubeCtr[0] - xList[1][j] + yList[1][j]
        y1 = app.cubeCtr[1] - z*i*app.cos + xList[1][j]*app.sin + yList[1][j]*app.sin
        canvas.create_line(x0,y0,x1,y1,width=2)
    pass

# Draws vertical wireframe lines for rotating cube
def drawVertLines(app, canvas, xList, yList, i, grid):
    z1 = (app.cubeSide*grid/3 + app.cubeSide/6)*(2**0.5)
    z2 = (app.cubeSide*grid/3 - app.cubeSide/6)*(2**0.5)
    x0 = app.cubeCtr[0] - xList[i] + yList[i]
    y0 = app.cubeCtr[1] - z1*app.cos + xList[i]*app.sin + yList[i]*app.sin
    x1 = app.cubeCtr[0] - xList[i] + yList[i]
    y1 = app.cubeCtr[1] - z2*app.cos + xList[i]*app.sin + yList[i]*app.sin
    canvas.create_line(x0,y0,x1,y1,width=2)

# Draws current player/winner
def drawCurrPlayerMsg(app, canvas):
    r = 30
    xCtr = app.width/3
    yCtr = app.height/20
    if app.currPlayer:
        text = "Player 1: Your Turn"
        fill = "#00d"
        canvas.create_text(xCtr,yCtr+r,text="O",fill=fill,font="Arial 40 bold")
    elif app.currPlayer == False:
        text = "Player 2: Your Turn"
        fill = "#d00"
        canvas.create_text(xCtr,yCtr+r,text="X",fill=fill,font="Arial 40 bold")
    elif app.winnerSmall:
        text = "Player 1 Wins!!!"
        fill = "#00d"
    elif app.winnerSmall == False:
        text = "Player 2 Wins!!!"
        fill = "#d00"
    elif app.winnerSmall == None and app.smallGameOver:
        text = "It's a Tie!"
        fill = "#000"
    if app.smallGameOver:
        canvas.create_text(xCtr,yCtr+r,text="Press e to exit...",
            font="Arial 15")
    canvas.create_text(xCtr,yCtr,text=text,font="Arial 30 bold",
            fill=fill)
    pass

# Calls all 3D mode drawing functions
def cube_redrawAll(app, canvas):
    for i in range(3):
        drawSingleGrid(app, canvas, i)
    drawPieces(app, canvas)
    drawCurrPlayerMsg(app, canvas)
    drawAngleMsg(app, canvas)
    if app.angle >= 0:
        for grid in range(2*len(app.board)-2,-1,-1):
            if grid%2 == 0:
                drawPieceLayer(app, canvas, grid//2)
            else:
                drawCubeLines(app, canvas, 2-grid)
    else:
        for grid in range(2*len(app.board)-1):
            if grid%2 == 0:
                drawPieceLayer(app, canvas, grid//2)
            else:
                drawCubeLines(app, canvas, 2-grid)
    pass

def win_keyPressed(app, event):
    appStarted(app)

def win_redrawAll(app, canvas):
    if app.winnerBig:
        colorA = "#00d"
        colorB = "#fff"
    elif app.winnerBig == False:
        colorA = "#d00"
        colorB = "#000"
    else:
        colorA = "#fff"
        colorB = "#000"
        text = "Tie Game! That's quite rare!"
    if app.numPlayers == 1:
        if app.winnerBig == False:
            text = "Oh no! You lost!"
        elif app.winnerBig:
            text = "Congrats! You Won!"
    else:
        if app.winnerBig == False:
            text = "Player 2 Won! Good Job!"
        elif app.winnerBig:
            text = "Player 1 Won! Good Job!"
    canvas.create_rectangle(0,0,app.width,app.height,width=0,fill=colorA)
    canvas.create_text(app.width/2,app.height*9/20,text=text,fill=colorB,
            font="Arial 60 bold")
    canvas.create_text(app.width/2,app.height*9/20+50,
            text="Press any key to play again",font="Arial 20 bold",fill=colorB)
    pass

runApp(width=1000,height=700)