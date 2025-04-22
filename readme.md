# 🎮🎮🎮 Gemgem 🎮🎮🎮 - Un clone de Bejeweled

**Auteur** : ALAIN GILDAS NGUEUDJANG DJOMO  
**Contact** : alain.ng.tech@gmail.com  
**Licence** : BSD Simplifiée  


## Description

**Gemgem** est un jeu de puzzle inspiré du célèbre jeu **Bejeweled**. L'objectif est d'aligner trois gemmes ou plus de la même couleur pour les faire disparaître et marquer des points. Le jeu propose plusieurs niveaux de difficulté, des animations fluides, des effets sonores, et une musique de fond pour une expérience immersive.


## Fonctionnalités

- **Plusieurs niveaux de difficulté** : Facile, Moyen, Difficile.
- **Système de niveaux** : Passez au niveau supérieur en atteignant un certain score.
- **Suggestions de mouvements** : Si vous êtes bloqué, le jeu vous suggère un mouvement possible.
- **Pause** : Mettez le jeu en pause à tout moment pour reprendre plus tard.
- **Effets sonores et musique** : Des sons pour les combinaisons réussies, les mauvais échanges, et une musique de fond relaxante.
- **Timer** : Un temps limité pour chaque niveau, ajoutant un défi supplémentaire.


## Règles du jeu

1. **Alignez les gemmes** : Échangez deux gemmes adjacentes pour aligner trois gemmes ou plus de la même couleur.
2. **Marquez des points** : Chaque combinaison de gemmes vous rapporte des points. Plus vous alignez de gemmes, plus vous gagnez de points.
3. **Passez au niveau supérieur** : Atteignez un score spécifique pour débloquer le niveau suivant.
4. **Évitez les mauvais échanges** : Si un échange ne forme pas de combinaison, les gemmes reviennent à leur position initiale.
5. **Gestion du temps** : Vous avez un temps limité pour atteindre le score requis. Si le temps s'écoule, la partie est terminée.


## Contrôles

- **Souris** :
  - **Clic gauche / Clic droit** : Sélectionnez et Échangez deux gemmes adjacentes.
- **Clavier** :
  - **ESPACE** : Mettre le jeu en pause.
  - **ÉCHAP** : Quitter le jeu.
  - **BACKSPACE** : Recommencer la partie.


## Installation

### Prérequis

- **Python 3.x** : Assurez-vous d'avoir Python installé sur votre système.
- **Pygame** : Le jeu utilise la bibliothèque Pygame pour la gestion des graphismes et des sons.

### Étapes d'installation

1. **Téléchargez le code source** :
   - Clonez ce dépôt ou téléchargez le fichier ZIP.
      `git clone https://github.com/LienNonDisponible/gemgem.git`

2. **Installez Pygame** :
   - Si vous n'avez pas encore Pygame installé, vous pouvez l'installer via pip :
      `pip install pygame`


3. **Téléchargez les ressources** :
   - Assurez-vous que les fichiers suivants sont présents dans le dossier du jeu :
     - `gem1.png`, `gem2.png`, ..., `gem7.png` (les images des gemmes).
     - `badswap.wav`, `match0.wav`, ..., `match5.wav` (les effets sonores).
     - `back.mp3` (la musique de fond).
     - `back.jpg` (l'image de fond du menu).

4. **Lancez le jeu** :
   - Exécutez le fichier `gem.py` pour démarrer le jeu :
      `python gem.py`


## Structure du projet

- **gem.py** : Le fichier principal du jeu, contenant toute la logique et les fonctions.
- **gem1.png, gem2.png, ..., gem7.png** : Les images des gemmes.
- **badswap.wav, match0.wav, ..., match5.wav** : Les effets sonores.
- **back.mp3** : La musique de fond.
- **back.jpg** : L'image de fond du menu.


## Fonctionnalités techniques

- **Gestion des animations** : Les gemmes sont animées lors des échanges et des chutes.
- **Gestion des sons** : Des sons sont joués lors des combinaisons, des mauvais échanges, et des passages de niveau.
- **Gestion des niveaux** : Le jeu propose plusieurs niveaux de difficulté avec des paramètres ajustables (vitesse des animations, taille du plateau, etc.).
- **Système de pause** : Le jeu peut être mis en pause à tout moment, avec un écran de pause dédié.
- **Suggestions de mouvements** : Si le joueur est bloqué, le jeu suggère un mouvement possible.


## Améliorations possibles

- **Mode multijoueur** : Ajouter un mode où deux joueurs peuvent s'affronter.
- **Niveaux supplémentaires** : Ajouter des niveaux avec des objectifs spécifiques (ex : atteindre un score en un temps limité).
- **Effets visuels supplémentaires** : Ajouter des effets visuels lors des combinaisons (explosions, etc.).
- **Sauvegarde de progression** : Permettre au joueur de sauvegarder sa progression et de reprendre plus tard.


## Licence

Ce projet est distribué sous la licence **BSD Simplifiée**. Vous êtes libre de l'utiliser, de le modifier et de le redistribuer, à condition de conserver la notice de licence originale.


## Contact

Pour toute question, suggestion ou problème, n'hésitez pas à me contacter :  
**ALAIN GILDAS NGUEUDJANG DJOMO**  
**Email** : alain.ng.tech@gmail.com  
**GitHub** : [NG ALAIN](https://github.com/ALAIN-NG)

**Amusez-vous bien avec Gemgem !** 🎮