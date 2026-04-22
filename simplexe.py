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

def saisir_vecteur(message, n):
    """Demande à l'utilisateur de saisir exactement 'n' valeurs numériques."""
    while True:
        try:
            vals = list(map(float, input(message).split()))
            if len(vals) == n:
                return vals
            print("Entrez exactement " + str(n) + " valeurs.")
        except ValueError:
            print("Valeurs invalides.")

def saisir_probleme():
    """Gère l'interaction avec l'utilisateur pour définir le problème linéaire."""
    while True:
        sens = input("\nType d'optimisation (max / min) : ").strip().lower()
        if sens in ("max", "min"):
            break
        print("  Entrez 'max' ou 'min'.")

    while True:
        try:
            n = int(input("\nNombre de variables de decision : "))
            if n >= 1:
                break
        except ValueError:
            pass
        print("  Entrez un entier >= 1.")

    noms_x = ["x" + str(j+1) for j in range(n)]
    print("Variables : " + ", ".join(noms_x))

    print("\nFonction objectif : " + sens.upper() + " Z")
    c = saisir_vecteur("Coefficients Z [" + ", ".join(noms_x) + "] : ", n)

    while True:
        try:
            m = int(input("\nNombre de contraintes : "))
            if m >= 1:
                break
        except ValueError:
            pass
        print("Entrez un entier >= 1.")

    A, b, types = [], [], []
    print("Saisie des contraintes :")

    for i in range(m):
        print("Contrainte " + str(i+1) + " :")
        ai = saisir_vecteur("  Coefficients [" + ", ".join(noms_x) + "] : ", n)
        while True:
            t = input("  Signe (<= / >= / =) : ").strip()
            if t in ("<=", ">=", "="):
                break
            print("Entrez <=, >= ou =.")
        
        while True:
            try:
                bi = float(input("  Membre droit b" + str(i+1) + " : "))
                break
            except ValueError:
                print("Entrez un nombre reel.")
        A.append(ai)
        b.append(bi)
        types.append(t)

    return sens, n, c, m, A, b, types, noms_x

def preparer_tableau(sens, n, c, m, A, b, types):
    """
    Traduit les données de l'utilisateur en un tableau matriciel compatible
    avec notre algorithme (Ligne Z à l'indice 0).
    Gère la création des variables d'écart, d'excédent et artificielles.
    """

    # Compter les variables nécessaires
    nb_ecart = types.count("<=")
    nb_excedent = types.count(">=")
    nb_artificielle = types.count(">=") + types.count("=")
    
    total_colonnes = n + nb_ecart + nb_excedent + nb_artificielle + 1 # +1 pour le RHS
    
    # Création de la coquille vide et de la base
    tableau = [[0.0 for _ in range(total_colonnes)] for _ in range(m + 1)]
    variables_en_base = [-1] * (m + 1) # -1 pour la ligne Z qui n'a pas de variable en base
    
    # Remplissage de la ligne Z (Indice 0)
    # Pour un problème MAX, on met les coefficients en négatif dans le tableau.
    # Pour un problème MIN, c'est l'inverse.
    for j in range(n):
        if sens == "max":
            tableau[0][j] = -c[j]
        else:
            tableau[0][j] = c[j] 
            
    # Remplissage des contraintes
    curseur_colonne = n # On commence à ajouter les variables après les x
    
    for i in range(m):
        ligne_actuelle = i + 1 # Car la ligne 0 est pour Z
        
        # Copier les coefficients des variables de décision (x)
        for j in range(n):
            tableau[ligne_actuelle][j] = A[i][j]
            
        # Copier le second membre (RHS) à la toute fin
        tableau[ligne_actuelle][-1] = b[i]
        
        # Ajouter les variables selon le signe
        signe = types[i]
        
        if signe == "<=":
            tableau[ligne_actuelle][curseur_colonne] = 1.0 # Variable d'écart
            variables_en_base[ligne_actuelle] = curseur_colonne
            curseur_colonne += 1
            
        elif signe == ">=":
            tableau[ligne_actuelle][curseur_colonne] = -1.0 # Variable d'excédent
            curseur_colonne += 1
            tableau[ligne_actuelle][curseur_colonne] = 1.0 # Variable artificielle
            variables_en_base[ligne_actuelle] = curseur_colonne
            curseur_colonne += 1
            
        elif signe == "=":
            tableau[ligne_actuelle][curseur_colonne] = 1.0 # Variable artificielle
            variables_en_base[ligne_actuelle] = curseur_colonne
            curseur_colonne += 1

    # On renvoie aussi le nombre de variables artificielles créées.
    # Si c'est > 0, le programme saura qu'il doit faire la Phase 1 (Deux Phases) !
    return tableau, variables_en_base, nb_artificielle

