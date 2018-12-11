#coding : utf-8

import pygame as py
from pygame.locals import *

from constantes import *

class Fireball():

	"""
		Méthode permettant de créer des boules de feu
	"""

	def __init__(self, info_joueur):

		if info_joueur.type_fireball == 0:
			self.image = py.image.load("data/images/fireball1.png").convert_alpha() #On importe l'image de la boule de feu
		else:
			self.image = py.image.load("data/images/fireball2.png").convert_alpha() #On importe l'image de la boule de feu bleue

		self.image_droite = py.transform.rotate(self.image, 90) #On effectue une rotation de l'image de 90°
		self.image_gauche = py.transform.rotate(self.image, -90)
		self.image_haut = py.transform.rotate(self.image, 180)


		self.pos = info_joueur.pos #On définit sa position comme celle du joueur
		self.direction = info_joueur.direction #On définit sa direction comme celle du joueur

	def update(self):

		if self.direction == GAUCHE: #Si le joueur est tourné vers la gauche
			self.image = self.image_gauche #On choisit l'image appropriée
			self.pos = self.pos.move(-(VITESSE+1),0) #On déplace la boule de feu

		elif self.direction == DROITE:
			self.image = self.image_droite
			self.pos = self.pos.move(VITESSE+1,0)

		elif self.direction == HAUT:
			self.image = self.image_haut
			self.pos = self.pos.move(0,-(VITESSE+1))

		else:
			self.pos = self.pos.move(0,VITESSE+1)