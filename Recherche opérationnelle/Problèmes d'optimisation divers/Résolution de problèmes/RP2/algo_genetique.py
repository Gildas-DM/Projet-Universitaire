import random
import matplotlib.pyplot as plt
import time
from TSP import *

#####Exercice 1

###Question 1
# codage direct : ok
# codage ordinal : ok
# croisement à un point : on prend deux tournée, on choisit une position (3), z = (x_1,x_2, x_3, y_1, y_2)
# croisement à un point fondé sur le rang : pour une position <= p, on a le parent de droite. Pour une position > p, on prend le parent à gauche (si la position ne figure pas déjà chez l'enfant)

# (codage direct, croisement à un point) : convient
# (codage direct, croisement à un point fondé sur le rang) : convient

# (codage ordinal, croisement à un point) : ne convient pas, en effet soit x=(1,2,3,4,5,6,7,8,9), y =(9,8,7,6,5,4,3,2,1), et π = 2, on obtient z=(1,2,7,6,5,4,3,2,1). La tournée ne passe pas par toutes les villes donc ce n'est pas une solution.
# (codage ordinal, croisement à un point fondé sur le rang) : ne convient pas, en effet soit x=(1,2,3,4,5,6,7,8,9) le codage correspondant est (1,1,1,1,1,1,1,1,1). Soit y=(1,2,3,4,5,6,7,9,8), le codage correspondant est (1,1,1,1,1,1,1,2,1). Pour p = 2, on obtient z=(1,1,2). La tournée ne passe que par 3 villes et non par les 9 villes, ainsi z n'est pas une solution.


###Question 2
# On sélectionne deux nombres aléatoires différent i et j
# Ensuite on permute les deux villes des position i et j.
# Ainsi, pour x=(1,2,3,4,5,6,7,8,9), i=1 et j=9, on obtient z=(9,2,3,4,5,6,7,8,1)


###Question 3
#On selectionne les parents minimisant le coût de la tournée totale.
# C'est à dire les villes minimisant la somme de 1 à n, des |v_i - v_{i+1}| avec v_i la ville en position i de la tournée selectionnée


###Question 4
random.seed(13)

def generation_population(nb_villes):
    return random.sample(range(1, nb_villes+1), nb_villes)


def selection(population, villes):
    #On prend au hasard 10 candidats
    candidats = random.sample(population, 10)
    min_individu = candidats[0]
    min_evaluation = evaluation(candidats[0], villes)

    for individu in candidats:
        tmp_eval = evaluation(individu, villes)
        if(tmp_eval < min_evaluation):
            min_evaluation = tmp_eval
            min_individu = individu
    return min_individu


def croisement(parent1, parent2):
    # On prend une position entre 1 et len(parent1)-2 pour garantir la modification
    p = random.randint(1, len(parent1)-2)
    enfant = parent1[:p]
    for ville in parent2:
        if ville not in enfant:
            enfant.append(ville)
    return enfant


def mutation(individu, p_m):
    if random.random() < p_m:
        i, j = random.sample(range(len(individu)), 2)
        individu[i], individu[j] = individu[j], individu[i]
    return individu


