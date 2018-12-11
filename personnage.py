# coding: utf-8
#zpreoiuhzperoih

import pygame as py
from pygame.locals import *

from constantes import *

class Personnage():

	"""
		Classe permettant de créer le personnage du joueur
	"""

	def __init__(self, spawn_joueur, liste_obstacles, type_joueur):
				
		"""
				Constructeur de la classe Personnage
		"""

		self.tileset = py.image.load("data/images/characters/personnages.png").convert_alpha() #On charge le tileset du personnage
		self.pos = spawn_joueur #La variable position du joueur est de type rect. Par défaut, la position d'une image est (0,0)
		self.nb_fireball = 3 #Nombre de boule feu du joueur
		self.type_fireball = 0 #Type de boule de feu (0: Normale - 1: Bleue)

		if type_joueur == 1: #Si c'est le joueur 1
			self.liste_images = [
			[py.Rect(3*32, 0, 32, 32), py.Rect(4*32, 0, 32, 32), py.Rect(5*32, 0, 32, 32)],
			[py.Rect(3*32, 1*32, 32, 32), py.Rect(4*32, 1*32, 32, 32), py.Rect(5*32, 1*32, 32, 32)],
			[py.Rect(3*32, 2*32, 32, 32), py.Rect(4*32, 2*32, 32, 32), py.Rect(5*32, 2*32, 32, 32)],
			[py.Rect(3*32, 3*32, 32, 32), py.Rect(4*32, 3*32, 32, 32), py.Rect(5*32, 3*32, 32, 32)]
			]
		else: #Si c'est le joueur 2
			self.liste_images = [
			[py.Rect(9*32, 0, 32, 32), py.Rect(10*32, 0, 32, 32), py.Rect(11*32, 0, 32, 32)],
			[py.Rect(9*32, 1*32, 32, 32), py.Rect(10*32, 1*32, 32, 32), py.Rect(11*32, 1*32, 32, 32)],
			[py.Rect(9*32, 2*32, 32, 32), py.Rect(10*32, 2*32, 32, 32), py.Rect(11*32, 2*32, 32, 32)],
			[py.Rect(9*32, 3*32, 32, 32), py.Rect(10*32, 3*32, 32, 32), py.Rect(11*32, 3*32, 32, 32)]
			]

		self.image_en_cours = self.liste_images[2][1] #On définit une première image par défaut

		self.liste_obstacles = liste_obstacles #Variable contenant la liste des obstacles

		self.direction = 0
		self.indice_image = 0



	def collision(self, direction):

		"""
			Méthode permettant de tester la collision entre
			le joueur et un obstacle
		"""

		if direction == GAUCHE: #Lorsque le joueur va à gauche
			hitbox_test = self.pos.move(-VITESSE,0) #On crée la variable hitbox_text qui prend comme coordonné celle du perso avec -1 pixel en abscisse

		elif direction == DROITE:
			hitbox_test = self.pos.move(VITESSE,0) 

		elif direction == HAUT:
			hitbox_test = self.pos.move(0,-VITESSE)

		else:
			hitbox_test = self.pos.move(0,VITESSE)

		
		test_collision = False

		for mur in self.liste_obstacles: 
			if hitbox_test.colliderect(mur): #Si il y a collision entre la hitbox_test et un mur
				test_collision = True #test_collision est vrai

		if test_collision: #Si test_collision est vrai
			return True #Il y a collision
		else:
			return False #Il n'y a pas collision

	def deplacer(self, direction, prisme):

		"""
			Méthode permettant de déplacer le joueur
		"""

		self.direction = direction

		if direction == GAUCHE: #lorsque le joueur va à gauche
			if not self.collision(GAUCHE): #Si il n'y a pas collision
				self.pos = self.pos.move(-VITESSE,0) #On déplace le joueur de 1 pixel
		elif direction == DROITE:
			if not self.collision(DROITE):
				self.pos = self.pos.move(VITESSE,0)
		elif direction == HAUT:
			if not self.collision(HAUT):
				self.pos = self.pos.move(0,-VITESSE)
		else:
			if not self.collision(BAS):
				self.pos = self.pos.move(0,VITESSE)


	def update_orientation(self, direction):

		"""
			Méthode permettant de changer la direction de l'image du personnage
		"""

		self.image_en_cours = self.liste_images[direction][self.indice_image] #On choisit une autre image


	def update(self):

		"""
			Méthode mettant à jour l'image du joueur
		"""

		self.image_en_cours = self.liste_images[self.direction][self.indice_image] #On modifie la valaur de image_en_cours
		if self.indice_image >= 2: #Lorsque l'indice_image est > ou = à 3
			self.indice_image = 0 #On lui donne la valeur 0
		else: #Sinon
			self.indice_image += 1 #On l'incrémente de 1