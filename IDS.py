import numpy as np
import pandas as pd
import time 

FILE_ADDR = 'new_tests/test_c.csv'
ROW = 0
COLUMN = 1
DIR = 2

class Node:
    def __init__(self, state, parent, operator, depth):
        self.state = state
        self.parent = parent
        self.operator = operator
        self.depth = depth

def createNode(state, parent, operator, depth):
    return Node(state, parent, operator, depth)

def moveIsPossible(state, newPos):
    #is in the board
    if((newPos[ROW]    < 1) or (newPos[ROW]    > 8)):
        return False
    if((newPos[COLUMN] < 1) or (newPos[COLUMN] > 8)):
        return False
    #is empty
    if(newPos in state):
        return False
    return True

def moveQueen(currState, index, move):
    state = ([x for x in currState])
    queenPos = state[index]
    newPos = ((queenPos[ROW] + move[ROW]), (queenPos[COLUMN] + move[COLUMN]))

    newState = state[:]
    if moveIsPossible(state, newPos):
        newState[index] = newPos
        return frozenset(newState)
    else:
        return None

def queenIsSafe(currState, queenIndex):
    state = ([x for x in currState])
    checkingQueenData = state[queenIndex]

    for index in range(0, 8):
        if index != queenIndex:
            toCheckWith = state[index]
            if(toCheckWith[ROW] == checkingQueenData[ROW]):
                return False
            if(toCheckWith[COLUMN] == checkingQueenData[COLUMN]):
                return False
            if((checkingQueenData[ROW] - toCheckWith[ROW]) == (checkingQueenData[COLUMN] - toCheckWith[COLUMN])):
                return False
    return True

def boardIsSafe(currState):
    state = ([x for x in currState])
    for first in range(0, 8):
        firstQueen = state[first]
        for second in range(first+1, 8):
            secondQueen = state[second]
            if(firstQueen[ROW] == secondQueen[ROW]):
                return False
            if(firstQueen[COLUMN] == secondQueen[COLUMN]):
                return False
            if((firstQueen[ROW] - secondQueen[ROW]) == (firstQueen[COLUMN] - secondQueen[COLUMN])):
                return False
    return True


def print_grid(state):
    for row in range(1, 9):
        data = ""
        for col in range(1,9):
            if((row, col) in state):
                data += "x "
            else:
                data += "o "
        print(data)

    print("\n")

def visitedBefore(visitedNodes, currState, depth):    
    if(currState in visitedNodes):
        if(visitedNodes[currState] <= depth):
            return True
    return False

def DFS(node, moves, maxDepth, visitedNodes):
    currState = node.state    
    if(visitedBefore(visitedNodes, currState, node.depth)):
        return (False, None)
   
    visitedNodes[currState] = node.depth
   
    if boardIsSafe(currState):
        return (True, node, len(visitedNodes))                  

    if maxDepth <= 0:
        return (False, None)

    for index, queen in node.state:
        for move in moves:
            newState = moveQueen(currState, index-1, move)
            if(newState == None):
                continue
            result = DFS(createNode(newState, node, move[DIR], node.depth + 1), moves, maxDepth - 1, visitedNodes)
            if(result[0]):
                return (True, result[1], result[2])
    return (False, None)

def IDDFS(start, moves):
    initialState = createNode(start, None, None, 0)
    
    i = 0
    while True:
        print(i)
        visitedNodes = {}
        result = DFS(initialState, moves, i, visitedNodes) 
        if(result[0]):
            return (True, result[1], result[2])
        i += 1

def readInput(fileAddr):
    data = pd.read_csv(fileAddr, header = None, names = ['row', 'col'] )
    dataList = []
    for index, d in data.iterrows():
        currQueenData = (d['row'], d['col'])
        dataList.append(currQueenData)
    dataList = frozenset(dataList)
    return dataList

def initMoves():
    moves = []

    moves.append([ 0,  1, 'R'])
    moves.append([ 0, -1, 'L'])
    moves.append([-1,  0, 'U'])
    moves.append([ 1,  0, 'D'])
    moves.append([-1,  1, 'RU'])
    moves.append([ 1,  1, 'RD'])
    moves.append([-1, -1, 'LU'])
    moves.append([ 1, -1, 'LD'])

    return moves

def main():
    initialBoard = readInput(FILE_ADDR)
    print_grid(initialBoard)
    moves = initMoves()
    
    start = time.clock()    
    result = IDDFS(initialBoard, moves)
    print("Elapsed Time:", time.clock() - start)
    if(result[0]):
        finalState = result[1]
        steps = result[2]
        print("Number of steps:", steps)
        print("Solution depth", finalState.depth)
        print_grid(finalState.state)
    else:
        print("No solution Found")


if __name__ == "__main__":
    main()