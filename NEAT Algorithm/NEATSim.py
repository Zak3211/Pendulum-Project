from DoublePendulum import doublePendulum
from GNN import graphNeuralNetwork
import tkinter as tk
import pickle
import math

def simulate(network):
    currPendulum = doublePendulum()
    
    fitness_score = 0
    remaining_epochs = 3000
    prev = False
    while remaining_epochs > 0 and fitness_score < 100000:
        currPendulum.update()
        inputs = [currPendulum.theta1_, currPendulum.theta2_, currPendulum.theta1, currPendulum.theta2, currPendulum.xb]
        currPendulum.xb__ = network.forward(inputs)

        target_height = 60
        if currPendulum.y2 > target_height:
            if prev and currPendulum.y2 > target_height + 15:
                fitness_score -= 100
            if prev and currPendulum.y1 > currPendulum.by:
                fitness_score -= 3
            remaining_epochs -= 1
            prev = False
        else:
            prev = True
            fitness_score += 1
        if currPendulum.y2 <= 53:
            fitness_score += 5

        if currPendulum.xb == currPendulum.boundary or currPendulum.xb == currPendulum.width - currPendulum.boundary:
            return -math.inf
    return fitness_score


def load_networks():
    with open(f"GraphNetworks.pkl", "rb") as file:
        return pickle.load(file)

def simulateGeneration():
    initial = load_networks()

    offspring = []
    for brain in initial:
        for i in range(10):
            offspring.append(brain[1].mutate())

    avg_score = 0
    for i in range(len(offspring)):
        total = simulate(offspring[i])
        offspring[i] = [total, offspring[i]]
        avg_score += total

    avg_score /= len(offspring)
    #offspring.extend(initial)
    offspring.sort(reverse= True, key = lambda x: x[0])

    print([offspring[i][0] for i in range(15)])
    offspring = offspring[:35]
    offspring = [child for child in offspring]
    print(offspring[0][1].connectionList)

    with open("GraphNetworks.pkl", "wb") as file:
        pickle.dump(offspring, file)

def displayPendulum():
    network = load_networks()[0]
    print(network[0])
    network = network[1]
    window = tk.Tk()
    canvas = tk.Canvas(window, bg = 'black', highlightthickness= 0)
    screen_width = 1000
    screen_height = 500
    canvas.config(width = screen_width, height = screen_height)
    canvas.pack()

    p = doublePendulum()

    x1 = p.xb + p.L1*math.sin(p.theta1)
    y1 =  p.by - p.L1*math.cos(p.theta1)
    x2 = x1 + p.L2*math.sin(p.theta2)
    y2 = y1 - p.L2*math.cos(p.theta2)

    line1 = canvas.create_line(p.xb, p.by, x1, y1, fill = 'white', width = 2)
    point1 = canvas.create_oval(x1 - 10, y1 - 10, x1 + 10, y1 + 10, fill='white')
    line2 = canvas.create_line(x1, y1, x2, y2, fill = 'white', width = 2)
    point2 = canvas.create_oval(x2 - 10, y2 - 10, x2 + 10, y2 + 10, fill='white')      
    base = canvas.create_line(p.xb-20, p.by, p.xb+20, p.by, fill = 'gray', width = 5)
    
    epochs = 3000
    fitness_score = 0
    prev = False
    def game_loop():
        nonlocal epochs
        nonlocal fitness_score
        nonlocal prev

        if epochs < 0:
            return
        
        p.update()
        inputs = [p.theta1_, p.theta2_, p.theta1, p.theta2, p.xb]
        p.xb__ = network.forward(inputs)

        target_height = 55
        if p.y2 > target_height:
            if prev:
                if p.y2 > target_height + 15:
                    fitness_score -= 350
            epochs -= 1
            prev = False
        else:
            prev = True
            fitness_score += 1

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
    print(fitness_score)

def resetNetworks():
    initialNetworks = [[0, graphNeuralNetwork()] for _ in range(35)]
    with open("GraphNetworks.pkl", "wb") as file:
        pickle.dump(initialNetworks, file)

def reevaluateNetworks():
    networks = load_networks()
    for i in range(len(networks)):
        networks[i][0] = simulate(networks[i][1])
    with open("GraphNetworks.pkl", "wb") as file:
        pickle.dump(networks, file)


#displayPendulum()
while True:
    simulateGeneration()