from src.Graph import *
from src.Solver import *
from src.Parser import *
from src.ObstacleGenerator import *


def testRandomGraphs():
    size = [10,20,30,40,50]
    nblocked = [10,20,30,40,50]
    solver = Solver() 
    for s,nb in zip(size,nblocked): 
        g = generateRandomGraph(s,s,nb)
        print(g)
        solver.writeOutput(solver.bfsSolver(g))

        

def ask_coordinates(max_x, max_y):
        x = int(input(f"Entrez la coordonnée x du point (0 à {max_x}) : "))
        y = int(input(f"Entrez la coordonnée y du point (0 à {max_y}) : "))

        if 0 <= x <= max_x and 0 <= y <= max_y:
            return x, y
        else:
            print("Coordonnées hors limites.")

def ask_orientation():
    orientations = ["nord", "sud", "est", "ouest"]
    o = input("Orientation initiale (nord/sud/est/ouest) : ")
    if o in orientations:
            return o
    print("Orientation invalide.")

def main():
    print("--- Générateur de poids + Solveur BFS ---")
    while True:
        try:
            M = int(input("Nombre de lignes M : "))
            N = int(input("Nombre de colonnes N : "))
            P = int(input("Nombre d'obstacles P : "))
            break
        except ValueError:
            print("Entrée invalide.")

    print("\n--- Génération des obstacles avec Gurobi ---")
    blocked = generate_obstacles(M, N, P)
    
    print("\n--- Matrice des obstacles ---")
    for x in range(M):
        row = ""
        for y in range(N):
            row += "1 " if (x, y) in blocked else "0 "
        print(row)
    
    obstacles = []
    for (x, y) in blocked:
        obstacles.extend([(x, y),(x+1,y),(x,y+1),(x+1,y+1)])


    print("\n--- Choisissez un point de départ ---")
    start_x, start_y = ask_coordinates(N, M)
    while (start_x, start_y) in obstacles:
        print("Ce point contient un obstacle. Choisissez un autre point.")
        print("\n--- Choisissez un point de départ ---")
        start_x, start_y = ask_coordinates(N, M)

    orientation = ask_orientation()
    while orientation not in ["nord", "sud", "est", "ouest"]:
        orientation = ask_orientation()



    print("\n--- Choisissez un point d'arrivée ---")
    end_x, end_y = ask_coordinates(N, M)
    while (end_x, end_y) in obstacles or (end_x, end_y) == (start_x, start_y):
        print("Ce point contient un obstacle ou est identique au point de départ. Choisissez un autre point.")
        print("\n--- Choisissez un point d'arrivée ---")
        end_x, end_y = ask_coordinates(N, M)


    print("\n--- Construction du graphe ---")
    			
    g = Graph(start_x, start_y, end_x, end_y, N, M, orientation, obstacles)
    g.createGraph()
    print(g)
    
    with open("examples/entree.txt", "w") as f:
        f.write(str(g))



    print("\n--- Résolution BFS ---")
    solver = Solver()
    best_path = solver.bfsSolver(g)

    solution = solver.writeOutput(best_path)
    return solution


def testRandomGraphs():
    size = [10,20,30,40,50]
    nblocked = [10,20,30,40,50]
    solver = Solver() 
    for s,nb in zip(size,nblocked): 
        g = generateRandomGraph(s,s,nb)
        print(g)
        print(solver.writeOutput(solver.bfsSolver(g)))


#Affichage de la solution pour la matrice du fichier ex1.txt situé dans le repertoir examples
#p = Parser()
#initX, initY, endX, endY, width, length, initOrientation, listBlocked =p.parseFile("examples/ex1.txt")
#g = Graph(initX, initY, endX, endY, width, length, initOrientation, listBlocked)
#g.createGraph()
#print(g)
#solver = Solver()
#print(solver.writeOutput(solver.bfsSolver(g)))
# Affichage d'un graphe choisit par l'utilisateur selon les contraintes de la question (e)
print(main())
