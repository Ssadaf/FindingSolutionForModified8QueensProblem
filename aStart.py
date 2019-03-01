import numpy as np
import pandas as pd

fileAddr = 'Inputs/in1.csv'

class Node:
	def __init__(self, state, parent, operator, depth, cost):
		self.state = state
		self.parent = parent
		self.operator = operator
		self.depth = depth
		self.cost = cost

def createNode(state, parent, operator, depth, cost):
	return Node(state, parent, operator, depth, cost)

def expandNode(node, nodes):
	expandedNodes = []

	expandedNodes.append(createNode(moveUp(node.state), node, "Up", node.depth + 1, node.cost + 1))
	expandedNodes.append(createNode(moveDown(node.state), node, "Down", node.depth + 1, node.cost + 1))
	expandedNodes.append(createNode(moveLeft(node.state), node, "Left", node.depth + 1, node.cost + 1))
	expandedNodes.append(createNode(moveRight(node.state), node, "Right", node.depth + 1, node.cost + 1))
	
	expandedNodes.append(createNode(moveUpRight(node.state), node, "UpRight", node.depth + 1, node.cost + 1))
	expandedNodes.append(createNode(moveUpLeft(node.state), node, "UpLeft", node.depth + 1, node.cost + 1))
	expandedNodes.append(createNode(moveDownRight(node.state), node, "DownRight", node.depth + 1, node.cost + 1))
	expandedNodes.append(createNode(moveDownLeft(node.state), node, "DownLeft", node.depth + 1, node.cost + 1))

	expandedNodes = [node for node in expanded_nodes if node.state != None]
	return expandedNodes

def aStar(start, goal):	
	nodes = []
	expandedNodes = 0
	visitedNodes = []

	nodes.append(createNode(start, None, None, 0, 0))

	while True:
		if len(nodes) == 0: 
			return None
		
		nodes.sort(cmp)
		expandedNodes += 1
		node = nodes.pop(0)
		visitedNodes.append(node.state)
		
		if node.state == goal:
			moves = []
			temp = node
			while True:
				moves.insert(0, temp.operator)
				if temp.depth <= 1: 
					break
				temp = temp.parent
			return moves,expandedNodes	
		expandedAnswer = expandNode(node, nodes)
		expandedAnswer = [node for node in expandedAnswer if node.state not in visitedNodes]
		nodes.extend(expandedAnswer)

def cmp(x, y):	
	answer = (x.depth + h(x.state)) - (y.depth + h(x.state))
	return answer

def h( state):
	#goal
	score = 0
	for i in range( len( state ) ):
		if state[i] != goal[i]:
			score = score + 1
	return score

class Node:
	def __init__( self, state, parent, operator, depth, cost ):
		self.state = state
		self.parent = parent
		self.operator = operator
		self.depth = depth
		self.cost = cost

def readInput(fileAddr):
	data = pd.read_csv(fileAddr, header = None, names = ['row', 'col'] )
	return data

def main():
	print("in main")
	queensData = readInput(fileAddr)

	print(queensData)

if __name__ == "__main__":
	main()