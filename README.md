# first
# Jeu Pokémon en Pygame

Ce projet est une implémentation simple d'un jeu de combat Pokémon en Python, utilisant la bibliothèque Pygame. Il permet au joueur de choisir un Pokémon et de participer à des combats contre des adversaires aléatoires. Les statistiques des Pokémon sont sauvegardées et chargées depuis un fichier texte.

## Fonctionnalités

* **Menu Principal :** Permet de naviguer entre les différentes sections du jeu (Jouer, Statistiques, Quitter).
* **Sélection de Pokémon :** Le joueur peut choisir parmi une liste de Pokémon disponibles (Salamèche, Carapuce, Bulbizarre).
* **Combats :** Des combats au tour par tour où le joueur peut attaquer ou se soigner (nombre limité de soins).
* **Statistiques :** Affichage des statistiques des Pokémon, incluant le nombre de victoires.
* **Sauvegarde des Statistiques :** Les statistiques des Pokémon (force, PV, victoires) sont sauvegardées dans un fichier (`pokemon_stats.txt`).
* **Interface Graphique :** Utilisation de Pygame pour une interface utilisateur graphique.



1.  **Prérequis :**
    * Python 3.x
    * Pygame 


## Utilisation

* **Menu Principal :**
    * **Jouer :** Commence une nouvelle partie et permet de choisir un Pokémon.
    * **Statistiques :** Affiche les statistiques des Pokémon.
    * **Quitter :** Ferme le jeu.

* **Sélection de Pokémon :**
    * Cliquez sur le nom du Pokémon pour le choisir et commencer le combat.
    * Utilisez le bouton "Back" pour revenir au menu principal.

* **Combat :**
    * Cliquez sur "Attaque" pour attaquer l'adversaire.
    * Cliquez sur "Soigner" pour restaurer les PV de votre Pokémon (limité à 3 fois).
    * Le combat se termine lorsqu'un des Pokémon atteint 0 PV.
    * Utilisez le bouton "Back" pour revenir au menu principal.

* **Statistiques :**
    * Affiche le nom, le type, la force, les PV et le nombre de victoires de chaque Pokémon.
    * Utilisez le bouton "Back" pour revenir au menu principal.

## Structure du Code

Le code est organisé en plusieurs classes :

* `Button` :  Définit les boutons interactifs.
* `Pokemon` :  Représente un Pokémon avec ses attributs (nom, image, force, type, PV).
* `MainMenu` :  Gère le menu principal du jeu.
* `GameWindow` :  Permet au joueur de choisir un Pokémon.
* `SettingsWindow` :  Affiche les statistiques des Pokémon.
* `combatWindow` :  Gère les combats Pokémon.
* `GameApp` :   L'application principale qui gère les différentes fenêtres du jeu.

## Fichiers

* `Jeux pokémon.py` : Le code source principal du jeu.
* `pokemon_stats.txt` :  Fichier texte qui stocke les statistiques des Pokémon.
* `pokeball.png` :  Icône du jeu.
* `S.png`, `C.png`, `B.png` :  Images des Pokémon (Salamèche, Carapuce, Bulbizarre).

## Améliorations Possibles

* Ajouter plus de Pokémon.
* Implémenter différents types d'attaques.
* Améliorer l'interface utilisateur.
* Ajouter des animations.
* Gérer la difficulté du jeu.
* Ajouter une bande-son et des effets sonores.




