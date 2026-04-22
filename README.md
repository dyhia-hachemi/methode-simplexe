# Solveur Simplexe & Méthode des Deux Phases (avec Visualisation 2D)

Ce projet est un outil interactif et complet de Recherche Opérationnelle écrit en Python. Il permet de résoudre des problèmes d'optimisation linéaire en utilisant l'algorithme du Simplexe et la méthode des Deux Phases, tout en détaillant de manière pédagogique chaque étape du calcul.

---

## Fonctionnalités

- **Maximisation & Minimisation** : Prise en charge des deux types d'optimisation.
- **Contraintes mixtes** : Supporte les inégalités (`<=`, `>=`) et les égalités (`=`).
- **Méthode des Deux Phases Automatique** : Détecte la nécessité d'ajouter des variables artificielles et gère la Phase 1 de manière autonome pour trouver une solution de base réalisable avant de lancer la Phase 2.
- **Affichage Pédagogique (Pas-à-pas)** : Affiche proprement les tableaux du Simplexe à chaque itération, en précisant la variable entrante, la variable sortante, le pivot et la solution de base courante.
- **Visualisation Graphique 2D** : Pour les problèmes à 2 variables de décision (x1 et x2), le programme génère un graphique traçant les droites de contraintes, coloriant le polygone des solutions admissibles, et pointant la solution optimale.

---

## Prérequis et Installation

Pour faire fonctionner ce programme, vous devez avoir **Python 3.x** installé sur votre machine, ainsi que les bibliothèques scientifiques standards.

1. Clonez ce dépôt ou téléchargez le fichier source `simplexe.py`.
2. Ouvrez un terminal et installez les dépendances requises :

```bash
pip install numpy matplotlib

## 🚀 Utilisation

Lancez simplement le script Python depuis votre terminal : python simplexe.py

Laissez-vous guider par l'interface interactive. Voici comment se déroule une saisie typique : - Choisissez le type d'optimisation (max ou min). - Entrez le nombre de variables de décision. - Saisissez les coefficients de la fonction objectif (espacés par un espace). - Entrez le nombre de contraintes. - Pour chaque contrainte, entrez les coefficients, le signe (<=, >=, =), puis le membre de droite.

## 📝 Auteur

Hachemi Dyhia

Projet réalisé dans le cadre de l'étude de l'optimisation linéaire et de la recherche opérationnelle.
```
