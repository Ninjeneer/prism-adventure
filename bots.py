# coding: utf-8

import pygame as py
from pygame.locals import *

from random import randrange, choice

from constantes import *

class PNJ():

	"""
		Classe permettant de créer les Personnages Non Joueurs 
	"""

	def __init__(self, point_de_spawn, liste_obstacles, type_bot):

		"""
			Constructeur de la classe PNJ
		"""

		self.tileset = py.image.load("data/images/characters/personnages.png").convert_alpha() #On importe un tileset contenant diverses images
		self.spawn = point_de_spawn #On définit son point de spawn
		self.pos = point_de_spawn
		self.type_bot = type_bot

		

		if type_bot == NORMAL: #Si c'est un bot normal
			self.pv_max = 1
			#On crée une liste d'image à deux dimensions contenant toutes les images du PNJ

			self.liste_images = [
			[py.Rect(6*32, 4*32, 32, 32), py.Rect(7*32, 4*32, 32, 32), py.Rect(8*32, 4*32, 32, 32)],
			[py.Rect(6*32, 5*32, 32, 32), py.Rect(7*32, 5*32, 32, 32), py.Rect(8*32, 5*32, 32, 32)],
			[py.Rect(6*32, 6*32, 32, 32), py.Rect(7*32, 6*32, 32, 32), py.Rect(8*32, 6*32, 32, 32)],
			[py.Rect(6*32, 7*32, 32, 32), py.Rect(7*32, 7*32, 32, 32), py.Rect(8*32, 7*32, 32, 32)]
			]
		elif type_bot == VERT: #Si c'est un bot vert
			self.pv_max = 2
			self.liste_images = [
			[py.Rect(0*32, 0*32, 32, 32), py.Rect(1*32, 0*32, 32, 32), py.Rect(2*32, 0*32, 32, 32)],
			[py.Rect(0*32, 1*32, 32, 32), py.Rect(1*32, 1*32, 32, 32), py.Rect(2*32, 1*32, 32, 32)],
			[py.Rect(0*32, 2*32, 32, 32), py.Rect(1*32, 2*32, 32, 32), py.Rect(2*32, 2*32, 32, 32)],
			[py.Rect(0*32, 3*32, 32, 32), py.Rect(1*32, 3*32, 32, 32), py.Rect(2*32, 3*32, 32, 32)]
			]
		elif type_bot == GARDIEN: #Si c'est un gardien
			self.pv_max = 3
			self.liste_images = [
			[py.Rect(9*32, 4*32, 32, 32), py.Rect(10*32, 4*32, 32, 32), py.Rect(11*32, 4*32, 32, 32), py.Rect(12*32, 4*32, 32, 32)],
			[py.Rect(9*32, 5*32, 32, 32), py.Rect(10*32, 5*32, 32, 32), py.Rect(11*32, 5*32, 32, 32), py.Rect(12*32, 5*32, 32, 32)],
			[py.Rect(9*32, 6*32, 32, 32), py.Rect(10*32, 6*32, 32, 32), py.Rect(11*32, 6*32, 32, 32), py.Rect(12*32, 6*32, 32, 32)],
			[py.Rect(9*32, 7*32, 32, 32), py.Rect(10*32, 7*32, 32, 32), py.Rect(11*32, 7*32, 32, 32), py.Rect(12*32, 7*32, 32, 32)]
			]
		elif type_bot == CHIEN:
			self.pv_max = 1
			self.liste_images = [
			[py.Rect(0*32, 4*32, 32, 32), py.Rect(1*32, 4*32, 32, 32), py.Rect(2*32, 4*32, 32, 32)],
			[py.Rect(0*32, 5*32, 32, 32), py.Rect(1*32, 5*32, 32, 32), py.Rect(2*32, 5*32, 32, 32)],
			[py.Rect(0*32, 6*32, 32, 32), py.Rect(1*32, 6*32, 32, 32), py.Rect(2*32, 6*32, 32, 32)],
			[py.Rect(0*32, 7*32, 32, 32), py.Rect(1*32, 7*32, 32, 32), py.Rect(2*32, 7*32, 32, 32)]
			]
		elif type_bot == BOSS:
			self.pv_max = 100
			self.liste_images = [
			[py.Rect(9*32, 0*32, 32, 32), py.Rect(10*32, 0*32, 32, 32), py.Rect(11*32, 0*32, 32, 32)],
			[py.Rect(9*32, 1*32, 32, 32), py.Rect(10*32, 1*32, 32, 32), py.Rect(11*32, 1*32, 32, 32)],
			[py.Rect(9*32, 2*32, 32, 32), py.Rect(10*32, 2*32, 32, 32), py.Rect(11*32, 2*32, 32, 32)],
			[py.Rect(9*32, 3*32, 32, 32), py.Rect(10*32, 3*32, 32, 32), py.Rect(11*32, 3*32, 32, 32)]
			]

		self.pv = self.pv_max #On définit son nombre de points de vie au maximum

		self.image_en_cours = self.liste_images[2][1] #image en cours prend comme valeur par défault 7*32,5*32

		self.liste_obstacles = liste_obstacles #Variable contenant la liste des obstacles



		self.changer_direction() #On lui donne une direction aléatoire
		self.indice_image = 0 

	def collision(self, direction):
		"""
            Méthode permettant de tester la collision
            du bot avec un obstacle
        """


		if direction == GAUCHE: #Lorsque le bot va à gauche
			hitbox_test = self.pos.move(-VITESSE_MOB,0) #On crée la variable hitbox_text qui prend comme coordonné celle du bot avec -1 pixel en abscisse

		elif direction == DROITE:
			hitbox_test = self.pos.move(VITESSE_MOB,0) 

		elif direction == HAUT:
			hitbox_test = self.pos.move(0,-VITESSE_MOB)

		else:
			hitbox_test = self.pos.move(0,VITESSE_MOB)

		if hitbox_test.left < 0 or hitbox_test.left + hitbox_test.width > FENETRE_X or hitbox_test.top < 0 or hitbox_test.top + hitbox_test.height > FENETRE_Y: #Si le bot sort de la fenêtre
			return True

		
		test_collision = False

		for mur in self.liste_obstacles: 
			if hitbox_test.colliderect(mur): #Si il y a collision entre la hitbox_test et un mur
				test_collision = True #test_collision est vrai

		if test_collision: #Si test_collision est vrai
			return True #Il y a collision
		else:
			return False #Il n'y a pas collision
		

	def changer_direction(self):
		"""
			Méthode permettant de changer la direction du bot
		"""

		self.direction = randrange(0,4) #On change aléatoirement de direction


	def deplacer(self):
		"""
			Méthode déplaçant le bot
		"""

		if self.type_bot == BOSS:
			vitesse = VITESSE_BOSS
		else:
			vitesse = VITESSE_MOB


		if self.direction == GAUCHE: #Lorsque le bot va à gauche
			if not self.collision(GAUCHE): #S'il n'y a pas de collision
				self.pos = self.pos.move(-vitesse,0) #On déplace le bot de 1 pixel
			else: #Sinon
				self.changer_direction() #Il change de direction

		elif self.direction == DROITE:
			if not self.collision(DROITE):
				self.pos = self.pos.move(vitesse,0)
			else:
				self.changer_direction()

		elif self.direction == HAUT:
			if not self.collision(HAUT):
				self.pos = self.pos.move(0,-vitesse)
			else:
				self.changer_direction()
		else:
			if not self.collision(BAS):
				self.pos = self.pos.move(0,vitesse)
			else:
				self.changer_direction()

	def respawn(self):
		"""
			Méthode permettant de faire réapparaître le bot
		"""

		self.pv = self.pv_max #On remet les points de vie du bot au maximum
		self.changer_direction() #On le fait changer de direction
		self.pos = self.spawn #On replace le bot à son point de spawn



	def update(self):
		"""
			Méthode mettant à jour l'image du bot
		"""
		
		#Le nombre de frames varie selon les bots
		if self.type_bot == GARDIEN:
			nb_frame = 4
		else:
			nb_frame = 3

		self.image_en_cours = self.liste_images[self.direction][self.indice_image] #On modifie la valaur de image_en_cours
		if self.indice_image >= nb_frame - 1: #Si on a atteint la frame maximale
			self.indice_image = 0 #On retourne à la première
		else: #Sinon
			self.indice_image += 1 #On l'incrémente de 1