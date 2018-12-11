import pygame as py
from pygame.locals import *

from constantes import *

class Interface():

	"""
		Classe permettant de créer l'interface de vie du boss
	"""

	def __init__(self):
		"""
			Méthode constructeur de la classe Interface
		"""
		self.perso = py.image.load("data/images/characters/personnages.png").convert_alpha() #On charge le tileset des personnages
		self.cadre = py.Surface((200, 45)) #On crée un cadre derrière la barre de vie
		self.cadre.set_alpha(200)

	def update(self, fenetre, boss):
		"""
			Méthode permettant de mettre à jour la barre de vie du boss
		"""

		nb_pv = boss.pv #On récupère les PVs actuels du boss
		pv_max = boss.pv_max #On récupère son nombre de PVs maximum

		image_boss = boss.liste_images[0][1] #On choisit l'image du boss de face

		self.barre_vie = py.Surface((nb_pv*150/100, 32)) #On crée une barre de vie ayant une largeur égale à son nombre de PVs

		if nb_pv > (pv_max*50/100): #Si la vie du boss est supérieure à 50%
			self.barre_vie.fill(VERT) #La barre est verte
		elif nb_pv > (pv_max*10/100): #Si la vie du boss est entre 50% et 10%
			self.barre_vie.fill(ORANGE) #La barre est orange
		else:
			self.barre_vie.fill(ROUGE) #Si sa vie est inférieure à 10%, la barre est rouge

		fenetre.blit(self.cadre, (855, 593))
		fenetre.blit(self.perso, (860, 600), image_boss)
		fenetre.blit(self.barre_vie, (900, 600))