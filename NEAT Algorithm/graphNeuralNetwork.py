from collections import defaultdict
from collections import deque
import random

class GraphNode:
    def __init__(self, id):
        self.id = id
        self.value = 0
        self.bias = random.randint(1,100)/100

class graphNeuralNetwork: 

    def __init__(self, numInputs = 4, numOutputs = 2):
        self.idToNode = {}
        self.currId = 0

        self.ids = []
        self.inputNodes = self.outputNodes = None
        self.inputNodes = [self.addNode() for _ in range(numInputs)]
        self.outputNodes = [self.addNode() for _ in range(numOutputs)]
        self.innerNodes = []

        self.graph = defaultdict(list)
        self.reverseGraph = defaultdict(list)

        self.connections = {}
        self.connectionList = []

    def addNode(self):
        newNode = GraphNode(self.currId)
        self.idToNode[self.currId] = newNode
        self.ids.append(self.currId)

        self.currId += 1
        return self.currId - 1

    def addConnection(self):
        for _ in range(30):
            node1 = self.idToNode[random.choice(self.ids)]
            node2 = self.idToNode[random.choice(self.ids)]
            if node1 == node2:
                continue
            if (node1, node2) in self.connections:
                continue

            self.graph[node1].append(node2)
            if self.detectLoop(node1):
                self.graph[node1].pop()
                continue
            self.reverseGraph[node2].append(node1)

            self.connections[(node1, node2)] = random.randint(1,100)/100
            self.connectionList.append((node1, node2))
            break
    
    def removeConnection(self):
        if not self.connectionList:
            return False
        connectionIndex = random.randint(len(self.connectionList))
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
        if nodeId in self.inputNodes:
            return currNode.value

        currNode.value = 0
        for neighbor in self.reverseGraph[nodeId]:
            if (nodeId, neighbor) not in self.connections:
                continue
            currNode.value += self.connections[(neighbor, nodeId)]*self.getNodeValue(neighbor)
        currNode.value = max(0, currNode.value + currNode.bias)
        return currNode.value
    
    def forward(self):
        return [self.getNodeValue(outputNode) for outputNode in self.outputNodes]
        
newNet = graphNeuralNetwork()
newNet.addConnection()
newNet.addConnection()
newNet.setInputs([1,2,3,4])

for _ in range(5):
    print(newNet.forward())