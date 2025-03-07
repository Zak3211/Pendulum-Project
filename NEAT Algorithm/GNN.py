from collections import defaultdict
from collections import deque
import random
import math
import copy

class GraphNode:
    def __init__(self, id):
        self.id = id
        self.value = 0
        self.bias = random.randint(-100,100)/100

class graphNeuralNetwork: 
    def __init__(self, numInputs = 5, numOutputs = 1):
        self.idToNode = {}
        self.currId = 0

        self.ids = []
        self.inputNodes = self.outputNodes = None
        self.inputNodes = [self.addNode() for _ in range(numInputs)]
        self.outputNodes = [self.addNode() for _ in range(numOutputs)]
        self.inputSet = set(self.inputNodes)
        self.outputSet = set(self.outputNodes)

        self.graph = defaultdict(list)
        self.reverseGraph = defaultdict(list)

        self.connections = {}
        self.connectionList = []

        self.addNode()
        self.addNode()
        for _ in range(15):
            self.addConnection()

    def addNode(self):
        newNode = GraphNode(self.currId)
        self.idToNode[self.currId] = newNode
        self.ids.append(self.currId)

        self.currId += 1
        return self.currId - 1

    def addConnection(self):
        for _ in range(30):
            node1 = random.choice(self.ids)
            node2 = random.choice(self.ids)
            if node1 == node2:
                continue
            if node1 in self.outputSet or node2 in self.inputSet:
                continue
            if (node1, node2) in self.connections:
                continue

            self.graph[node1].append(node2)
            if self.detectLoop(node1):
                self.graph[node1].pop()
                continue
            self.reverseGraph[node2].append(node1)

            self.connections[(node1, node2)] = random.randint(-100,100)/100
            self.connectionList.append((node1, node2))
            return True
        self.addNode()
        return False
    
    def removeConnection(self):
        if not self.connectionList:
            return False
        connectionIndex = random.randint(0, len(self.connectionList)-1)
        del self.connections[self.connectionList[connectionIndex]]
        self.connectionList.pop(connectionIndex)
        return True        

    def detectLoop(self, nodeId):
        visited = set()
        queue = deque([nodeId])
        while queue:
            currNode = queue.popleft()
            if currNode in visited:
                return True
            visited.add(currNode)
            for neighbour in self.graph[currNode]:
                queue.append(neighbour)
        return False

    def setInputs(self, inputs):
        for i in range(len(inputs)):
            self.idToNode[self.inputNodes[i]].value = inputs[i]

    def getNodeValue(self, nodeId):
        currNode = self.idToNode[nodeId]
        if nodeId in self.inputSet:
            return currNode.value

        currNode.value = 0
        for neighbor in self.reverseGraph[nodeId]:
            if (neighbor, nodeId) not in self.connections:
                continue
            currNode.value += self.connections[(neighbor, nodeId)]*self.getNodeValue(neighbor)
        currNode.value = math.tanh(currNode.value + currNode.bias) 
        return currNode.value
    
    def forward(self, inputs):
        self.setInputs(inputs)
        outPutLayer = [self.getNodeValue(outputNode) for outputNode in self.outputNodes]
        if len(outPutLayer) == 1:
            outPutLayer = outPutLayer[0]
        return 100*outPutLayer

    def mutate(self):
        newNetwork = copy.deepcopy(self)

        for connection in newNetwork.connections.keys():
            newNetwork.connections[connection] += random.randint(-100,100)/600
        for nodeId in newNetwork.ids:
            newNetwork.idToNode[nodeId].bias += random.randint(-100,100)/600
        
            
        random_variable = random.randint(0,15)
        if random_variable == 1:
            newNetwork.addConnection()
        elif random_variable == 2:
            newNetwork.removeConnection()

        return newNetwork
