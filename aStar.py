import numpy as np
import pandas as pd
import time

FILE_ADDR = 'Inputs/goodTest.csv'
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

def giveEmpty(data):
    emptyRes = [i for i in range(0, 8)]
    for d in data:
        if(emptyRes.count(d)>0):
            emptyRes.remove(d)
    return emptyRes

def diagonalAttack(state, pos):
    checkingQueenData = state[queenIndex]

    for index in range(0, 8):
        if index != queenIndex:
            toCheckWith = state[index]
            if((checkingQueenData[ROW] - toCheckWith[ROW]) == (checkingQueenData[COLUMN] - toCheckWith[COLUMN])):
                return False
    return True

def moveQueen(state, index, move, emptyRows, emptyColumns):
    numMoves = 0
    newPos = state[index]
    newState = state[:]

    while(newPos[ROW] not in emptyRows):
        numMoves += 1
        newPos = [(queenPos[ROW] + move[ROW]), (queenPos[COLUMN] + move[COLUMN])]
        if(not moveIsPossible(newState, newPos)):
            return (False, None)
        newState[index] = newPos

    while(newPos[COLUMN] not in emptyColumns):
        numMoves += 1
        newPos = [(queenPos[ROW] + move[ROW]), (queenPos[COLUMN] + move[COLUMN])]
        if(not moveIsPossible(newState, newPos)):
            return (False, None)
        newState[index] = newPos

    while(diagonalAttack(newState, newPos)):
        numMoves += 1
        newPos = [(queenPos[ROW] + move[ROW]), (queenPos[COLUMN] + move[COLUMN])]
        if(not moveIsPossible(newState, newPos)):
            return (False, None)
        newState[index] = newPos
    
    return (True, newState, numMoves)

def queenIsSafe(state, queenIndex):
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

def expandNode(node, moves, emptyRows, emptyColumns):
    expandedNodes = []

    for index, queen in node.state:
        if queenIsSafe(node.state, index-1):
            continue
        for move in moves:
            res = moveQueen(node.state, index-1, move, emptyRows, emptyColumns)
            if(res[0]):
                expandedNodes.append(createNode(res[1], node, move[DIR], node.depth + res[2]))
    return expandedNodes

def boardIsSafe(state):
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
            if([row, col] in state):
                data += "x "
            else:
                data += "o "
        print(data)

    print("\n")

def visitedBefore(visitedNodes, currState, depth):    
    if( currState in visitedNodes):
        if(visitedNodes[currState] <= depth):
            return True
    return False

def aStar(start, moves):	
    nodes = []
    expandedNodes = 0
    visitedNodes = []
    
    nodes.append(createNode(start, None, None, 0))
    
    while True:
        if len(nodes) == 0: 
            return None
        nodes.sort(key = keyFunc)
        expandedNodes += 1
        node = nodes.pop(0)
        visitedNodes.append(node.state)
        if boardIsSafe(node.state):
            boards = []
            temp = node
            while True:
                boards.insert(0, temp.state)
                if temp.depth == 1: 
                    break
                temp = temp.parent
            return boards, node, len(visitedNodes)
        
        emptyRows = giveEmpty([s[ROW] for s in node.state])
        emptyColumns = giveEmpty([s[ROW] for s in node.state])

        expandedAnswer = expandNode(node, nodes, emptyRows, emptyColumns)
        expandedAnswer = [node for node in expandedAnswer if node.state not in visitedNodes]
        nodes.extend(expandedAnswer)
def h(state):
    score = 0
    for index, queen in state:
        if(not queenIsSafe(state, index - 1)):
            score = score + 1
    return score

def keyFunc(x):	
	return (x.depth + h(x.state))


def readInput(fileAddr):
    data = pd.read_csv(fileAddr, header = None, names = ['row', 'col'] )
    dataList = []
    for index, d in data.iterrows():
        currQueenData = list([d['row'], d['col']])
        dataList.append(currQueenData)
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
    start = time.clock()

    initialBoard = readInput(FILE_ADDR)
    moves = initMoves()
    res = aStar(initialBoard, moves)
    if(res != None):
        pathToRes, finalState, steps = res
        print("Elapsed Time:", time.clock() - start)
        print("Number of steps:", steps)
        print("Solution depth", finalState.depth)
        print_grid(finalState.state)
    else:
        print("No solution Found")

    


if __name__ == "__main__":
    main()