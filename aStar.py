import numpy as np
import pandas as pd
import time

FILE_ADDR = 'Inputs/in3.csv'
ROW = 0
COLUMN = 1
DIR = 2

class Node:
    def __init__(self, state, parent, operator, depth, heuristic):
        self.state = state
        self.parent = parent
        self.operator = operator
        self.depth = depth
        self.heuristic = heuristic

def createNode(state, parent, operator, depth, heuristic):
    return Node(state, parent, operator, depth, heuristic)
    
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

def moveQueen(state, index, move):
    queenPos = state[index]
    newPos = [(queenPos[ROW] + move[ROW]), (queenPos[COLUMN] + move[COLUMN])]

    newState = state[:]
    if moveIsPossible(state, newPos):
        newState[index] = newPos
        return newState
    else:
        return None

def queenIsSafe(state, queenIndex):
    i = 0
    checkingQueenData = state[queenIndex]

    for index in range(0, 8):
        if index != queenIndex:
            toCheckWith = state[index]
            if(toCheckWith[ROW] == checkingQueenData[ROW]):
                i += 1
                continue
            if(toCheckWith[COLUMN] == checkingQueenData[COLUMN]):
                i += 1
                continue
            if(abs(checkingQueenData[ROW] - toCheckWith[ROW]) == abs(checkingQueenData[COLUMN] - toCheckWith[COLUMN])):
                i += 1
                continue
    return i

def h(state):
    score = 0
    index = 0
    for queen in state:
        score += queenIsSafe(state, index - 1)
        index += 1
    
    # if(score % 2 ==1):
    #     queenIndex = 0
    #     for queen in state:
    #         print(queenIndex)
    #         queenIndex += 1
    #     print(":::::::")
    #     print_grid(state)
    #     for queenIndex, queen in state:
    #         queenIndex = queenIndex - 1
    #         checkingQueenData = state[queenIndex]
    #         print("##", queenIndex,"###", checkingQueenData)
    #         for index in range(0, 8):
    #             if index != queenIndex:
    #                 toCheckWith = state[index]
    #                 print(index , "***", toCheckWith)
    #                 if(toCheckWith[ROW] == checkingQueenData[ROW]):
    #                     print(toCheckWith)
    #                     continue
    #                 if(toCheckWith[COLUMN] == checkingQueenData[COLUMN]):
    #                     print(toCheckWith)
    #                     continue
    #                 if(abs(checkingQueenData[ROW] - toCheckWith[ROW]) == abs(checkingQueenData[COLUMN] - toCheckWith[COLUMN])):
    #                     print(toCheckWith)                                             
    #                     continue
    #     quit()
                    


    return score

def heuristicFunc(depth, state):   
    return (depth + h(state))

def expandNode(node, moves):
    expandedNodes = []
    index = 0

    for  queen in node.state:
        for move in moves:
            res = moveQueen(node.state, index, move)
            if(res != None):
                expandedNodes.append(createNode(res, node, move[DIR], node.depth + 1, heuristicFunc(node.depth + 1, res)))
        index += 1
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
            if(abs(firstQueen[ROW] - secondQueen[ROW]) == abs(firstQueen[COLUMN] - secondQueen[COLUMN])):
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

def keyFunc(x):
    return x.heuristic

def aStar(start, moves):    
    nodes = []
    expandedNodes = 0
    moves = initMoves()

    nodes.append(createNode(start, None, None, 0, heuristicFunc(0, start)))
    
    while True:
        if len(nodes) == 0: 
            return None

        nodes.sort(key = keyFunc)
        expandedNodes += 1
        node = nodes.pop(0)

       


        if boardIsSafe(node.state):
            return node, expandedNodes
        
        expandedAnswer = expandNode(node, moves)
        nodes.extend(expandedAnswer)

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
    moves = initMoves()

    initialBoard = readInput(FILE_ADDR)
    moves = initMoves()
    res = aStar(initialBoard, moves)
    if(res != None):
        finalState, steps = res
        print("Elapsed Time:", time.clock() - start)
        print("Number of steps:", steps)
        print("Solution depth", finalState.depth)
        print_grid(finalState.state)
    else:
        print("No solution Found")

if __name__ == "__main__":
    main()