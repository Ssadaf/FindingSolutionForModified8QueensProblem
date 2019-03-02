import numpy as np
import pandas as pd
import time 

FILE_ADDR = 'new_tests/test_a.csv'
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

# def moveQueen(state, index, move):
# 	queenPos = state[index]
# 	newPos = [(queenPos[ROW] + move[ROW]), (queenPos[COLUMN] + move[COLUMN])]

# 	newState = state[:]
# 	if moveIsPossible(state, newPos):
# 		newState[index] = newPos
# 		return newState
# 	else:
# 		return None

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


def expandNode(node, moves, visitedNodes):
	expandedNodes = []
	currState = ([x for x in node.state])

	for i, queen in currState:
		index = i-1
		queenPos = currState[index]
		for move in moves:
			newPos = ((queenPos[ROW] + move[ROW]), (queenPos[COLUMN] + move[COLUMN]))
			newState = currState[:]
			newState[index] = newPos
			newState = frozenset(newState)
			if newState in visitedNodes:
				continue
			if moveIsPossible(currState, newPos):
				expandedNodes.append(createNode(newState, node, move[DIR], node.depth + 1))	
	return expandedNodes

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

def bfs(start, moves):
	nodes = []
	visitedNodes = set()
	
	nodes.append(createNode(start, None, None, 0))

	while True:
		if len(nodes) == 0: 
			return None
		
		node = nodes.pop(0)
		if(node.state in visitedNodes):
			continue
		visitedNodes.add(node.state)
		
		i = 0		 					
		expandedAnswer = expandNode(node, moves, visitedNodes)
		for expNode in expandedAnswer:
			i += 1
			if boardIsSafe(expNode.state):
				return expNode, (len(visitedNodes) + i)		
		nodes.extend(expandedAnswer)

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
	start = time.clock()

	initialBoard = readInput(FILE_ADDR)
	moves = initMoves()
	finalState, steps = bfs(initialBoard, moves)

	print("Elapsed Time:", time.clock() - start)
	print("Number of steps:", steps)
	print("Solution depth", finalState.depth)
	print_grid(finalState.state)


if __name__ == "__main__":
	main()