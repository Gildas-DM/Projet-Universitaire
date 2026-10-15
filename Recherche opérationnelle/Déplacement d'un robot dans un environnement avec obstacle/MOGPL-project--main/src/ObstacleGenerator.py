import gurobipy as gp
from gurobipy import GRB
import random

def get_user_input():
    while True:
        try:
            M = int(input("Entrez le nombre de lignes M : "))
            N = int(input("Entrez le nombre de colonnes N : "))
            P = int(input("Entrez le nombre d'obstacles P : "))

            if M <= 0 or N <= 0:
                print("Erreur : M et N doivent être strictement positifs.")
                continue

            if P <= 0 or P > M * N:
                print(f"Erreur : P doit être compris entre 1 et {M*N}.")
                continue

            break

        except ValueError:
            print("Entrée invalide : veuillez entrer des entiers.")
    
    return M, N, P


def generate_obstacles(M, N, P):
    model = gp.Model("ObstacleGenerator")

    # Random weights
    weights = [[random.randint(0, 1000) for j in range(N)] for i in range(M)]

    # Binary variables
    x = {}
    for i in range(M):
        for j in range(N):
            x[i, j] = model.addVar(vtype=GRB.BINARY)

    model.update()

    # Objective: minimize total weight of chosen cells
    model.setObjective(
        sum(weights[i][j] * x[i, j] for i in range(M) for j in range(N)),
        GRB.MINIMIZE
    )

    # Constraint: exactly P obstacles
    model.addConstr(sum(x[i, j] for i in range(M) for j in range(N)) == P)

    # Max obstacles per row
    for i in range(M):
        model.addConstr(
            sum(x[i, j] for j in range(N)) <= 2 * P // M
        )
    # Max obstacles per col
    for j in range(N):
        model.addConstr(
            sum(x[i, j] for i in range(M)) <= 2 * P // N
        )

    # No 101 in rows
    for i in range(M):
        for j in range(N - 2):
            model.addConstr(x[i, j] + x[i, j + 2] - x[i, j + 1] <= 1)

    # No 101 in columns
    for j in range(N):
        for i in range(M - 2):
            model.addConstr(x[i, j] + x[i + 2, j] - x[i + 1, j] <= 1)

    # Solve
    model.optimize()

    print("\n--- Obstacles trouvés ---")
    blocked = []
    for i in range(M):
        for j in range(N):
            if x[i, j].X > 0.5:
                print(f"Obstacle : ({i}, {j})")
                blocked.append((i, j))

    return blocked