def executer_phase_1(tableau, variables_en_base, types):
    """
    Gère la Phase 1 du Simplexe pour chasser les variables artificielles.
    Crée une fonction objectif temporaire, lance le pivotage, et vérifie la faisabilité.
    """
    print("\nDÉMARRAGE DE LA PHASE 1")

    # Sauvegarde de la vraie ligne Z (avec la méthode .copy() pour ne pas la perdre)
    vraie_ligne_z = tableau[0].copy()

    # On remplace la ligne Z actuelle par des zéros
    colonnes = len(tableau[0])
    tableau[0] = [0.0 for _ in range(colonnes)]

    # La ruse mathématique : on construit le "Faux objectif"
    # Pour chaque contrainte qui avait un >= ou un =, il y a une variable artificielle.
    # On doit soustraire cette ligne à notre nouvelle ligne Z.
    for i in range(len(types)):
        signe = types[i]
        ligne_actuelle = i + 1 # +1 car la ligne 0 c'est Z
        
        if signe == ">=" or signe == "=":
            # On soustrait chaque élément de la ligne à la ligne Z
            for j in range(colonnes):
                tableau[0][j] = tableau[0][j] - tableau[ligne_actuelle][j]

    print("\nTableau préparé pour la Phase 1 (Fausse ligne Z) :")
    afficher_tableau(tableau)
    
    # On lance le moteur sur ce faux problème !
    print("\nRésolution de la Phase 1 ---")
    executer_phase_2(tableau, variables_en_base)

    valeur_phase_1 = tableau[0][-1]
    # Si la valeur est négative (en dessous de -0.00001 pour ignorer les micro-erreurs d'arrondi)
    if valeur_phase_1 < -1e-5: 
        print("\nERREUR : Problème INFAISABLE.")
        print("Il est impossible de respecter toutes ces contraintes en même temps.")
        return False, vraie_ligne_z
        
    print("\nPhase 1 réussie ! Les variables artificielles ont été éliminées.")
    return True, vraie_ligne_z

def afficher_graphe_2d(A, b, types, x1_val, x2_val):
    """Génère un graphique 2D montrant les contraintes, la zone admissible et l'optimum."""
    print("\nGénération du graphique en cours...")
    
    # Déterminer la taille de la fenêtre (un peu plus grande que les points clés)
    max_val = max(10, x1_val * 1.5, x2_val * 1.5)
    for i in range(len(b)):
        if A[i][0] > 0: max_val = max(max_val, (b[i] / A[i][0]) * 1.2)
        if A[i][1] > 0: max_val = max(max_val, (b[i] / A[i][1]) * 1.2)
        
    # Créer une grille de points pour colorier la zone admissible
    x = np.linspace(0, max_val, 400)
    y = np.linspace(0, max_val, 400)
    X, Y = np.meshgrid(x, y)
    
    zone_admissible = np.ones_like(X, dtype=bool)
    
    # Appliquer chaque contrainte sur la grille
    for i in range(len(b)):
        a1, a2 = A[i]
        if types[i] == "<=":
            zone_admissible = zone_admissible & (a1 * X + a2 * Y <= b[i])
        elif types[i] == ">=":
            zone_admissible = zone_admissible & (a1 * X + a2 * Y >= b[i])
        elif types[i] == "=":
            # Pour l'égalité, on trace une "bande" très fine sur la grille
            zone_admissible = zone_admissible & (abs(a1 * X + a2 * Y - b[i]) < max_val * 0.01)

    plt.figure(figsize=(8, 6))
    
    # Colorier la zone admissible en vert transparent
    plt.imshow(zone_admissible.astype(int), extent=(0, max_val, 0, max_val), origin="lower", cmap="Greens", alpha=0.3)
    
    # Tracer les droites des contraintes
    x_ligne = np.linspace(0, max_val, 400)
    for i in range(len(b)):
        a1, a2 = A[i]
        if a2 != 0:
            y_ligne = (b[i] - a1 * x_ligne) / a2
            plt.plot(x_ligne, y_ligne, label=f'Contrainte {i+1} ({types[i]} {b[i]})')
        else:
            plt.axvline(x=b[i]/a1, label=f'Contrainte {i+1} ({types[i]} {b[i]})')
            
    # Placer un gros point rouge sur la solution optimale
    plt.plot(x1_val, x2_val, 'ro', markersize=8, label=f'Optimum ($x_1$={x1_val:.2f}, $x_2$={x2_val:.2f})')
    
    plt.xlim(0, max_val)
    plt.ylim(0, max_val)
    plt.xlabel("$x_1$")
    plt.ylabel("$x_2$")
    plt.title("Polygone des solutions admissibles")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    
    print("Le graphique a été généré ! \nFermez la fenêtre du graphique pour terminer le programme.")
    plt.show()