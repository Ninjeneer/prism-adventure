# coding: utf-8

import pygame as py
from pygame.locals import *

from constantes import *
import son


class Prologue():

	"""
		Classe permettant de créer le prologue, les dialogues et l'épilogue
	"""

	def __init__(self, type_prologue):

		"""
			Contructeur de la classe Prologue
		"""

		py.font.init() #On initialise le module d'écriture

		#On crée deux polices
		self.font = py.font.Font(None, 40)
		self.font2 = py.font.Font(None, 24)

		self.type_prologue = type_prologue #On récupère le type que l'on veut afficher (Prologue ou Epilogue)

		self.fenetre = py.display.set_mode((FENETRE_X, FENETRE_Y), DOUBLEBUF) #On crée la fenêtre Pygame
		py.display.set_caption("PRISM ADVENTURE") #On change le titre de la fenêtre

		#On importe et on redimensionne les images utiles
		self.background_debut = py.image.load("data/images/royaume.jpg").convert()
		self.background_trone = py.image.load("data/images/salle_trone.jpg").convert()
		self.background_trone = py.transform.scale(self.background_trone, (FENETRE_X, FENETRE_Y)).convert()
		self.background_fin = py.image.load("data/images/royaume_fin.jpg").convert()
		self.background_fin = py.transform.scale(self.background_fin, (FENETRE_X, FENETRE_Y)).convert()
		self.image_jeu = py.image.load("data/images/titre.png").convert()
		self.image_jeu = py.transform.scale(self.image_jeu, (FENETRE_X, FENETRE_Y)).convert()


		#On blanchit un peu l'écran pour faciliter la lecture
		self.fond_blanc = py.Surface((FENETRE_X, FENETRE_Y))
		self.fond_blanc.fill(BLANC)
		self.fond_blanc.set_alpha(50)

		self.fondu = py.Surface((FENETRE_X, FENETRE_Y)) #Surface permettant de créer des fondus

		#Surface dans laquelle seront affichés les dialogues
		self.zone_texte = py.Surface((FENETRE_X, 105))
		self.zone_texte.set_alpha(200)


		#On récupère le pseudo du joueur pour l'afficher dans les dialogues
		with open("data/joueur.txt") as fichier_joueur:
			pseudo_joueur = fichier_joueur.read()
				  

		#On crée tous les dialogues
		self.dialog1 = "Roi: Moi, roi des Arcadiens et du Royaume des 6 t'ai fais mander en ce jour, héros de notre royaume,\net je suis heureux de voir que tu as répondu à notre appel. Je vais être bref, comme tu le sais déjà,\nles forces d'Arcadia se battent en ce moment même contre les forces du mal.\nTu connais le rôle qui te fut attribué à ta naissance de par les astres qui se penchèrent sur ton berceau.\nLe royaume se tourne donc vers toi et ton pouvoir pour tuer Asmodan, le seigneur des forces du mal."
		self.dialog2 = pseudo_joueur + " : Mon seigneur ?"
		self.dialog3 = "Roi: Pour se faire, tu devras récupérer les 6 cristaux de ce monde afin de renforcer ce pouvoir qui est tiens.\nMais gare à toi, ses soldats parcourent le monde à la recherche de ces cristaux et n'hésiteront pas à te tuer.\nPour mener à bien ta quête, une guide t'accompagnera tout au long de ton périple.\nMaintenant va, et accompli ton destin."

	def afficher_prologue(self):
		"""
			Méthode permettant d'afficher le prologue
		"""

		#On crée le fondu d'ouverture
		for i in range(255):
			if 255 - 3*i > 0:
				self.fondu.set_alpha(255-i*3) #On diminue son opacité petit à petit
			else:
				break

			for event in py.event.get():
				pass
			self.fenetre.blit(self.image_jeu, (0,0))
			self.fenetre.blit(self.fondu, (0,0))
			py.display.flip()
			py.time.wait(30)


		for i in range(255):
			if i*2 < 255:
				self.fondu.set_alpha(i*3) #On augmente son opacité petit à petit
				self.fenetre.blit(self.image_jeu, (0,0))
				self.fenetre.blit(self.fondu, (0,0))
				py.display.flip()
				py.time.wait(30)


		son.charger_musique_prologue()
		son.mixer.music.play()

		#On crée le fondu d'ouverture
		for i in range(255):
			if 255 - 3*i > 0:
				self.fondu.set_alpha(255-i*3) #On diminue son opacité petit à petit
			else:
				break

			self.fenetre.blit(self.background_debut, (0,0))
			self.fenetre.blit(self.fond_blanc, (0,0))
			self.fenetre.blit(self.fondu, (0,0))
			py.display.flip()
			py.time.wait(30)

		texte = py.image.load("data/images/prologue.png").convert_alpha()
		pos_texte = texte.get_rect()

		pos_texte.move_ip(0, FENETRE_Y + 10)

		while pos_texte.bottom > 0: #Tant que le texte n'est pas sorti par le haut de la fenêtre
			for event in py.event.get():
				if event.type == QUIT:
					return 0

			pos_texte = pos_texte.move(0,-1) #On le fait monter
			self.fenetre.blit(self.background_debut, (0,0))
			self.fenetre.blit(self.fond_blanc, (0,0))
			self.fenetre.blit(self.fondu, (0,0))
			self.fenetre.blit(texte, pos_texte)
			py.display.flip()
			py.time.wait(20)

		#On crée un fondu de fermeture
		for i in range(255):
			if i*2 < 255:
				self.fondu.set_alpha(i*3) #On augmente son opacité petit à petit
				self.fenetre.blit(self.background_debut, (0,0))
				self.fenetre.blit(self.fond_blanc, (0,0))
				self.fenetre.blit(self.fondu, (0,0))
				py.display.flip()
				py.time.wait(30)

		son.mixer.music.fadeout(5000)
		

	def afficher_epilogue(self):
		"""
			Méthode permettant d'afficher l'épilogue
		"""
		#On crée un fondu d'ouverture
		for i in range(255):
			if 255 - 3*i > 0:
				self.fondu.set_alpha(255-i*3) #On diminue son opacité petit à petit
			else:
				break

			self.fenetre.blit(self.background_fin, (0,0))
			self.fenetre.blit(self.fond_blanc, (0,0))
			self.fenetre.blit(self.fondu, (0,0))
			py.display.flip()
			py.time.wait(30)

		texte = py.image.load("data/images/epilogue.png").convert_alpha()
		pos_texte = texte.get_rect()

		pos_texte.move_ip(0, FENETRE_Y + 10)
		son.charger_musique_epilogue()
		son.mixer.music.play()

		while pos_texte.bottom > 0: #Même chose que pour le prologue
			for event in py.event.get():
				if event.type == QUIT:
					for i in range(255):
						if i*2 < 255:
							self.fondu.set_alpha(i*3) #On augmente son opacité petit à petit
							self.fenetre.blit(self.background_fin, (0,0))
							self.fenetre.blit(self.fond_blanc, (0,0))
							self.fenetre.blit(self.fondu, (0,0))
							py.display.flip()
							py.time.wait(30)
					return 0
					
			pos_texte = pos_texte.move(0,-1)
			self.fenetre.blit(self.background_fin, (0,0))
			self.fenetre.blit(self.fond_blanc, (0,0))
			self.fenetre.blit(self.fondu, (0,0))
			self.fenetre.blit(texte, pos_texte)
			py.display.flip()
			py.time.wait(20)


		#On crée un fondu de fermeture
		for i in range(255):
			if i*2 < 255:
				self.fondu.set_alpha(i*3) #On augmente son opacité petit à petit
				self.fenetre.blit(self.background_fin, (0,0))
				self.fenetre.blit(self.fond_blanc, (0,0))
				self.fenetre.blit(self.fondu, (0,0))
				py.display.flip()
				py.time.wait(30)


	def afficher_dialogue(self, phrase):
		"""
			Méthode permettant d'afficher les dialogues
		"""

		for event in py.event.get():
			pass

		if phrase == self.dialog1: #Si on au tout début du dialogue
			#On crée un fondu d'ouverture
			for i in range(255):
				if 255 - 3*i > 0:
					self.fondu.set_alpha(255-3*i) #On crée un fondu
				else:
					break
				self.fenetre.blit(self.background_trone, (0,0))
				self.fenetre.blit(self.zone_texte, (0, FENETRE_Y - 105))
				self.fenetre.blit(self.fondu, (0,0))
				py.display.flip()
				py.time.wait(30)
		else:
			self.fenetre.blit(self.background_trone, (0,0))
			self.fenetre.blit(self.zone_texte, (0, FENETRE_Y - 105))

		liste_phrase = phrase.split("\n") #On découpe toutes les phrases

		x = 0
		y = FENETRE_Y - 100

		for ligne in liste_phrase:
			for lettre in ligne:
				for event in py.event.get():
					if event.type == QUIT:
						return 0

				#On affiche les lettres une par une
				text = self.font2.render(lettre,1,BLANC)
				pos_text = text.get_rect()
				self.fenetre.blit(text, (15+x, y))
				py.display.flip()

				x += pos_text.left + text.get_width() + 2

				if lettre != ".":
					py.time.wait(50)
				else:
					py.time.wait(400) 
			x=0
			y+=20

		#On attend que le joueur appuie sur une touche pour passer au dialogue suivant
		suivant = False
		while not suivant:
			for event in py.event.get():
				if event.type == KEYDOWN:
					suivant = True

	def afficher_credits(self):
		"""
			Méthode permettant d'afficher les crédits
		"""

		credits = py.image.load("data/images/credits.png").convert() #On charge l'image des crédits
		pos_credits = credits.get_rect()
		pos_credits.move_ip(0, FENETRE_Y + 10)

		while pos_credits.bottom > 0: #On fait monter l'image jusqu'à ce qu'elle sorte de l'écran
			for event in py.event.get():
				if event.type == QUIT:
					return 0
			pos_credits = pos_credits.move(0,-1)
			self.fenetre.blit(credits, pos_credits)
			py.display.flip()
			py.time.wait(20)

	def afficher(self):
		"""
			Méthode permettant de lancer la totalité du prologue/épiloque/crédits
		"""



		if self.type_prologue == DEBUT: 
			######### PROLOGUE #########
			self.afficher_prologue()
		
			son.charger_musique_dialogue()
			son.mixer.music.play(loops=-1)
			self.afficher_dialogue(self.dialog1)
			self.afficher_dialogue(self.dialog2)
			self.afficher_dialogue(self.dialog3)

			for i in range(100):
				if i*3 < 100:
					self.fondu.set_alpha(i*3) #Et on augmente son opacité petit à petit
					self.fenetre.blit(self.fondu, (0,0))
					py.display.flip()
					py.time.wait(30)

		else:
			######### EPILOGUE #########
			son.stop_all()
			self.afficher_epilogue()
			self.afficher_credits()

		son.stop_all()
		py.display.quit()