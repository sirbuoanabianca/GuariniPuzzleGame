import time

import game
import gameParameters
import utils
from gameParameters import *

iterations = 0
iterationsBFS = 0
iterationsUni = 0
iterationsFr = 0
iterationsA = 0
# matricea numarului de mutari in functie de offset
heuristicMatrix = [
    [0, 3, 2, 5, 2],
    [3, 4, 1, 2, 3],
    [2, 1, 4, 3, 2],
    [5, 2, 3, 2, 3]
]


def depthFirstSearch(board):
    global iterations
    nodCrt = (board, [])  # va fi tabla init si o lista de miscari
    frontiera = utils.Stack()  # stari care urmeaza sa fie explorate
    frontiera.push(nodCrt)

    frontieraSet = set()
    frontieraSet.add(list2tuple(nodCrt[0]))
    teritoriu = set()  # stari(toata tabla) care au fost deja explorate

    while not frontiera.isEmpty():
        iterations += 1

        nodCrt = frontiera.pop()

        if iterations % 100 == 0:
            print("front: ", len(frontiera.list), " ter: ", len(teritoriu), "   ", nodCrt[0])

        nodCrtTuple = list2tuple(nodCrt[0])
        frontieraSet.remove(nodCrtTuple)
        teritoriu.add(nodCrtTuple)

        if game.isFinalState(nodCrt[0]):
            return nodCrt[1]  # o lista de miscari care vor duce la tabla finala
        succesori = game.expand(nodCrt[0])  # de tipul (nextState,action,cost)
        for succesor in succesori:
            (state, action, cost) = succesor

            stateTuple = list2tuple(state)

            if stateTuple not in teritoriu and stateTuple not in frontieraSet:  # sa nu fie in teritoriu=inseamna ca deja a fost explorat
                cale = nodCrt[1] + [action]
                frontieraSet.add(stateTuple)
                frontiera.push((state, cale))  # sa nu fie in frontiera=pentru a nu-l mai adauga inca o data
    return []


def breadthFirstSearch(board):
    global iterationsBFS
    nodCrt = (board, [])  # va fi tabla init si o lista de miscari
    frontiera = utils.Queue()  # stari care urmeaza sa fie explorate
    frontiera.push(nodCrt)

    frontieraSet = set()
    frontieraSet.add(list2tuple(nodCrt[0]))
    teritoriu = set()  # stari(toata tabla) care au fost deja explorate

    while not frontiera.isEmpty():
        iterationsBFS += 1
        if iterationsBFS % 100 == 0:
            print("front: ", len(frontiera.list), " ter: ", len(teritoriu), "   ", nodCrt[0])
        nodCrt = frontiera.pop()

        nodCrtTuple = list2tuple(nodCrt[0])
        frontieraSet.remove(nodCrtTuple)
        teritoriu.add(nodCrtTuple)

        if game.isFinalState(nodCrt[0]):
            return nodCrt[1]  # o lista de miscari care vor duce la tabla finala
        succesori = game.expand(nodCrt[0])  # de tipul (nextState,action,cost)
        for succesor in succesori:
            (state, action, cost) = succesor

            stateTuple = list2tuple(state)
            if stateTuple not in teritoriu and stateTuple not in frontieraSet:  # sa nu fie in teritoriu=inseamna ca deja a fost explorat
                cale = nodCrt[1] + [action]
                frontiera.push((state, cale))  # sa nu fie in frontiera=pentru a nu-l mai adauga inca o data
                frontieraSet.add(stateTuple)

    return []

def list2tuple(state):
    tuples = []
    for row in state:
        tuples.append(tuple(row))
    return tuple(tuples)

def extractStates(lista):
    a = []
    for nodCrt in lista:
        a.append(nodCrt[0])
    return a