def algorithme_genetique(taille_pop, nb_gen, p_m, villes):

    population = [generation_population(len(villes)) for _ in range(taille_pop)]

    historique = []
    meilleur_individu = population[0]
    meilleur_evaluation = evaluation(meilleur_individu, villes)
    for generation in range(nb_gen):
        nouvelle_population = []
        for i in range(taille_pop//2):
            parent1 = selection(population, villes)
            parent2 = selection(population, villes)
            enfant1 = croisement(parent1, parent2)
            enfant2 = croisement(parent1, parent2)
            enfant1 = mutation(enfant1, p_m)
            enfant2 = mutation(enfant2, p_m)
            nouvelle_population.append(enfant1)
            nouvelle_population.append(enfant2)

        population = nouvelle_population

        # Enregistrer la meilleure solution
        min_individu = population[0]
        min_evaluation = evaluation(population[0], villes)
        for individu in population:
          tmp_eval = evaluation(individu, villes)
          if(tmp_eval < min_evaluation):
              min_evaluation = tmp_eval
              min_individu = individu
        historique.append(min_evaluation)
        if(meilleur_evaluation > min_evaluation):
            meilleur_evaluation = min_evaluation
            meilleur_individu = min_individu

        print(f"Pour la génération {generation}, la meilleur valeur est : {min_evaluation}")

    return meilleur_individu, meilleur_evaluation, historique

#####Exercice 2
###Question 1
#On regarde l'ensemble des permutations de villes i et j avec i < j
def voisins(solution):
    voisins = []
    n = len(solution)

    for i in range(n - 1):
        for j in range(i + 1, n):
            voisin = solution.copy()
            voisin[i], voisin[j] = voisin[j], voisin[i]
            voisins.append(voisin)

    return voisins

def recherche_locale(solution, villes):
    voisins_solutions = voisins(solution)
    min_individu = solution
    min_evaluation = evaluation(solution, villes)

    for voisin in voisins_solutions:
        tmp_eval = evaluation(voisin, villes)
        if tmp_eval < min_evaluation:
            min_evaluation = tmp_eval
            min_individu = voisin
            # On return directement sinon l'ordinateur freeze
            return min_individu, min_evaluation

    return min_individu, min_evaluation

###Question 2
def algorithme_memetique(taille_pop, nb_gen, p_m, villes):

    population = [generation_population(len(villes)) for _ in range(taille_pop)]

    historique = []
    meilleur_individu = population[0]
    meilleur_evaluation = evaluation(meilleur_individu, villes)
    for generation in range(nb_gen):
        nouvelle_population = []
        for i in range(taille_pop//2):
            parent1 = selection(population, villes)
            parent2 = selection(population, villes)
            enfant1 = croisement(parent1, parent2)
            enfant2 = croisement(parent1, parent2)
            enfant1, _ = recherche_locale(enfant1, villes)
            enfant2, _ = recherche_locale(enfant2, villes)
            nouvelle_population.append(enfant1)
            nouvelle_population.append(enfant2)

        population = nouvelle_population

        # Enregistrer la meilleure solution
        min_individu = population[0]
        min_evaluation = evaluation(population[0], villes)
        for individu in population:
          tmp_eval = evaluation(individu, villes)
          if(tmp_eval < min_evaluation):
              min_evaluation = tmp_eval
              min_individu = individu
        historique.append(min_evaluation)
        if(meilleur_evaluation > min_evaluation):
            meilleur_evaluation = min_evaluation
            meilleur_individu = min_individu

        print(f"Pour la génération {generation}, la meilleur valeur est : {min_evaluation}")

    return meilleur_individu, meilleur_evaluation, historique

def main():

    instance = "instances/kroA100.tsp"
    data = read_tsp_data(instance)
    nbCities = int(detect_dimension(data))
    cities = read_tsp(nbCities, data)

    debut = time.time()
    meilleure, distance, historique = algorithme_genetique(taille_pop=50, nb_gen=50, p_m=0.05, villes=cities)
    fin = time.time()
    temps = fin - debut
    print("Le temps pris par l'algorithme génétique est ", temps, "s")
    print("\nLa meilleure distance pour l'algorithme génétique trouvée est :", distance)

    plottour(instance, meilleure, cities)

    plt.figure()
    plt.plot(historique)
    plt.xlabel("Nombre de générations")
    plt.ylabel("Distance de la meilleure solution")
    plt.title("Évolution de la meilleure solution - algo génétique sur kroA100")
    plt.show()



    #####Exercice 2
    ###Question 1
    debut2 = time.time()
    meilleure_recherche_loc, distance_recherche_loc = recherche_locale(meilleure, cities)
    fin2 = time.time()
    temps2 = fin2 - debut2
    print("Le temps pris par la recherche locale est ", temps2, "s")
    print("\nLa meilleure distance après recherche locale trouvée est :", distance_recherche_loc)
    plottour(instance, meilleure_recherche_loc, cities)

    ###Question 3
    debut3 = time.time()
    meilleure_algo_meme, distance_algo_meme, historique_meme = algorithme_memetique(taille_pop=50, nb_gen=50, p_m=0.05, villes=cities)
    fin3 = time.time()
    temps3 = fin3 - debut3
    print("Le temps pris par l'algorithme mémétique est ", temps3, "s")
    print("\nLa meilleure distance pour l'algorithme mémétique trouvée est :", distance_algo_meme)
    plottour(instance, meilleure_algo_meme, cities)
    
    plt.figure()
    plt.plot(historique_meme)
    plt.xlabel("Nombre de générations")
    plt.ylabel("Distance de la meilleure solution")
    plt.title("Évolution de la meilleure solution - algo mémétique sur kroA100")
    plt.show()



main()
