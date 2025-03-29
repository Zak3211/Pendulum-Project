from DoublePendulum import doublePendulum
from GNN import graphNeuralNetwork
import tkinter as tk
import pickle
import math

currFile = "GraphNetworks3.pkl"

def getInputs(currPendulum):
    """Returns network inputs"""

    return [currPendulum.xb - currPendulum.x1, currPendulum.xb - currPendulum.x2, currPendulum.by - currPendulum.y1, currPendulum.by - currPendulum.y2, currPendulum.theta1__, currPendulum.theta2__, currPendulum.theta1_, currPendulum.theta2_, currPendulum.theta1, currPendulum.theta2]

def fitness_function1(network, currPendulum = None):
    """Enforces Swing-up behavior"""

    #Initializes Downward Pendulum
    if not currPendulum:
        currPendulum = doublePendulum()
    currPendulum.theta1 = math.pi
    currPendulum.theta2 = math.pi

    fitness_score = 0
    for _ in range(3000):
        
        #Updates Pendulum and takes network output
        currPendulum.update()
        inputs = getInputs(currPendulum)
        currPendulum.xb__ = network.forward(inputs)

        #Positively Enforces Closeness to Top
        fitness_score += 1/(currPendulum.y2 - (currPendulum.by - currPendulum.L1 - currPendulum.L2) + 0.1)

    return fitness_score

def fitness_function2(network, currPendulum = None):
    """Enforces Balancing Behavior"""

    #Initializes Balanced Pendulum
    if not currPendulum:
        currPendulum = doublePendulum()
        currPendulum.theta1 = 0
        currPendulum.theta2 = 0.001

    fitness_score = 0
    for _ in range(3000):
        
        #Updates Pendulum and takes network output
        currPendulum.update()
        inputs = getInputs(currPendulum)
        currPendulum.xb__ = network.forward(inputs)

        #Ends the simulation if Pendulum becomes unbalanced
        if currPendulum.y2 >= currPendulum.by:
            return fitness_score

        #Positively reinforces pendulum being balanced
        fitness_score += 1/(currPendulum.y2 - (currPendulum.by - currPendulum.L1 - currPendulum.L2) + 0.1)
    return fitness_score

def load_networks():
    """Loads graphNeuralNetwork objects from pikl file"""

    with open(currFile, "rb") as file:
        return pickle.load(file)

def simulateGeneration():
    """Simulates one generation of networks"""

    #Initializes current generation
    curr_generation = []
    previous_generation = load_networks()

    #Populates current generation
    for network in previous_generation:

        #Creates a weighted amount of mutated offspring
        for i in range(math.floor(network[0]*2500)):
            curr_generation.append(network[1].mutate())

        #print(f"The length of the current generation is {len(curr_generation)}")

    #Categorizes the fitness of every network
    for i in range(len(curr_generation)):
        currPendulum = doublePendulum()
        fitness = fitness_function1(curr_generation[i], currPendulum=currPendulum)
        fitness += fitness_function2(curr_generation[i], currPendulum=currPendulum)
        curr_generation[i] = [fitness, curr_generation[i]]

    #Initializes next generation
    next_generation = curr_generation

    #Fetches maximum score to scale fitness for softmax
    maximum_score = max([score[0] for score in next_generation])

    #Displays the maximum score
    print(f"Maximum Score: {maximum_score}")

    base = 1.1

    #Fetches total score to scale fitness for softmax
    total = sum([math.pow(base, score[0]-maximum_score) for score in next_generation]) + 0.1
    
    #Applies softmax on all the scores
    for i in range(len(next_generation)):
        next_generation[i][0] = math.pow(base, next_generation[i][0]-maximum_score)/total

    #Writes best-performing networks to next generation
    with open(currFile, "wb") as file:
        pickle.dump(next_generation, file)

def displayPendulum():
    """Displays the best performing network from the previous generation"""

    networks = sorted(load_networks(), reverse=True, key = lambda x: x[0])
    network = networks[0][1]
    window = tk.Tk()
    canvas = tk.Canvas(window, bg = 'black', highlightthickness= 0)
    screen_width = 1000
    screen_height = 500
    canvas.config(width = screen_width, height = screen_height)
    canvas.pack()

    p = doublePendulum()
    p.theta1 = math.pi
    p.theta2 = math.pi

    x1 = p.xb + p.L1*math.sin(p.theta1)
    y1 =  p.by - p.L1*math.cos(p.theta1)
    x2 = x1 + p.L2*math.sin(p.theta2)
    y2 = y1 - p.L2*math.cos(p.theta2)
    

    line1 = canvas.create_line(p.xb, p.by, x1, y1, fill = 'white', width = 2)
    point1 = canvas.create_oval(x1 - 10, y1 - 10, x1 + 10, y1 + 10, fill='white')
    line2 = canvas.create_line(x1, y1, x2, y2, fill = 'white', width = 2)
    point2 = canvas.create_oval(x2 - 10, y2 - 10, x2 + 10, y2 + 10, fill='white')      
    base = canvas.create_line(p.xb-20, p.by, p.xb+20, p.by, fill = 'gray', width = 5)
    

    def game_loop():
        p.update()
        inputs = getInputs(p)
        p.xb__ = network.forward(inputs)

        x1 = p.xb + p.L1*math.sin(p.theta1)
        y1 = p.by - p.L1*math.cos(p.theta1)
        x2 = x1 + p.L2*math.sin(p.theta2)
        y2 = y1 - p.L2*math.cos(p.theta2)

        canvas.coords(line1, [p.xb, p.by, x1, y1])
        canvas.coords(point1, [x1 - 10, y1 - 10, x1 + 10, y1 + 10])
        canvas.coords(line2, [x1, y1, x2, y2])
        canvas.coords(point2, [x2 - 10, y2 - 10, x2 + 10, y2 + 10])  
        canvas.coords(base, [p.xb-20, p.by, p.xb+20, p.by])
        canvas.after(2, game_loop)
    
    game_loop()
    window.mainloop()

def resetNetworks():
    """Reinitializes the pikl file to random networks"""

    initialNetworks = [[1, graphNeuralNetwork(numInputs= 10)] for _ in range(35)]
    with open(currFile, "wb") as file:
        pickle.dump(initialNetworks, file)

def reevaluateNetworks():
    """Reevaluates all networks in the pikl file"""

    networks = load_networks()
    for i in range(len(networks)):
        fitness = 0
        currPendulum = doublePendulum()
        fitness += fitness_function1(networks[i][1], currPendulum=currPendulum)
        fitness += fitness_function2(networks[i][1], currPendulum=currPendulum)
        networks[i] = [fitness, networks[i][1]]

    with open(currFile, "wb") as file:
        pickle.dump(networks, file)

displayPendulum()
while True:
    break
    simulateGeneration()