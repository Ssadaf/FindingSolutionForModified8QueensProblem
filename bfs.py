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

	for index, queen in node.state.iterrows():
		expandedNodes.append

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

def bfs( start, goal ):
	nodes = []
	expandedNodes = 0
	visitedNodes = []
	
	nodes.append(create_node(start, None, None, 0, 0))

	while True:
		if len(nodes) == 0: 
			return None
		expandedNodes += 1
		node = nodes.pop(0)
		visitedNodes.append(node.state)
		
		if node.state == goal:
			moves = []
			temp = node
			while True:
				moves.insert(0, temp.operator)
				if temp.depth == 1: 
					break
				temp = temp.parent
			return moves, expandedNodes					
		expandedAnswer = expandNode(node, nodes)
		expandedAnswer = [node for node in expandedAnswer if node.state not in visitedNodes]
		
		nodes.extend(expandedAnswer)

def readInput(fileAddr):
	data = pd.read_csv(fileAddr, header = None, names = ['row', 'col'] )
	dataList = []
	for index, d in data.iterrows():
		currQueenData = list([d['row'], d['col']])
		dataList.append(currQueenData)
	return dataList

def main():
	print("in main")
	queensData = readInput(fileAddr)

	for queen in queensData:
		print(queen)

if __name__ == "__main__":
	main()