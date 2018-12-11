# coding: utf-8

import pygame as py
from pygame.locals import *

from math import floor

import pickle

from constantes import *
from bots import *
from boutons import *


class Carte():

	"""
		Classe permettant de créer la carte
	"""

	def __init__(self):
		"""
			Constructeur de la classe Carte
		"""

		self.structure = [[]] #On crée la structure de la carte sous forme d'une liste à deux dimensions
		self.tileset_map = py.image.load("data/images/map/tileset.png").convert_alpha() #On importe le tileset qui contiendra les images de notre map
		self.crane2 = py.image.load("data/images/skull2.png").convert_alpha()

		self.fichier = "" #La variable fichier contiendra le nom de la carte
		self.liste_obstacles = [] #Liste contenant les positions de tous les obstacles
		self.position_portes = [] #Garde en mémoire la position des portes
		self.prisme = [] #Variable contenant la position du ou des prisme
		self.levier = 0 #Variable contenant la position du levier
		self.get_prisme = False #Booléen indiquant si le joueur à récupéré le prisme ou non
		self.get_levier = False #Booléen indiquant si le joueur est en contact avec le levier
		self.action_levier = False #Booléen indiquant l'effet que doit avoir le levier

		self.spawn_joueur = 0 #Variable contenant la position du spawn joueur
		self.spawn_joueur2 = 0 #Variable ontenant la position du spawn du joueur 2
		self.spawn_normal = [] #Liste contenant la position des spawnw PNJ normaux
		self.spawn_vert = [] #Liste contenant la position des spawn PNJ verts
		self.spawn_chien = [] #Liste contenant la position des spawn PNJ chiens
		self.spawn_gardien = [] #Liste contenant la position des spawn PNJ gardien
		self.spawn_boss = [] #Liste contenant la position des spawn PNJ boss
		self.liste_bots = []

	def charger(self, fichier):
		"""
			Méthode chargeant la carte depuis un fichier cible
		"""

		try:
			with open(fichier, "rb") as fichier_carte: #On essai d'ouvrir le fichier
					self.structure = pickle.load(fichier_carte) #On charge la structure depuis le fichier	

		except: #Si on ne peut pas ouvrir le fichier
			self.structure = [[-1] * NB_BLOCS_X for _ in range(NB_BLOCS_Y)] #Si la carte ne parvient pas à être charger tous les blocs prendront la valeur -1 (vide)

		self.fichier = fichier


		for j in range(len(self.structure)): #j allant de 0 -> Nombre de lignes
			for i in range(len(self.structure[0])): #i allant 0 -> Longueur de la ligne (On envoi prend uniquement la longueur de la première ligne car toutes les lignes sont de tailles égales)

				case = self.structure[j][i] #Simplie l'écriture

				if case == -5: #Si on trouve le spawn du joueur 2
					self.spawn_joueur2 = py.Rect(i*TAILLE_SPRITE, j*TAILLE_SPRITE, TAILLE_SPRITE, TAILLE_SPRITE) #On ajoute le rect à la liste des spawns

				elif 0 <= case < 219 and case != 82: #Si on trouve un obstacle
					if case == 80:
						self.position_portes.append((j,i))
					elif case == 81:
						self.position_portes.append((j,i))
					self.liste_obstacles.append(py.Rect(i*TAILLE_SPRITE, j*TAILLE_SPRITE, TAILLE_SPRITE, TAILLE_SPRITE)) #On ajoute le rect à la liste des obstacles

				elif 219 <= case <= 224: #Si on trouve un prisme
					self.prisme.append(py.Rect(i*TAILLE_SPRITE, j*TAILLE_SPRITE, TAILLE_SPRITE, TAILLE_SPRITE)) #On définit sa position		
				
				elif case == 225: #Si on trouve le spawn du joueur
					self.spawn_joueur = py.Rect(i*TAILLE_SPRITE, j*TAILLE_SPRITE, TAILLE_SPRITE, TAILLE_SPRITE) #On défini sa position par un rect

				elif case == 226: #Si on trouve un spawn de PNJ normal
					self.spawn_normal.append(py.Rect(i*TAILLE_SPRITE, j*TAILLE_SPRITE, TAILLE_SPRITE, TAILLE_SPRITE)) #On ajoute le rect à la liste des spawns

				elif case == 227: #Si on trouve un spawn de PNJ vert
					self.spawn_vert.append(py.Rect(i*TAILLE_SPRITE, j*TAILLE_SPRITE, TAILLE_SPRITE, TAILLE_SPRITE)) #On ajoute le rect à la liste des spawns

				elif case == 228: #Si on trouve un spawn de PNJ gardien
					self.spawn_gardien.append(py.Rect(i*TAILLE_SPRITE, j*TAILLE_SPRITE, TAILLE_SPRITE, TAILLE_SPRITE)) #On ajoute le rect à la liste des spawns

				elif case == 229: #Si on trouve un spawn de PNJ chien
					self.spawn_chien.append(py.Rect(i*TAILLE_SPRITE, j*TAILLE_SPRITE, TAILLE_SPRITE, TAILLE_SPRITE))

				elif case == 82:
					self.spawn_boss.append(py.Rect(i*TAILLE_SPRITE, j*TAILLE_SPRITE, TAILLE_SPRITE, TAILLE_SPRITE))

				elif 230 <= case <= 235 :#Si on trouve un levier
					self.levier = py.Rect(i*TAILLE_SPRITE, j*TAILLE_SPRITE, TAILLE_SPRITE, TAILLE_SPRITE)

		for j in range(len(self.structure)): #j allant de 0 -> Nombre de lignes
			for i in range(len(self.structure[0])): #i allant 0 -> Longueur de la ligne (On envoi prend uniquement la longueur de la première ligne car toutes les lignes sont de tailles égales)

				case = self.structure[j][i]

				if case == 226: #Si on trouve un spawn de PNJ normal
					point_spawn = choice(self.spawn_normal)
					self.spawn_normal.remove(point_spawn)
					self.liste_bots.append(PNJ(point_spawn, self.liste_obstacles, NORMAL)) #On ajoute les PNJ "normaux"
				elif case == 227: #Si on trouve un spawn de PNJ vert
					point_spawn = choice(self.spawn_vert)
					self.spawn_vert.remove(point_spawn)
					self.liste_bots.append(PNJ(point_spawn, self.liste_obstacles, VERT)) #On ajoute les PNJ "verts"
				elif case == 228: #Si on trouve un spawn de PNJ gardien
					point_spawn = choice(self.spawn_gardien)
					self.spawn_gardien.remove(point_spawn)
					self.liste_bots.append(PNJ(point_spawn, self.liste_obstacles, GARDIEN)) #On ajoute les PNJ "gardiens"
				elif case == 229:
					point_spawn = choice(self.spawn_chien)
					self.spawn_chien.remove(point_spawn)
					self.liste_bots.append(PNJ(point_spawn, self.liste_obstacles, CHIEN)) #On ajoute les PNJ "gardiens"
				elif case == 82:
					point_spawn = choice(self.spawn_boss)
					self.spawn_boss.remove(point_spawn)
					self.liste_bots.append(PNJ(point_spawn, self.liste_obstacles, BOSS)) #On ajoute les PNJ "gardiens"

	def afficher(self, fenetre):
		"""
			Méthode affichant la carte

		"""
		x,y = 0,0 #x et y représente les coordonées où seront affichés les blocs
		for j in range(len(self.structure)): #j allant de 0 -> Nombre de lignes
			for i in range(len(self.structure[0])): #i allant 0 -> Longueur de la ligne (On envoi prend uniquement la longueur de la première ligne car toutes les lignes sont de tailles égales)

				case = self.structure[j][i] #Simplifie l'écriture

				if case == -5: #Si on trouve un spawn de PNJ
					fenetre.blit(self.crane2, (x,y)) #On affiche un crâne

				tile = self.get_bloc(self.structure[j][i]) #Permet de cibler le tile adéquat dans l'image "tileset"

				fenetre.blit(self.tileset_map, (x,y), tile) #Affiche le tile sur la fenêtre

				x += TAILLE_SPRITE #On incrémente x de la taille d'un sprite

			y += TAILLE_SPRITE #On incrémente y de la taille d'un sprite
			x = 0 #Puisqu'on change de ligne, on remet x à 0


	########################### EDITEUR ##############################

	def editer(self, event, bloc):
		"""
			Méthode permettant d'éditer un niveau
		"""

		x = floor((event.pos[0] - 350) / TAILLE_SPRITE) #On repère le bloc ciblé en abscisse
		y = floor(event.pos[1] / TAILLE_SPRITE) #On repère le bloc ciblé en ordonnée

		if event.pos[0] >= 345:
			self.structure[y][x] = int(bloc) #On modifie le bloc dans la structure du niveau


	def get_bloc(self, bloc, zoom=1):
		"""
			Méthode permettant de récupérer le bloc séléctionné
		"""

		#Par défaut zoom = 1, on retourne donc l'image taille réelle

		tile = py.Rect(floor(bloc % NB_TILES_X) * TAILLE_SPRITE*zoom, floor(bloc / NB_TILES_Y) * TAILLE_SPRITE*zoom, TAILLE_SPRITE*zoom, TAILLE_SPRITE*zoom) #Permet de cibler le tile adéquat dans l'image "tileset"
		
		return tile

	def copier_bloc(self, event):
		"""
			Méthode permettant de copier le bloc séléctionné
		"""

		x = floor((event.pos[0] - 345)/ TAILLE_SPRITE) #On repère le bloc ciblé en abscisse
		y = floor(event.pos[1]/ TAILLE_SPRITE) #On repère le bloc ciblé en ordonnée

		bloc = self.structure[y][x]

		return bloc

	def reset(self, fenetre):
		"""
			Méthode permettant de reset la carte
		"""

		font = py.font.Font(None, 30) #On crée une police
		texte = font.render("Êtes-vous certain de vouloir reset la carte ?", 1, BLANC) #On crée le texte

		#On crée deux surfaces qui font office de cadre
		border = py.Surface((500, 300))
		dialog = py.Surface((496, 296))

		border.fill(ROUGE)
		dialog.fill((20, 20, 20))

		pos_texte_x = 654 + (dialog.get_width() / 2) - (texte.get_width() / 2) #On place le texte au milieu de la boîte de dialogue
		pos_texte_y = 172 + texte.get_height() + 10

		bt_oui = PyButton(window=fenetre, coord=(704, 300), size=(175,75), color=BLANC, text=("Oui", 24, NOIR)) #On crée un bouton
		bt_non = PyButton(window=fenetre, coord=(925, 300), size=(175,75), color=BLANC, text=("Non", 24, NOIR)) #Idem

		#On affiche le tout
		fenetre.blit(border, (652, 170))
		fenetre.blit(dialog, (654, 172))
		fenetre.blit(texte, (pos_texte_x, pos_texte_y))

		bt_oui.print()
		bt_non.print()

		py.display.flip()

		continuer_dialogue = True
		while continuer_dialogue:
			for event in py.event.get():
				if event.type == QUIT: #Si on appuie sur la croix
					continuer_dialogue = False #On ferme la boîte de dialogue

				if event.type == KEYDOWN: 
					if event.key == K_ESCAPE: #Si on appuie sur ECHAP
						continuer_dialogue = False #On ferme la boîte de dialogue

				if event.type == MOUSEBUTTONDOWN:
					if bt_oui.click(event): #Si il clique sur Oui
						self.structure = [[-1] * NB_BLOCS_X for _ in range(NB_BLOCS_Y)] #On reset la carte
						continuer_dialogue = False #On ferme la boîte de dialogue
					elif bt_non.click(event): #Si il clique sur Non
						continuer_dialogue = False #On ferme la boîte de dialogue



	def sauvegarder(self):
		"""
			Méthode permettant de sauvegarder le niveau en édition
		"""

		with open(self.fichier, "wb") as fichier_carte: #On ouvre le fichier
			pickle.dump(self.structure, fichier_carte) #On le rempli par la nouvelle structure