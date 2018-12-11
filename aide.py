import pygame as py
from pygame.locals import *

from constantes import *

class Dialog_aide():

	"""
		Classe permettant d'afficher le dialogue d'aide
	"""

	def __init__(self):
		"""	
			Constructeur de la classe Dialog_aide
		"""

		py.font.init() #On initialise le module d'écriture

		#On crée deux polices
		self.font  = py.font.Font(None, 24)
		self.font2 = py.font.Font(None, 17)

		self.fenetre = py.display.set_mode((FENETRE_X, FENETRE_Y), DOUBLEBUF) #On crée la fenêtre Pygame

		self.background_guide = py.image.load("data/images/characters/aide_joueur.jpg").convert() #On charge l'image de fond
		self.background_guide = py.transform.scale(self.background_guide, (FENETRE_X, FENETRE_Y))

		ZOOM = 5

		self.fenetre.blit(self.background_guide, (0,0))

		py.display.flip()

		#On crée toutes les répliques
		self.phrase1  = "Bien le bonjour Aventurier !\nJe suis Lexa, c'est moi qui vais t'accompagner tout au long\nde ta quête."
		self.phrase2  = "Je vais te guider et t'apprendre les rudiments\nde ce monde implacable. Tu vas devoir récupérer six cristaux\ndivins à travers des donjons."
		self.phrase3  = "Pour se faire, tu vas devoir utiliser\nles flèches directionnelles afin de te déplacer. Si tu croises\nles forces du mal, tu peux utiliser tes pouvoirs divins."
		self.phrase4  = "Pour cela, appuie sur la barre espace . Mais attention !\nTon pouvoir est limité ! Tu ne peux lancer que 3 boules de feu !\n\nDurant ton périple, tu rencontreras différents éléments,\nhostiles ou non."
		self.phrase5  = "Si tu croises un symbole comme celui-ci, fais attention.\nC'est ici que naissent les forces du mal. Tu peux cependant\npasser dessus sans crainte."
		self.phrase6  = "Ce symbole-ci représente l'endroit où tu débutes dans le donjon."
		self.phrase7  = "C'est la porte de sortie du donjon, elle s'ouvrira automatiquement\nquand tu récupéreras le prisme ou bien quand tu actionnera\nun levier."
		self.phrase8  = "Ces prismes sont ton objectif principal. Tu dois les\nrécupérer afin de sortir du donjon. L'obtention des 6 prismes\nva te permettre de vaincre le seigneur des forces\ndu mal."
		self.phrase9  = "Au cours de ton exploration des donjons, tu trouveras ces leviers.\nLes activer te permettra d'ouvrir la porte te menant au prochain\nétage du donjon."
		self.phrase10 = "Je pense avoir fais le tour... À toi de jouer maintenant !"

		#On importe toutes les images et on les remdimensionne
		self.image_crane   = py.image.load("data/images/skull.png").convert_alpha()
		self.image_crane   = py.transform.scale(self.image_crane, (self.image_crane.get_width()*ZOOM, self.image_crane.get_height()*ZOOM))

		self.image_spawn   = py.image.load("data/images/spawn_joueur.png").convert_alpha()
		self.image_spawn   = py.transform.scale(self.image_spawn, (self.image_spawn.get_width()*ZOOM, self.image_spawn.get_height()*ZOOM))

		self.image_porte   = py.image.load("data/images/porte.png").convert_alpha()
		self.image_porte   = py.transform.scale(self.image_porte, (self.image_porte.get_width()*ZOOM, self.image_porte.get_height()*ZOOM))

		self.image_levier  = py.image.load("data/images/levier.png").convert_alpha()
		self.image_levier  = py.transform.scale(self.image_levier, (self.image_levier.get_width()*ZOOM, self.image_levier.get_height()*ZOOM))

		self.image_prisme  = py.image.load("data/images/prisme.png").convert_alpha()
		self.image_prisme  = py.transform.scale(self.image_prisme, (self.image_prisme.get_width()*ZOOM, self.image_prisme.get_height()*ZOOM))

		self.image_touches = py.image.load("data/images/touches.png").convert_alpha()

		self.image_espace  = py.image.load("data/images/spacebar.png").convert_alpha()
		self.image_espace  = py.transform.scale(self.image_espace, (self.image_espace.get_width()*2, self.image_espace.get_height()*2))

		self.image_continuer = py.image.load("data/images/press_spacebar.png").convert_alpha()


	def afficher (self, phrase):
		"""
			Méthode permettant d'afficher une réplique
		"""

		liste_phrase = phrase.split("\n") #On découpe la phrase à chaque retour à la ligne		
		x = 0
		y = FENETRE_Y - 100

		#On affiche lettre par lettre le texte
		for ligne in liste_phrase:
			for lettre in ligne:
				for event in py.event.get():
					pass
				text = self.font.render(lettre,1,BLANC)
				pos_text = text.get_rect()
				self.fenetre.blit(text, (15+x, y))
				py.display.flip()

				x += pos_text.left + text.get_width() + 2

				if lettre != ".":
					py.time.wait(10)
				else:
					py.time.wait(400)
			x=0
			y+=20

			if ligne == "":
				py.time.wait(800)

		texte_espace = self.font2.render("Appuyez sur n'importe quelle touche pour continuer...",1,BLANC)
		self.fenetre.blit(texte_espace, (FENETRE_X - texte_espace.get_width() - 20, FENETRE_Y - texte_espace.get_height() - 5))
		py.display.flip()

		self.fenetre.blit(self.background_guide, (0,0))


		#On attend que le joueur appuie sur une touche pour continuer
		suivant = False
		while not suivant:
			for event in py.event.get():
				if event.type == KEYDOWN:
					suivant = True

	def afficher_aide_joueur(self):
		"""
			Méthode permettant d'afficher l'ensemble du dialogue
		"""

		self.afficher(self.phrase1)
		self.afficher(self.phrase2)
		self.fenetre.blit(self.image_touches, (200, 200))
		self.afficher(self.phrase3)
		self.fenetre.blit(self.image_espace, (150, 225))
		self.afficher(self.phrase4)
		self.fenetre.blit(self.image_crane, (200, 200))
		self.afficher(self.phrase5)
		self.fenetre.blit(self.image_spawn, (200, 200))
		self.afficher(self.phrase6)
		self.fenetre.blit(self.image_porte, (200, 125))
		self.afficher(self.phrase7)
		self.fenetre.blit(self.image_prisme, (200, 200))
		self.afficher(self.phrase8)
		self.fenetre.blit(self.image_levier, (200, 200))
		self.afficher(self.phrase9)
		self.afficher(self.phrase10)

		py.display.quit()