def uniformCostSearch(board):

    global iterationsUni, iterationsFr
    frontiera = utils.PriorityQueue()
    teritoriu = set()

    nodCrt = (board, [])
    frontieraSet = set()
    frontieraSet.add(list2tuple(nodCrt[0]))
    frontiera.push(nodCrt, 0)
    while not frontiera.isEmpty():
        iterationsUni += 1
        if iterationsUni % 100 == 0:
            print("front: ", frontiera.count, " ter: ", len(teritoriu), "   ", nodCrt[0])
        nodCrt = frontiera.pop()

        nodCrtTuple = list2tuple(nodCrt[0])
        frontieraSet.remove(nodCrtTuple)
        teritoriu.add(nodCrtTuple)

        if game.isFinalState(nodCrt[0]):
            return nodCrt[1]

        succesori = game.expand(nodCrt[0])


        for succesor in succesori:
            (state, action, cost) = succesor

            stateTuple = list2tuple(state)

            if stateTuple not in teritoriu:
                cale = nodCrt[1] + [action]
                g = game.getCostOfActionSequence(cale)

                frontiera.update((state, cale), g)
                if stateTuple not in frontieraSet:
                    frontieraSet.add(stateTuple)
    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def heuristicMatrixEstimations(board):
    # aceasta euristica alege aceeasi coloana pe care se afla piesa
    # va plasa o piesa B pe primul rand de sus
    # va plasa o piesa W pe ultimul rand
    h = 0
    offset = [0, 0]
    for row in range(gameParameters.NO_ROWS):
        for col in range(gameParameters.NO_COLS):

            if board[row][col] == '_':
                continue

            # daca piesa e deja pe pozitia finala,trecem mai departe
            if board[row][col] == 'B':
                if row == 0:
                    continue
                else:  # black trebuie sa ajunga pe primul randul
                    destRow = 0

            if board[row][col] == 'W':
                if row == gameParameters.NO_ROWS - 1:
                    continue
                else:  # white trebuie sa ajunga pe ultimul rand
                    destRow = gameParameters.NO_ROWS - 1

            offset[1] = 0  # pe aceeasi coloana
            offset[0] = abs(destRow - row)
            h += movesEst(offset)

    return h


def heuristicMatrixEstimations2(board):
    # aceasta euristica alege coloana care este libera si cu cel mai mic numar de mutari
    # va plasa o piesa B pe primul rand de sus
    # va plasa o piesa W pe ultimul rand
    h = 0
    offset = [0, 0]
    destColEst = []
    for row in range(gameParameters.NO_ROWS):
        for col in range(gameParameters.NO_COLS):

            if board[row][col] == '_':
                continue

            # daca piesa e deja pe pozitia finala, decrem euristica pt a asigura ca piesa ramane pe poz finala si trecem mai departe
            if board[row][col] == 'B':
                if row == 0:
                    h -= 1
                    continue
                else:  # black trebuie sa ajunga pe primul randul
                    destRow = 0

            if board[row][col] == 'W':
                if row == gameParameters.NO_ROWS - 1:
                    h -= 1
                    continue
                else:  # white trebuie sa ajunga pe ultimul rand
                    destRow = gameParameters.NO_ROWS - 1

            offset[0] = abs(destRow - row)
            # coloana cu cel mai mic nr de mutari
            for i in range(gameParameters.NO_COLS):
                # daca piesa curenta este diferita de piesele de pe randul destinatie
                # atunci se calculeaza offsetul fata de fiecare coloana libera/ocupata de alta piesa
                if board[row][col] != board[destRow][i]:
                    offset[1] = abs(i - col)
                    destColEst.append(movesEst(offset))
            # h += 4*min(destColEst)
            # h += 2*max(destColEst)
            h += (sum(destColEst) // len(destColEst))

    return h


def movesEst(offset):
    return heuristicMatrix[offset[0]][offset[1]]


def easyHeuristic(board):
    # euristica care numara cate piese nu sunt pe pozitia finala
    # starea care are cel mai mare nr de piese pe poz finala este aleasa
    h = 0
    for row in range(gameParameters.NO_ROWS):
        for col in range(gameParameters.NO_COLS):
            if board[row][col] == 'B' and row != 0:
                h += 1
            if board[row][col] == 'W' and row != gameParameters.NO_ROWS - 1:
                h += 1
    return 3 * h


def aStarSearch(board, heuristic=nullHeuristic):
    global iterationsA
    frontiera = utils.PriorityQueue()
    teritoriu = []
    nodCrt = (board, [])
    g = 0
    h = heuristic(board)
    f = g + h
    frontiera.push(nodCrt, f)
    while not frontiera.isEmpty():
        iterationsA += 1
        if iterationsA % 100 == 0:
            print("front: ", frontiera.count, " ter: ", len(teritoriu), "   ", nodCrt[0])
        nodCrt = frontiera.pop()
        if game.isFinalState(nodCrt[0]):
            return nodCrt[1]
        teritoriu.append(nodCrt[0])
        succesori = game.expand(nodCrt[0])
        for (state, action, cost) in succesori:
            if state not in teritoriu:
                cale = nodCrt[1] + [action]
                g = game.getCostOfActionSequence(cale)
                h = heuristic(state)
                f = g + h
                frontiera.update((state, cale), f)
    return []

bfs=breadthFirstSearch
dfs=depthFirstSearch
uni=uniformCostSearch
astar=aStarSearch

easyHeur=easyHeuristic
heur1=heuristicMatrixEstimations
heur2=heuristicMatrixEstimations2
