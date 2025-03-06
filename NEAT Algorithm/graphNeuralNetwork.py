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
        
        self.inputSet = set(self.inputNodes)
        self.outputSet = set(self.outputNodes)

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

            self.connections[(node1, node2)] = random.randint(1,100)/100
            self.connectionList.append((node1, node2))
            break
    
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
        currNode.value = max(0, currNode.value + currNode.bias)
        return currNode.value
    
    def forward(self):
        return [self.getNodeValue(outputNode) for outputNode in self.outputNodes]

    def mutate(self):
        for connection in self.connections.keys():
            self.connections[connection] += random.randint(-100,100)/1000

        for nodeId in self.ids:
            self.idToNode[nodeId].bias += random.randint(-100,100)/1000
        
        newNodeCount = max(0, random.randint(0,100) - 80)//10
        for _ in range(newNodeCount):
            self.addNode()
            
        removedConnectionCount = max(0, random.randint(0,100) - 85)//5
        for _ in range(removedConnectionCount):
            self.removeConnection()

        newConnectionCount = max(0, random.randint(0,100) - 70)//5
        for _ in range(newConnectionCount):
            self.addConnection()
        
newNet = graphNeuralNetwork()
newNet.addNode()
newNet.addNode()
for _ in range(100):
    newNet.addConnection()

newNet.setInputs([1,2,3,4])
for _ in range(50):
    newNet.removeConnection()
    print(len(newNet.connectionList))
    print(newNet.forward())