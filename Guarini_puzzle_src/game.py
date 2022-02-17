import copy

import gameParameters
from gameParameters import *

expandedNodes = 0

# initializare tabla
initBoard = [
    ['W', 'W', 'W'],
    ['_', '_', '_'],
    ['_', '_', '_'],
    ['B', 'B', 'B']
]

final = [
    ['B', 'B', 'B'],
    ['_', '_', '_'],
    ['_', '_', '_'],
    ['W', 'W', 'W']
]
'''
move:
    {
        "pieceLocation":[row,col] ,
        "offset": [rowOffset,colOffset]
    }
'''
def createInitBoard():
    board = []
    for i in range(gameParameters.NO_ROWS):
        if i == 0:
            board.append(['W'] * gameParameters.NO_COLS)
        elif i == gameParameters.NO_ROWS - 1:
            board.append(['B'] * gameParameters.NO_COLS)
        else:
            board.append(['_'] * gameParameters.NO_COLS)

    return board

def makeMove(move,boardOrig):
    if not isMoveValid(move, boardOrig):
        return  boardOrig
    board = copy.deepcopy(boardOrig)
    piece = move["pieceLocation"]
    offset = move["offset"]
    target = [piece[0] + offset[0], piece[1] + offset[1]]
    board[target[0]][target[1]] = board[piece[0]][piece[1]]
    board[piece[0]][piece[1]] ='_'
    return board

def isMoveValid(move, board):
    piece = move["pieceLocation"]
    offset = move["offset"]
    target = [piece[0] + offset[0],
              piece[1] + offset[1]
              ]

    if \
            target[0] < 0 or target[0] >= gameParameters.NO_ROWS \
                    or target[1] < 0 or target[1] >= gameParameters.NO_COLS:
        return False

    if board[piece[0]][piece[1]] == '_':
        return False

    if board[target[0]][target[1]] != '_':
        return False

    if not (abs(offset[0]) == 1 and abs(offset[1]) == 2
            or abs(offset[0]) == 2 and abs(offset[1]) == 1):
        return False

    return True


def isFinalState(board):
    first_row = ['B'] * gameParameters.NO_COLS
    last_row = ['W'] * gameParameters.NO_COLS
    others_rows = ['_'] * gameParameters.NO_COLS

    for i in range(gameParameters.NO_ROWS):
        if i == 0 and not (board[i] == first_row):
            return False

        elif i == gameParameters.NO_ROWS - 1 and not (board[i] == last_row):
            return False

        elif i!=0 and i!= gameParameters.NO_ROWS - 1 and not (board[i] == others_rows):
            return False
    return True


def generateOffsets():
    off = []
    s = [1, 2, -1, -2]
    for i in range(len(s)):
        for j in range(len(s)):
            if i != j and (i % 2 != j % 2):
                off.append([s[i], s[j]])
    return off


def getActions(board):
    #returneaza posibilele mutari
    possible_moves = []
    offsets = generateOffsets()

    for row in range(gameParameters.NO_ROWS):
        for col in range(gameParameters.NO_COLS):

            for offset in offsets:
                move_i = {"pieceLocation": [row, col], "offset": offset}
                if isMoveValid(move_i, board):
                    possible_moves.append(move_i)

    return possible_moves

def expand(board):
    #returneaza o lista de tuple (nextState,action,cost)
    #action=(pieceLocation,offset)
    #nextState=starea tablei la care se va ajunge aplicand action
    #cost=1 - toate mutarile au acelasi cost
    global expandedNodes
    expandedNodes+=1
    children = []
    for action in getActions(board):
        nextState = makeMove(action,board)
        children.append((nextState, action, 1))

    return children

def getCostOfActionSequence(cale):
    #returneaza numarul de actiuni(mutari)
    return len(cale)


# gs = initBoard  # gamestate
