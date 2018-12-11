# coding: utf-8

#Ce fichier contient toutes les constantes du jeu

NB_TILES_X = 15 #Nombre de tile en abscisse dans le tileset
NB_TILES_Y = 15 #Nombre de tile en ordonnée dans le tileset

NB_BLOCS_X = 35 #Le nombre de blocs en abscisse
NB_BLOCS_Y = 20 #Le nombre de blocs en ordonnée

TAILLE_SPRITE = 32 #La taille de tous les sprites du jeu

FENETRE_X = NB_BLOCS_X * TAILLE_SPRITE #La largeur (en px) de la fenêtre
FENETRE_Y = NB_BLOCS_Y * TAILLE_SPRITE #La hauteur (en px) de la fenêtre

(BAS, GAUCHE, DROITE, HAUT)          = range(4) #On crée 4 constantes avec des valeurs arbitraires
(NORMAL, VERT, CHIEN, GARDIEN, BOSS) = range(5) #On crée 5 constantes avec des valeurs arbitraires
(DEBUT, FIN)                         = range(2) #On crée 2 constantes avec des valeurs arbitraires

VITESSE      = 1 #Vitesse du joueur
VITESSE_MOB  = 1 #Vitesse du mob
VITESSE_BOSS = 2 #Vitesse du boss

COEF_ZOOM = 3 #Coefficient de zoom de l'apercu de l'éditeur

DEGATS_FIREBALL = 1 #Nombre de pv que retirent les boules de feu

FICHIER_PSEUDO = "data/joueur.txt"

#On crée des couleurs
NOIR   = (0, 0, 0)
BLANC  = (255, 255, 255)
VERT   = (0, 255, 0)
ORANGE = (255, 126, 0)
ROUGE  = (255, 0, 0)