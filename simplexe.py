# HACHEMI Dyhia

import numpy as np
from matplotlib import pyplot as plt

def afficher_tableau(tableau):
    """Affiche la matrice du simplexe de manière formatée et lisible."""
    for ligne in tableau: # pour chaque ligne du tableau
        ligne_propre = [] # pour le formatage des lignes
        for nbr in ligne: # pour chaque element de la ligne
            nbr = f"{nbr:6.2F}" # formatage: 6 caracteres de large avec 2 chiffres apres la virgule
            ligne_propre.append(nbr) 
        separateur = " | " # separer entre les colonnes de la ligne
        ligne = separateur.join(ligne_propre)
        print(ligne) # affichage de la ligne


def effectuer_pivot(tableau, ligne_pivot:int, colonne_pivot:int):
    """
    Modifie le tableau en place en effectuant l'opération du pivot de Gauss.
    - Divise la ligne du pivot pour que l'élément pivot devienne 1.
    - Annule les autres coefficients de la colonne du pivot (crée des 0).
    """
    # isoler la valeur pivot
    valeur_pivot = tableau[ligne_pivot][colonne_pivot]
    # normaliser la ligne pivot
    for j in range(len(tableau[ligne_pivot])):
        tableau[ligne_pivot][j] = tableau[ligne_pivot][j] / valeur_pivot
    # Mise à jour des autres lignes pour créer des zéros dans la colonne pivot
    for i in range(len(tableau)):
        if i != ligne_pivot:
            multiplicateur = tableau[i][colonne_pivot]
            for j in range(len(tableau[i])):
                tableau[i][j] = tableau[i][j] - (multiplicateur * tableau[ligne_pivot][j])

def trouver_variable_entrante(ligne_z) -> int:
    """
    Identifie la colonne entrante (le coefficient le plus négatif de la ligne Z).
    Retourne -1 si tous les coefficients sont positifs (optimum atteint).
    """
    valeur_min =  0
    index_min:int = -1 # l'index du coefficient negatif dans la ligne z par defaut c'est -1 
                       # si cette valeur ne change pas alors tous les coefficients de z sont positifs donc l'optimum est atteint
    for i in range (len(ligne_z)-1): # on parcourt les coefficients et pas la colonne du second membre
        if ligne_z[i] < valeur_min :
            valeur_min = ligne_z[i]
            index_min = i 
    return index_min

def trouver_variable_sortante(tableau, colonne_entrante) -> int:
    """
    Effectue le test du ratio minimum pour trouver la ligne sortante.
    Retourne -1 si la solution est non bornée (aucun ratio positif).
    """
    ratio_min = float('inf') # initialisation par une valeur infinie
    index_ligne = -1 # si l'index ne change pas à la fin alors la solution est non bornée
    for i in (range(1,len(tableau))): # la 1ere ne participe pas au calcul du pivot sortant
        if tableau[i][colonne_entrante] > 0:
            ratio = tableau[i][-1] / tableau[i][colonne_entrante]
            if ratio < ratio_min:
                ratio_min = ratio
                index_ligne = i
    return index_ligne

def executer_phase_2(tableau, variable_en_base):
    """
    Exécute la boucle principale de l'algorithme du Simplexe (Phase 2).
    S'arrête quand l'optimum est atteint ou si le problème est non borné.
    """
    iteration = 1
    while True:
        colonne_entrante = trouver_variable_entrante(tableau[0])
        if colonne_entrante == -1:
            print("\nFin : L'optimum est atteint !")
            break
        else: # il y a une colonne negative
            ligne_sortante = trouver_variable_sortante(tableau, colonne_entrante)
            if ligne_sortante == -1:
                print("Erreur : Problème non borné (aucun ratio valide).")
                break
            else: 
                pivot = tableau[ligne_sortante][colonne_entrante]
                print(f"\nITERATION {iteration}")
                print(f"Variable entrante: colonne {colonne_entrante}")
                print(f"Variable sortante: Ligne {ligne_sortante}")
                print(f"Elément pivot: {pivot:.2F} ")
                # Mise à jour de la base et calcul
                variable_en_base[ligne_sortante] = colonne_entrante
                effectuer_pivot(tableau, ligne_sortante, colonne_entrante)
                
                print("\nNouveau tableau après pivotage :")
                afficher_tableau(tableau)
                # Affichage de la solution de base actuelle
                valeur = []
                for i in range(1, len(tableau)):
                    valeur.append(tableau[i][-1])
                print(f"\n-Solution de base actuelle: {valeur}")
                valeur_z = tableau[0][-1]
                print(f"-Valeur de Z courante = {valeur_z:.2F}")
                iteration += 1