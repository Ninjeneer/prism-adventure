# coding: utf-8

"""
	

  _____           _      _     _____  _____ _   _ 
 |  __ \         (_)    | |   |_   _|/ ____| \ | |
 | |__) | __ ___  _  ___| |_    | | | (___ |  \| |
 |  ___/ '__/ _ \| |/ _ \ __|   | |  \___ \| . ` |
 | |   | | | (_) | |  __/ |_   _| |_ ____) | |\  |
 |_|   |_|  \___/| |\___|\__| |_____|_____/|_| \_|
                _/ |                              
               |__/                               


"""



############################
# JEU : PRISM ADVENTURE    #
# PAR : ALOUACHE LOAN      #
#       RIETTE NATHAN      #
############################


#Importation des modules Pygame
import pygame as py
from pygame.locals import *

#Importation des différents fichiers
from constantes import *
from carte import *
from personnage import *
from bots import *
from fireball import *
from boutons import *
from interface import *

import son
import options
import aide
import prologue

#Importation de Tkinter
from tkinter import *
from tkinter.messagebox import *
import tkinter.ttk as ttk

#Importation du module de système d'exploitation
import os
#Importation du module de système
import sys


mode_joueur = 0 #Permet de connaître le mode de jeu choisi (1 joueur / 2 joueurs)

###### CHEATS #######
god_mode     = False
armagedon    = False
degats_bonus = False
#####################

class Menu():
	"""
		Classe permettant de créer le menu principal
	"""


	def __init__(self):
		"""
			Constructeur de la classe Menu
		"""

		son.charger_musique_menu()
		son.mixer.music.play(loops=-1)
		son.musique_en_cours = True

		self.fenetre = Tk()
		self.fenetre.title("Prism Adventure") # On définit le titre de la fenêtre
		self.fenetre.resizable(0,0) # On empêche l'utilisateur de redimensionner la fenêtre

		self.main_frame = Frame(self.fenetre) # Frame prinicpale (Utilisée pour faciliter la tâche en cas de redesign de la fenêtre)

		self.titre = Label(self.main_frame, text="PRISM ADVENTURE", font=("Ubuntu", 16))
		self.bt_prologue = Button(self.main_frame, text="Prologue", height=2, command=self.lancer_prologue)
		self.bt_aventure = Button(self.main_frame, text="Aventure", height=5, command=lambda x=3: Menu.set_nb_joueurs(self, x))
		self.bt_1j = Button(self.main_frame, text="Mode 1 joueur", height=5, command=lambda x=1: Menu.set_nb_joueurs(self, x))
		self.bt_2j = Button(self.main_frame, text="Mode 2 joueurs", height=5, command=lambda x=2: Menu.set_nb_joueurs(self, x))

		liste_niveaux_aventure = os.listdir("data/levels/aventure/")
		self.select_aventure = ttk.Combobox(self.main_frame, values=sorted(liste_niveaux_aventure), state="readonly")
		if len(liste_niveaux_aventure) > 0:
			self.select_aventure.current(0)


		liste_niveaux = os.listdir("data/levels/") #On récupère la liste des fichiers dans le dossier
		try:
			liste_niveaux.remove("deux_joueurs") #On enlève la carte deux joueurs du mode 1 joueur
			liste_niveaux.remove("aventure") #On enlève le dossier "aventure"
		except:
			pass
		self.select = ttk.Combobox(self.main_frame, values=sorted(liste_niveaux), state="readonly") #Liste déroulante
		if len(liste_niveaux) > 0:
			self.select.current(0) #Par défaut le champs est vide. On le rempli alors avec la première entrée

		self.bt_editeur = Button(self.main_frame, text="Éditeur de niveau", height=2, command=self.lancer_editeur)
		self.bt_aide = Button(self.main_frame, text="Aide", width=20, command=self.lancer_aide)
		self.bt_options = Button(self.main_frame, text="Options", width=20, command=self.ouvrir_options)
		self.bt_jouer = Button(self.main_frame, text="Jouer !", height=5, command=self.lancer_jeu)
		



		# On place les widgets sur la fenêtre
		self.main_frame.pack(padx=10, pady=10)

		self.titre.grid(columnspan=5, padx=10, pady=10)
		self.bt_prologue.grid(columnspan=5, column=0, row=2, padx=10, pady=10, sticky="we") #L'attribut "sticky" indique que le widget doit s'étendre de gauche à droite (WE = West-Est)
		self.bt_aventure.grid(columnspan=5, column=0, row=3, padx=10, pady=10, sticky="we")
		self.bt_1j.grid(column=0, row=5, padx=10, pady=10, sticky="we") 
		self.bt_2j.grid(column=1, row=5, padx=10, pady=10, sticky="we")
		self.bt_editeur.grid(columnspan=5, row=7, padx=10, pady=10, sticky="we")

		self.bt_aide.grid(column=0, row=8, padx=10, pady=10)
		self.bt_options.grid(column=1, row=8, padx=10, pady=10)
		self.bt_jouer.grid(columnspan=5, column=0, row=9, padx=10, pady=10, sticky="we")

		with open(FICHIER_PSEUDO, "r") as fichier: #On cherche si le joueur a déjà entré son pseudo
			pseudo = fichier.read()

		#Si on ne trouve pas de pseudo, c'est le tout premier lancement du jeu
		if pseudo == "":
			self.demander_pseudo() #On demande le pseudo au joueur

		self.lettres_tapees = ""
		self.fenetre.bind_all("<KeyPress>", self.clavier) #On récupère tout ce que le joueur tape pour vérifier le code de triche


	def demander_pseudo(self):
		"""
			Méthode permettant de demander le pseudo du joueur
		"""

		self.fenetre_pseudo = Toplevel() #On crée une fenêtre fille au menu
		self.fenetre_pseudo.resizable(0,0) #On empêche l'utilsateur de redimensionner la fenêtre
		self.fenetre_pseudo.grab_set()
		self.fenetre_pseudo.focus_force()

		main_frame = Frame(self.fenetre_pseudo) #On crée une frame pour ajouter un padding à la fenêtre

		titre = Label(main_frame, text="Entrez votre pseudo (3 - 12) : ")
		self.ent_pseudo = Entry(main_frame) #Champs de texte du pseudo
		bt_valider = Button(main_frame, text="OK", command=self.valider_pseudo)

		#On place les widgets sur la fenêtre
		main_frame.grid(padx=15, pady=15)
		titre.grid(column=0, row=0)
		self.ent_pseudo.grid(column=1, row=0, sticky="ns")
		bt_valider.grid(column=2, row=0, sticky="ns", padx=5)

	def valider_pseudo(self):
		"""
			Méthode permettant de valider le pseudo du joueur
		"""
		pseudo = self.ent_pseudo.get() #On récupère son pseudo
		if 3 <= len(pseudo) <= 12: #Si son pseudo fait plus de 3 lettres et moins de 12 lettres
			with open(FICHIER_PSEUDO, "w") as fichier: #On ouvre le fichier joueur
				fichier.write(pseudo) #On y écrit son pseudo
				self.fenetre_pseudo.destroy() #On ferme la fenêtre
		else:
			showwarning('Erreur', 'Votre pseudo doit contenir entre 3 et 12 lettres !') #On affiche un warning


	def set_nb_joueurs(self, mode):
		"""
			Méthode modifiant le type de jeu
		"""

		global mode_joueur

		mode_joueur = mode

		bg_color = self.fenetre.cget('bg') #Récupère la couleur de fond par défaut

		if mode == 1: #Mode 1 joueur
			self.bt_1j.config(bg="#669999", fg="#FFFF00", relief="sunken") #On change le design du bouton
			self.bt_2j.config(bg=bg_color, fg="black", relief="raised") #Et on reset le design de l'autre
			self.bt_aventure.config(bg=bg_color, fg="black", relief="raised")

			self.select.grid(columnspan=5, row=6, padx=10, sticky="we") #On affiche la liste déroulante
			self.select_aventure.grid_forget()
		elif mode == 2: #Mode 2 joueurs
			self.bt_2j.config(bg="#669999", fg="#FFFF00", relief="sunken")
			self.bt_1j.config(bg=bg_color, fg="black", relief="raised")
			self.bt_aventure.config(bg=bg_color, fg="black", relief="raised")
			self.select.grid_forget() #On fait disparaître la liste déroulante
			self.select_aventure.grid_forget()
		elif mode == 3: #Mode Aventure
			self.bt_aventure.config(bg="#669999", fg="#FFFF00", relief="sunken")
			self.bt_1j.config(bg=bg_color, fg="black", relief="raised")
			self.bt_2j.config(bg=bg_color, fg="black", relief="raised")
			self.select.grid_forget()

			liste_niveaux = os.listdir("data/levels/aventure") #On récupère la liste des fichiers dans le dossier
			self.select_aventure.config(values=liste_niveaux)
			self.select_aventure.grid(column=0, row=4, columnspan=5, padx=10, sticky="we")


	def lancer_jeu(self):
		"""
			Méthode permettant de lancer le jeu
		"""

		if mode_joueur == 1: #Mode 1 joueur
			niveau_choisi = self.select.get() #On récupère le niveau choisi
			niveau_choisi = "data/levels/" + niveau_choisi #On ajoute le chemin du fichier
		elif mode_joueur == 3: #Mode Aventure
			niveau_choisi = self.select_aventure.get()
			niveau_choisi = "data/levels/aventure/" + niveau_choisi

		if mode_joueur != 0: #Si un mode de jeu à été choisi
			self.quitter() #On ferme la fenêtre
			
			if mode_joueur != 2: #Si il n'a pas choisi le mode 2 joueurs
				demarrer_jeu(niveau_choisi) #On démarre le jeu en mode 1 joueur (Aventure ou Solo)
			else:
				demarrer_2j("data/levels/deux_joueurs") #On démarre le mode 2 joueurs

	def lancer_editeur(self):
		"""
			Méthode permettant d'ouvrir la fenêtre d'édition
		"""

		menu_editeur = Menu_Editeur() #On crée un objet de type Menu_Editeur
		menu_editeur.mainloop() #On ouvre la fenêtre

	def lancer_prologue(self):
		"""
			Méthode permettant de lancer le prologue
		"""

		self.quitter() #On ferme le menu
		pro = prologue.Prologue(DEBUT)
		pro.afficher() #On lance le prologue

		afficher_menu() #Puis on relance le menu

	def lancer_aide(self):
		"""
			Méthode permettant de lancer l'aide
		"""

		self.quitter() #On ferme le menu
		dialog_aide = aide.Dialog_aide()
		dialog_aide.afficher_aide_joueur() #On lance l'aide

		afficher_menu() #Puis on relance le menu

	def ouvrir_options(self):
		"""
			Méthode permettant d'ouvrir la fenêtre des options
		"""

		self.fenetre_option = Toplevel() #On ouvre une fenêtre "fille"
		self.fenetre_option.title("PRISM ADVENTURE | Options") #On change son titre
		self.fenetre_option.resizable(0,0) #On empêche l'utilisateur de le redimensionner la fenêtre

		main_frame = Frame(self.fenetre_option) #On crée une Frame question de simplicité d'utilisation

		titre = Label(main_frame, text="PRISM ADVENTURE | Options", font=("Ubuntu", 16)) #On ajoute un titre
		self.barre_son = Scale(main_frame, from_=0, to=100, tickinterval=10, label="Volume de la musique", orient=HORIZONTAL, length=345, resolution=1) #on crée une barre de défilement
		self.barre_son.set(options.get_son()) #On récupère la valeur du son dans le fichier d'options
		bt_pseudo = Button(main_frame, text="Changer de pseudo", command=self.demander_pseudo) #On crée un bouton pour changer de pseudo
		self.txt_sauvegarde = Label(main_frame, text="Sauvegardé !", fg="green") #Texte indiquant que la sauvegarder est effectuée
		bt_sauvegarder = Button(main_frame, text="Sauvegarder", command=self.sauvegarder_options) #Bouton permettant de sauvegarder les options


		#On affiche tous les widgets
		main_frame.grid(padx=10, pady=10)

		titre.grid(columnspan=5, column=0, row=0, padx=20, pady=20)
		self.barre_son.grid(columnspan=5, column=0, row=1, padx=10, pady=10)
		bt_pseudo.grid(columnspan=5, column=0, row=2, padx=10, pady=10, sticky="we")
		bt_sauvegarder.grid(columnspan=5, column=0, row=4, padx=10, pady=10, sticky="we")

	def sauvegarder_options(self):
		"""
			Méthode permettant de sauvegarder les options
		"""

		volume = self.barre_son.get() #On récupère le volume du son
		options.save_son(volume) #On l'écrit dans un fichier texte
		self.txt_sauvegarde.grid(column=0, row=3, pady=10) #On affiche le texte de sauvegarder

	def clavier(self, e):
		"""
			Méthode permettant de récupérer tout ce qui est tapé
		"""

		global god_mode
		global armagedon
		global degats_bonus
		global DEGATS_FIREBALL

		alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" #On liste les lettres acceptées
		lettre = str(e.char) #On récupère la lettre préssée

		if lettre in alphabet: #Si elle se trouve dans la liste des lettres
			self.lettres_tapees += lettre #On l'ajoute à la liste des lettres tapées

		if "phillipe" in self.lettres_tapees: #Si la liste des lettres tapées contient le code de triche
			self.lettres_tapees = "" #On remet à zéro les lettres tapées
			if not god_mode:
				showinfo("Code de triche", "Madame Phillipe modifie les lois de la physique, vous êtes maintenant invincible.\nPour le désactiver ce code, retapez le.") #On montre un message
				god_mode = True #On active de le god mode
			else:
				showinfo("Code de triche", "Madame Phillipe rétabli les lois de la physique, vous n'êtes plus invincible\nPour réactiver le code, retapez le.") #On montre un message
				god_mode = False #On active de le god mode
				
		elif "thuillier" in self.lettres_tapees:
			self.lettres_tapees = ""
			if not armagedon:
				showinfo("Code de triche", "Grâce à Mr. Thuillier Hamel, la limite de vos boules de feu tend vers +∞\nPour le désactiver ce code, retapez le.") #On montre un message
				armagedon = True #On active le cheat armagedon
			else:
				showinfo("Code de triche", "Monsieur Thuilier Hamel a redéfini la limite de vos boules de feu à 3.\nPour réactiver le code, retapez le.") #On montre un message
				armagedon = False #On active le cheat armagedon

		elif "lebel" in self.lettres_tapees:
			self.lettres_tapees = ""
			if not degats_bonus:
				showinfo("Code de triche", "Monsieur Lebel est énervé. Il diminue la défense immunitaire des ennemis.\nTes boules de feu font maintenant 10x plus dégats.\nPour le désactiver ce code, retapez le.") #On montre un message
				degats_bonus = True #On active le cheat degats_bonus
				DEGATS_FIREBALL = 10
			else:
				showinfo("Code de triche", "Monsieur Lebel s'est calmé, la défense immunitaire des ennemis n'est plus affaiblie\nPour réactiver le code, retapez le.") #On montre un message
				degats_bonus = False #On active le cheat degats_bonus
				DEGATS_FIREBALL = 1



	def quitter(self):
		"""
			Méthode permettant de quitter le menu
		"""

		son.stop_all()
		self.fenetre.quit()
		self.fenetre.destroy()



class Menu_Editeur(Tk):
	"""
		Classe permettant de créer le menu d'édition de niveau
	"""

	def __init__(self):
		"""
			Constructeur de la classe Menu_Editeur
		"""

		var_choix = "" #Variable contenant le choix du joueur (Créer niveau / Editer niveau)

		Tk.__init__(self)

		self.title("PRISM ADVENTURE | EDITEUR") #On définit le titre de la fenêtre
		self.resizable(0,0) #On empêche l'utilisateur de redimensionner la fenêtre

		self.main_frame = Frame(self) #On crée une frame principale (Cf : main_frame du menu principale)

		self.titre = Label(self.main_frame, text="PRISM ADVENTURE| EDITEUR DE NIVEAUX", font=("Ubuntu", 16)) #On ajoute un titre
		self.cb_creer = Radiobutton(self.main_frame, text="Créer un niveau", variable=var_choix, value="1", command=lambda x=1: self.show_frame(x)) #Bouton radio : Créer niveau
		self.cb_editer = Radiobutton(self.main_frame, text="Éditer un niveau", variable=var_choix, value="2", command=lambda x=2: self.show_frame(x)) #Bouton radio : Éditer niveau

		self.frame_creer = Frame(self.main_frame)
		self.ent_nom = Entry(self.frame_creer, fg="grey") #Champs de texte pour entrer le nom du nouveau niveau
		self.ent_nom.insert(0, "Nom du niveau")
		self.bt_creer = Button(self.frame_creer, text="Créer le niveau", command=lambda x=1: self.lancer_editeur(x)) #Bouton créer

		self.frame_editer = Frame(self.main_frame)
		liste_niveaux = os.listdir("data/levels/") #On récupère la liste des niveaux dans le dossier
		try:
			liste_niveaux.remove("aventure") #On tente de remove le dossier aventure
		except:
			pass
		self.select_level = ttk.Combobox(self.frame_editer, values=liste_niveaux, state="readonly") #Liste déroulante
		self.select_level.current(0)
		self.bt_editer = Button(self.frame_editer, text="Éditer le niveau", command=lambda x=2: self.lancer_editeur(x)) #Bouton éditer
	
		

		#On place les widgets dans la fenêtre

		self.main_frame.pack()

		self.titre.grid(columnspan=5, padx=10, pady=10)
		self.cb_creer.grid(column=0, row=1, padx=10, pady=10)
		self.cb_editer.grid(column=1, row=1, padx=10, pady=10)

		#Frame contenant les widgets nécessaires à la création d'un niveau
		self.ent_nom.grid(column=0, row=2, pady=5)
		self.bt_creer.grid(column=0, row=3, sticky="we", pady=5)

		#Frame contenant les widgets nécessaires à la création d'un niveau
		self.select_level.grid(column=0, row=0, pady=5)
		self.bt_editer.grid(column=0, row=1, pady=5, sticky="we")

		

		self.ent_nom.bind("<Button-1>", lambda mode=1: self.modif_ent_nom(mode))
		
		self.mainloop() #On affiche la fenêtre

	def show_frame(self, frame_id):
		"""
			Méthode permettant d'afficher / masquer les options d'édition
		"""
		
		if frame_id == 1: #si le joueur a choisi de créer un niveau
			self.frame_creer.grid(column=0, row=2, padx=10, pady=10) #On affiche la frame de création
			self.frame_editer.grid_forget() #On masque la frame d'édition
		else: #si il a choisi d'éditer un niveau
			self.frame_editer.grid(column=1, row=2, padx=10, pady=10) #On affiche la frame d'édition
			self.frame_creer.grid_forget() #On masque la frame de création

	def lancer_editeur(self, mode):
		"""
			Méthode permettant de lancer l'éditeur de niveau
		"""

		if mode == 1: #Si le joueur crée un niveau
			niveau_choisi = self.ent_nom.get() #On récupère le nom du niveau dans le champs de texte
		else: #Si il édite un niveau existant
			niveau_choisi = self.select_level.get() #On récupère le nom du niveau dans la liste déroulante

			try:
				niveau_choisi.remove("aventure") #On tente de retirer le dossier Aventure de la liste
			except:
				pass

		niveau_choisi = "data/levels/" + niveau_choisi#On lui ajoute le chemin du dossier levels


		demarrer_editeur(niveau_choisi) #On lance l'éditeur

	def modif_ent_nom(self, event, mode):
		"""
			Méthode permettant de modifier le design du champs de texte en cas de clique
		"""
		if mode == 1:
			self.ent_nom.delete(0, END) #On supprime le placeholder
			self.ent_nom.config(fg="black") #On configure l'écriture en noire






def afficher_menu():
	
	"""
		Fonction créant le menu et l'affichant
	"""
	menu = Menu() #On crée un objet de type Menu
	menu.fenetre.mainloop() #On ouvre la fenêtre

################# FONCTIONS DU JEU #################

def fondu(fenetre):

	"""
		Méthode permettant de faire un fondu à la mort du boss
	"""
	py.time.wait(60) #On attend un petit peu avant de lancer le fondu
	fond = py.Surface((FENETRE_X, FENETRE_Y)) #On crée une surface
	fond.fill(NOIR) #On la remplie de noir
	fond.set_alpha(0) #On la rend transparente

	for i in range(100):
		if i*2 < 100:
			fond.set_alpha(i*2) #Et on augmente son opacité petit à petit
			fenetre.blit(fond, (0,0))
			py.display.flip()
			py.time.wait(30)


def verif_touche_appuyee(liste_touches):
	
	"""
		Cette fonction permet de vérifier si le joueur presse une flêche directionnelle
	"""

	nb_touches = 0 #Nombre de touches appuyées

	for touche in liste_touches:
		if touche == True: #Si une touche est appuyée
			nb_touches += 1 #On incrémente le nombre de touches appuyées

	if nb_touches > 0: #Si une touche est appuyée
		return True #On retourne True
	else:
		return False #Sinon on retourne False



def changer_niveau(niveau_choisi):

	"""
		Fonction permettant de changer de niveau
	"""

	if mode_joueur == 1:
		liste_niveaux = os.listdir("data/levels/")
		liste_niveaux.remove("deux_joueurs")

		prefix = "data/levels/"
	else:
		liste_niveaux = os.listdir("data/levels/aventure/")
		prefix = "data/levels/aventure/"

	max_level = len(liste_niveaux) - 1 #On récupère le nombre de niveaux

	indice_niveau_suivant = 0

	for i, nom_level in enumerate(liste_niveaux): #On récupère la position (i) dans la liste et sa valeur (nom_level)
		nom_level = prefix + nom_level #On ajoute le chemin du niveau
		if nom_level == niveau_choisi and i < max_level: #Si il y a un niveau après celui en cours
			indice_niveau_suivant = i + 1 #On change de niveau


	demarrer_jeu(prefix + liste_niveaux[indice_niveau_suivant]) #On lance le jeu avec le niveau suivant



def demarrer_jeu(niveau_choisi):

	"""
		Fonction créant la fenêtre Pygame et l'affichant
	"""

	fenetre = py.display.set_mode((FENETRE_X, FENETRE_Y), DOUBLEBUF) #On crée la fenêtre Pygame

	if mode_joueur == 1: #Si on est en mode solo
		titre_niveau = "PRISM ADVENTURE | " + niveau_choisi[12:]
	else: #Si on est en mode aventure
		titre_niveau = "PRISM ADVENTURE | " + niveau_choisi[21:]
	py.display.set_caption(titre_niveau) #On définit le titre de la fenêtre


	niveau = Carte() #On crée le niveau, de type Carte.
	niveau.charger(niveau_choisi) #On charge le niveau en fonction du niveau choisi

	joueur = Personnage(niveau.spawn_joueur, niveau.liste_obstacles, 1) #On crée un personnage joueur de type Personnage.
	dernier_niveau = False
	if niveau_choisi == "data/levels/aventure/Niveau Final - Étage 2":
		dernier_niveau = True

		joueur.type_fireball = 2
		joueur.nb_fireball = 999999999 

		interface = Interface()

	if armagedon: joueur.nb_fireball = 999999999 
	liste_fireball = [] #On crée une liste de boules de feu

	compteur_boucle = 0 #Compteur de boucle
	touches_appuyees = [False, False, False, False] #Liste des flêches directionnelle (False : Non pressée - True : Pressée)
	espace_maintenu = False

	if not dernier_niveau:
		if not son.musique_en_cours:
			son.charger_musique_niveaux() #On charge la musique du niveau
			son.mixer.music.play(loops=-1) #On active la lecture en boucle
			son.musique_en_cours = True
	else:
		son.charger_musique_boss() #On charge la musique du niveau
		son.mixer.music.play(loops=-1) #On active la lecture en boucle
		son.musique_en_cours = True


	#Boucle principale du jeu
	continuer_jeu = True
	while continuer_jeu:

		fenetre.fill(NOIR) #On "nettoie" la fenêtre en la remplissant de noir

		#On récupère tous les évènements du clavier et de la souris
		event = py.event.poll()
		if event.type == QUIT:
			continuer_jeu = False

		k = py.key.get_pressed() #On récupère la (ou les) touches sur lesquelles le joueur appuie


		if k[K_LEFT]: #Si le joueur appuie sur la flêche de gauche
			joueur.deplacer(GAUCHE, niveau.get_prisme) #On le déplace vers la gauche
			joueur.update_orientation(GAUCHE)
			touches_appuyees[0] = True #On indique qu'il presse une touche
		if k[K_RIGHT]:
			joueur.deplacer(DROITE, niveau.get_prisme)
			joueur.update_orientation(DROITE)
			touches_appuyees[1] = True
		if k[K_UP]:
			joueur.deplacer(HAUT, niveau.get_prisme)
			joueur.update_orientation(HAUT)
			touches_appuyees[2] = True
		if k[K_DOWN]:
			joueur.deplacer(BAS, niveau.get_prisme)
			joueur.update_orientation(BAS)
			touches_appuyees[3] = True
		if k[K_SPACE]:
			if not espace_maintenu:
				if joueur.nb_fireball > 0:
					joueur.nb_fireball -= 1
					liste_fireball.append(Fireball(joueur))
				espace_maintenu = True


		if event.type == KEYUP: #Si le joueur relâche une des flêche
			if event.key == K_LEFT: #Si il relâche la flêche de gauche
				touches_appuyees[0] = False #On indique qu'il n'appuie plus sur la touche
			if event.key == K_RIGHT:
				touches_appuyees[1] = False
			if event.key == K_UP:
				touches_appuyees[2] = False
			if event.key == K_DOWN:
				touches_appuyees[3] = False
			if event.key == K_SPACE:
				espace_maintenu = False



		compteur_boucle += 1 #On augmente le compteur de boucle de 1

		niveau.afficher(fenetre) #On affiche la carte
		fenetre.blit(joueur.tileset, joueur.pos, joueur.image_en_cours) #On affiche le joueur

		if compteur_boucle % 13 == 0: #Toutes les 13 boucles
			for bot in niveau.liste_bots: #Pour chaque bot
				bot.update() #On met à jour son image

			if verif_touche_appuyee(touches_appuyees): #Si le joueur appuie sur une flêche
				joueur.update() #On met à jour l'image du joueur


		############### GESTION DES BOTS #######################
		for bot in niveau.liste_bots: #Pour chaque bot
			if not god_mode:
				if joueur.pos.colliderect(bot.pos): #S'il y a collision entre le joueur et le bot
					game_over(fenetre, niveau_choisi, continuer_jeu) #Le joueur a perdu

			if dernier_niveau: #Si le joueur est au dernier niveau
				if bot.type_bot == BOSS:
					interface.update(fenetre, bot) #On affiche la vie du boss

			bot.deplacer()
			fenetre.blit(bot.tileset, bot.pos, bot.image_en_cours) #On affiche le bot
			
			 

		############ GESTION DES BOULES DE FEU ################
		for fireball in liste_fireball: #Pour chaque boule de feu
			for mur in niveau.liste_obstacles: #Pour chaque mur
				if fireball.pos.colliderect(mur): #Si la boule de feu touche un mur
					if fireball in liste_fireball: #Si la boule de feu est toujours dans la liste
						liste_fireball.remove(fireball) #Elle disparaît

			for bot in niveau.liste_bots: #Pour chaque bot
				if fireball.pos.colliderect(bot.pos): #Si une boule touche un bot
					if fireball in liste_fireball: #Si la boule de feu est toujours dans la liste
						liste_fireball.remove(fireball) #La boule de feu disparaît
						bot.pv -= (1 * DEGATS_FIREBALL)
						if bot.pv <= 0:
							if not dernier_niveau: #Si on tue un bot différent du boss
								bot.respawn() #On fait repsawn le bot à son emplacement initial
							else: #Sinon si on tue le boss
								son.mixer.music.fadeout(1500)
								fondu(fenetre) #On fait un fondu
								pro = prologue.Prologue(FIN) #Et on lance le prologue de fin
								pro.afficher()
								afficher_menu() #Puis on relance le menu du jeu


			fenetre.blit(fireball.image, fireball.pos) #On affiche la boule de feu
			fireball.update() #On met à jour sa position

		########## GESTION DE LA SORTIE ###########################
		if len(niveau.prisme) > 0: #Si il y a un prisme sur la carte
			for prisme in niveau.prisme: #On parcours la liste des prismes présents
				if joueur.pos.colliderect(prisme): #Si le joueur ramasse le prisme
					son.prisme.play() #On joue un son
					niveau.get_prisme = True #On indique que le joueur a ramassé le prisme
					niveau.prisme.remove(prisme) #On enlève le prisme

					#On parcours la carte afin de faire disparaître les portes
					for j in range(len(niveau.structure)): 
						for i in range(len(niveau.structure[0])):
							if 219 <= niveau.structure[j][i] <= 224: #On retire tous les prismes
								niveau.structure[j][i] = -1

							if niveau.structure[j][i] == 80 or niveau.structure[j][i] == 81: #Si on trouve une porte (Bloc 80 et 81)
								niveau.structure[j][i] = -1 #On la remplace par du vide

								position_porte = py.Rect(i * TAILLE_SPRITE, j * TAILLE_SPRITE, TAILLE_SPRITE, TAILLE_SPRITE) #On récupère la position de la porte
								niveau.liste_obstacles.remove(position_porte) #Et on la retire de la liste des obstacles
					break

		if niveau.levier != 0: #Si il y a un levier
			if joueur.pos.colliderect(niveau.levier): #Si le joueur touche le levier
				for j in range(len(niveau.structure)): 
					for i in range(len(niveau.structure[0])):

						#On test les différents types de levier pour afficher le bon dans une autre position
						if niveau.structure[j][i] == 230:
							if not niveau.get_levier:
								niveau.structure[j][i] = 231

						elif niveau.structure[j][i] == 231:
							if not niveau.get_levier:
								niveau.structure[j][i] = 230

						elif niveau.structure[j][i] == 232:
							if not niveau.get_levier:
								niveau.structure[j][i] = 233

						elif niveau.structure[j][i] == 233:
							if not niveau.get_levier:
								niveau.structure[j][i] = 232

						elif niveau.structure[j][i] == 234:
							if not niveau.get_levier:
								niveau.structure[j][i] = 235

						elif niveau.structure[j][i] == 235:
							if not niveau.get_levier:
								niveau.structure[j][i] = 234


				if not niveau.get_levier: #Si il arrive pour la première fois sur le levier
					if not niveau.action_levier: #Si le levier en train de fermer la porte
							#On ouvre la porte
							niveau.structure[niveau.position_portes[0][0]][niveau.position_portes[0][1]] = -1 #On retire les deux blocs de porte
							niveau.structure[niveau.position_portes[1][0]][niveau.position_portes[1][1]] = -1

							position_porte = py.Rect(niveau.position_portes[0][1] * TAILLE_SPRITE, niveau.position_portes[0][0] * TAILLE_SPRITE, TAILLE_SPRITE, TAILLE_SPRITE) #On récupère la position de la porte
							niveau.liste_obstacles.remove(position_porte) #Et on la retire de la liste des obstacles
							position_porte = py.Rect(niveau.position_portes[1][1] * TAILLE_SPRITE, niveau.position_portes[1][0] * TAILLE_SPRITE, TAILLE_SPRITE, TAILLE_SPRITE) #On récupère la position de la porte
							niveau.liste_obstacles.remove(position_porte) #Et on la retire de la liste des obstacles
							niveau.action_levier = True #Porte ouverte
					else: #Si le levier en train d'ouvrir la porte
						#On ferme la porte
						niveau.structure[niveau.position_portes[0][0]][niveau.position_portes[0][1]] = 81 #On remet les deux blocs de porte
						niveau.structure[niveau.position_portes[1][0]][niveau.position_portes[1][1]] = 80

						position_porte = py.Rect(niveau.position_portes[0][1] * TAILLE_SPRITE, niveau.position_portes[0][0] * TAILLE_SPRITE, TAILLE_SPRITE, TAILLE_SPRITE) #On récupère la position de la porte
						niveau.liste_obstacles.append(position_porte) #Et on les remet dans la liste des obsctacles
						position_porte = py.Rect(niveau.position_portes[1][1] * TAILLE_SPRITE, niveau.position_portes[1][0] * TAILLE_SPRITE, TAILLE_SPRITE, TAILLE_SPRITE) #On récupère la position de la porte
						niveau.liste_obstacles.append(position_porte) #Et on les remet dans la liste des obsctacles

						niveau.action_levier = False #Porte fermée

				niveau.get_levier = True #Le joueur touche le levier

			else:
				niveau.get_levier = False #Le joueur ne touche pas de levier


		########## GESTION DU PERSONNAGE ######################
		if joueur.pos.left + joueur.pos.width < 0 or joueur.pos.left > FENETRE_X or joueur.pos.top + joueur.pos.height < 0 or joueur.pos.top > FENETRE_Y: #Si le joueur sort de la fenêtre
			changer_niveau(niveau_choisi) #On change de niveau


		py.display.flip()#On actualise l'affichage
		py.event.pump()
		py.time.wait(2) #On ralenti la boucle de 5 milisecondes

	py.display.quit() #Si on sort de la boucle, on quitte Pygame
	afficher_menu() #Et on ré-ouvre le menu



def demarrer_2j(niveau_choisi):

	"""
		Fonction créant la fenêtre Pygame et l'affichant
	"""

	fenetre = py.display.set_mode((FENETRE_X, FENETRE_Y), DOUBLEBUF) #On crée la fenêtre Pygame

	titre_niveau = "PRISM ADVENTURE | Multijoueurs"
	py.display.set_caption(titre_niveau) #On définit le titre de la fenêtre

	niveau = Carte() #On crée le niveau, de type Carte.
	niveau.charger(niveau_choisi) #On charge le niveau en fonction du niveau choisi

	joueur = Personnage(niveau.spawn_joueur, niveau.liste_obstacles, 1) #On crée un personnage joueur de type Personnage.
	joueur2 = Personnage(niveau.spawn_joueur2, niveau.liste_obstacles, 2) #On crée un deuxième personnage
	

	compteur_boucle = 0 #Compteur de boucle
	touches_appuyees = [False, False, False, False] #Liste des flêches directionnelle (False : Non pressée - True : Pressée)
	touches_appuyees_j2 = [False, False, False, False] #Liste des touches sur lesquelles le joueur 2 appuie
	espace_maintenu = False

	os = sys.platform #On récupère l'OS car on gère les touches différement selon les OS

	clock = py.time.Clock() #On créé un objet de type Clock
	temps = 0 #Variable permettant de mesurer le temps de jeu

	son.charger_musique_boss() #On charge la musique du boss
	son.mixer.music.play(loops=-1) #On joue la musique du boss en boucle

	#Boucle principale du jeu
	continuer_jeu = True
	while continuer_jeu:

		fenetre.fill(NOIR) #On "nettoie" la fenêtre en la remplissant de noir

		#On récupère tous les évènements du clavier et de la souris
		event = py.event.poll()

		if event.type == QUIT: #Si le joueur ferme à l'aide la croix rouge
			continuer_jeu = False #On arrête le jeu

		k = py.key.get_pressed() #On récupère la (ou les) touches sur lesquelles le joueur appuie


		################ GESTION DES TOUCHES JOUEUR 1 ################################

		if k[K_LEFT]: #Si le joueur appuie sur la flêche de gauche
			joueur.deplacer(GAUCHE, niveau.get_prisme) #On le déplace vers la gauche
			joueur.update_orientation(GAUCHE)
			touches_appuyees[0] = True #On indique qu'il presse une touche
		if k[K_RIGHT]:
			joueur.deplacer(DROITE, niveau.get_prisme)
			joueur.update_orientation(DROITE)
			touches_appuyees[1] = True
		if k[K_UP]:
			joueur.deplacer(HAUT, niveau.get_prisme)
			joueur.update_orientation(HAUT)
			touches_appuyees[2] = True
		if k[K_DOWN]:
			joueur.deplacer(BAS, niveau.get_prisme)
			joueur.update_orientation(BAS)
			touches_appuyees[3] = True

		################ GESTION DES TOUCHES JOUEUR 2 ################################

		if k[K_d]:
			joueur2.deplacer(DROITE, niveau.get_prisme)
			joueur2.update_orientation(DROITE)
			touches_appuyees_j2[1] = True

		if k[K_s]:
			joueur2.deplacer(BAS, niveau.get_prisme)
			joueur2.update_orientation(BAS)
			touches_appuyees_j2[3] = True

		if os != "linux": #Si on est sous Windows
			#On anticipe le clavier Qwerty
			if k[K_w]: 
				joueur2.deplacer(HAUT, niveau.get_prisme)
				joueur2.update_orientation(HAUT)
				touches_appuyees_j2[2] = True
			if k[K_a]:
				joueur2.deplacer(GAUCHE, niveau.get_prisme)
				joueur2.update_orientation(GAUCHE)
				touches_appuyees_j2[0] = True
		else: #Sinon
			#On reste en Azerty
			if k[K_z]:
				joueur2.deplacer(HAUT, niveau.get_prisme)
				joueur2.update_orientation(HAUT)
				touches_appuyees_j2[2] = True
			if k[K_q]: #Si le joueur appuie sur la flêche de gauche
				joueur2.deplacer(GAUCHE, niveau.get_prisme) #On le déplace vers la gauche
				joueur2.update_orientation(GAUCHE)
				touches_appuyees_j2[0] = True #On indique qu'il presse une touche




		if event.type == KEYUP: #Si le joueur relâche une des flêche
			################ JOUEUR 1 ################
			if event.key == K_LEFT: #Si il relâche la flêche de gauche
				touches_appuyees[0] = False #On indique qu'il n'appuie plus sur la touche
			elif event.key == K_RIGHT:
				touches_appuyees[1] = False
			elif event.key == K_UP:
				touches_appuyees[2] = False
			elif event.key == K_DOWN:
				touches_appuyees[3] = False

			################ JOUEUR 2 ################
			if os != "linux":
				if event.key == K_a: #Si il relâche la flêche de gauche
					touches_appuyees_j2[0] = False #On indique qu'il n'appuie plus sur la touche
				elif event.key == K_w:
					touches_appuyees_j2[2] = False
			else:
				if event.key == K_q: #Si il relâche la flêche de gauche
					touches_appuyees_j2[0] = False #On indique qu'il n'appuie plus sur la touche
				elif event.key == K_z:
					touches_appuyees_j2[2] = False	

			if event.key == K_d:
				touches_appuyees_j2[1] = False

			elif event.key == K_s:
				touches_appuyees_j2[3] = False


		compteur_boucle += 1 #On augmente le compteur de boucle de 1

		temps += clock.tick() #On incrémente le chrono de jeu

		niveau.afficher(fenetre) #On affiche la carte
		fenetre.blit(joueur.tileset, joueur.pos, joueur.image_en_cours) #On affiche le joueur
		fenetre.blit(joueur2.tileset, joueur2.pos, joueur2.image_en_cours)

		if compteur_boucle % 13 == 0: #Toutes les 13 boucles

			if verif_touche_appuyee(touches_appuyees): #Si le joueur appuie sur une flêche
				joueur.update() #On met à jour l'image du joueur
			if verif_touche_appuyee(touches_appuyees_j2): #Si le joueur 2 appuie sur une touche
				joueur2.update() #On met à jour l'image du joueur 2


		######### GESTION DU PRISME ###########################
		if len(niveau.prisme) > 0: #Si il y a un prisme sur la carte
			for prisme in niveau.prisme: #On parcours la liste des prismes présents
				if joueur.pos.colliderect(prisme): #Si le joueur ramasse le prisme
					niveau.get_prisme = True #On indique que le joueur a ramassé le prisme
					niveau.prisme.remove(prisme) #On enlève le prisme

					son.prisme.play() #On joue le son du prisme

					#On parcours la carte afin de faire disparaître les portes
					for j in range(len(niveau.structure)): 
						for i in range(len(niveau.structure[0])):
							if 219 <= niveau.structure[j][i] <= 224:
								niveau.structure[j][i] = -1

							if niveau.structure[j][i] == 80 or niveau.structure[j][i] == 81: #Si on trouve une porte (Bloc 80 et 81)
								niveau.structure[j][i] = -1 #On la remplace par du vide

								position_porte = py.Rect(i * TAILLE_SPRITE, j * TAILLE_SPRITE, TAILLE_SPRITE, TAILLE_SPRITE) #On récupère la position de la porte
								niveau.liste_obstacles.remove(position_porte) #Et on la retire de la liste des obstacles
					break


		########## GESTION DES PERSONNAGE ######################
		if not god_mode: #Si le joueur n'est pas en god mode
			if joueur.pos.colliderect(joueur2.pos): #Si le joueur 2 touche le joueur 1
				game_over(fenetre, niveau_choisi, continuer_jeu) #On perd

		if joueur.pos.left + joueur.pos.width < 0 or joueur.pos.left > FENETRE_X or joueur.pos.top + joueur.pos.height < 0 or joueur.pos.top > FENETRE_Y: #Si le joueur sort de la fenêtre
			victoire(fenetre, niveau_choisi, continuer_jeu, temps)

	
		py.display.flip() #On actualise l'affichage
		py.event.pump()
		py.time.wait(2) #On ralenti la boucle de 5 milisecondes




	py.quit() #Si on sort de la boucle, on quitte Pygame
	afficher_menu() #Et on ré-ouvre le menu

def victoire(fenetre, niveau_choisi, continuer_jeu, temps):

	"""
		Fonction terminant le jeu en cas de victoire
	"""

	son.charger_musique_win() #On charge la musique de game over
	py.mixer.music.play() #On joue la musique

	image = py.image.load("data/images/victoire.png").convert_alpha() #On importe l'image de victoire
	pos_image = (FENETRE_X / 2 - image.get_width() / 2, FENETRE_Y / 2 - image.get_height() / 2 - 150)

	bt_restart = PyButton(window=fenetre, coord=(25, 500), size=(200,50), color=BLANC, text=("Recommencer", 24, NOIR)) #On crée un bouton
	bt_quitter = PyButton(window=fenetre, coord=(895, 500), size=(200,50), color=BLANC, text=("Quitter", 24, NOIR)) #Idem

	font = py.font.Font(None, 30) #On importe un type de police
	texte_temps = font.render("Bravo ! Tu as réussi à sortir en " + str(decoupe_temps(temps)) + " secondes !", 1, (255, 255, 255)) #On crée le texte
	pos_texte_temps = (FENETRE_X / 2 - texte_temps.get_width() / 2, pos_image[1] + 400) #On définit une position

	continuer_game_over = True
	while continuer_game_over:
		fenetre.fill(NOIR)

		fenetre.blit(image, pos_image) #On affiche l'image
		fenetre.blit(texte_temps, pos_texte_temps) #On affiche le texte

		bt_restart.print() #On affiche le bouton
		bt_quitter.print() #Idem

		for event in py.event.get():
			if event.type == MOUSEBUTTONDOWN:
				if bt_restart.click(event): #Si on clique sur le bouton Recommencer
					demarrer_2j("data/levels/deux_joueurs") #On relance le mode deux joueurs

				if bt_quitter.click(event): #Si on clique sur le bouton Quitter
					continuer_game_over = False #On sort de la boucle

			if event.type == KEYDOWN: #Si le joueur appuie sur une touche
				if event.key == K_r or event.key == K_RETURN: #Si il appuie sur R ou Entrée
					demarrer_2j("data/levels/deux_joueurs") #On relance le mode deux joueurs


		py.display.flip()

	py.display.quit() #On quitte Pygame
	afficher_menu() #Et on raffiche le menu

def game_over(fenetre, niveau_choisi, continuer_jeu):

	"""
		Fonction terminant le jeu en cas d'échec
	"""

	
	image = py.image.load("data/images/game_over/game_over3.png").convert_alpha() #On importe l'image du game over

	son.charger_musique_gameover() #On charge la musique de game over
	py.mixer.music.play() #On joue la musique

	bt_restart = PyButton(window=fenetre, coord=(25, 500), size=(200,50), color=BLANC, text=("Recommencer", 24, NOIR)) #On crée un bouton
	bt_quitter = PyButton(window=fenetre, coord=(895, 500), size=(200,50), color=BLANC, text=("Quitter", 24, NOIR)) #Idem

	blit_x = (fenetre.get_width() / 2) - (image.get_width() / 2) #On définie les coordonnées de blit au centre de l'écran
	blit_y = (fenetre.get_height() / 2) - (image.get_height() / 2) #Idem

	continuer_game_over = True
	while continuer_game_over:
		fenetre.fill(NOIR)

		fenetre.blit(image, (blit_x, blit_y))

		bt_restart.print() #On affiche le bouton
		bt_quitter.print() #Idem

		for event in py.event.get():
			if event.type == MOUSEBUTTONDOWN:
				if bt_restart.click(event): #Si on clique sur le bouton Recommencer
					son.stop_all()
					if mode_joueur != 2:
						demarrer_jeu(niveau_choisi) #On redémarre le jeu
					else:
						demarrer_2j("data/levels/deux_joueurs")

				if bt_quitter.click(event): #Si on clique sur le bouton Quitter
					continuer_game_over = False #On sort de la boucle

			if event.type == KEYDOWN:
				if event.key == K_r or event.key == K_RETURN:
					son.stop_all()
					if mode_joueur != 2:
						demarrer_jeu(niveau_choisi)
					else:
						demarrer_2j("data/levels/deux_joueurs")


		py.display.flip()

	py.display.quit() #On quitte Pygame
	afficher_menu() #Et on raffiche le menu

	
def decoupe_temps(temps):

	"""
		Fonction permettant de convertir les milisecondes en secondes
	"""
	return temps / 1000
		




######################### EDITEUR #############################################

blocActuel = 0

def afficher_bloc_selectionne(blocActuel, x, y, fenetre, niveau):

	"""
		Fonction permettant d'afficher le bloc séléctionné au niveau du curseur
	"""

	x -= (TAILLE_SPRITE / 2) #On place le bloc au centre
	y -= (TAILLE_SPRITE / 2) #On place le bloc au centre

	bloc = niveau.get_bloc(blocActuel) #On récupère le bloc séléctionné

	if x > 345:
		fenetre.blit(niveau.tileset_map, (x,y), bloc) #On l'affiche au niveau du curseur

def block_picker(event):
	"""	
		Fonction permettant de piocher un bloc dans le tileset sur le côté
	"""

	global blocActuel

	if event.pos[0] < 345: #Si on clique quelque part dans la zone du tileset

		#On récupère le bloc séléctionné
		x = floor(event.pos[0] / 23)
		y = floor(event.pos[1] / 25)

		blocActuel = y*15 + x

		print(blocActuel)


def demarrer_editeur(niveau_choisi):

	"""
		Fonction permettant de lancer l'éditeur de jeu
	"""

	global blocActuel
	global apercu_bloc

	py.init() #Initialisation de Pygame

	fenetre = py.display.set_mode((FENETRE_X + 345, FENETRE_Y), DOUBLEBUF) #On crée la fenêtre Pygame

	titre_niveau = "PRISM ADVENTURE | EDITEUR : " + niveau_choisi[12:]
	py.display.set_caption(titre_niveau) #On définit le titre de la fenêtre

	zone_image = py.Surface((345, FENETRE_Y))
	zone_editeur = py.Surface((FENETRE_X, FENETRE_Y))

	editeur = Carte()
	editeur.charger(niveau_choisi) #La carte à éditer correspond au niveau sélectionné par le joueur

	bloc_selection = py.transform.scale(editeur.tileset_map, (345, 405))
	apercu_tileset = py.transform.scale(editeur.tileset_map, (480*COEF_ZOOM, 512*COEF_ZOOM))

	blocMin = 0 #Le bloc minimal possible
	blocMax = 234 #Le bloc maximal possible

	x = 0 #Permet de récupérer la position X du curseur
	y = 0 #Permet de récupréer la position Y du curseur

	clicGauche = False
	clicDroit = False

	continuer_editeur = True
	while continuer_editeur:

		for event in py.event.get(): #On récupère tous les évènements du clavier et de la souris
			if event.type == QUIT: #Si le type d'event est de type QUIT
				continuer_editeur = False #On quitte le mode éditeur

			if event.type == MOUSEBUTTONDOWN: #Si le joueur clique

				if event.button == 1: #Si le clique correspond au clic gauche
					clicGauche = True 
					verifier_spawn(editeur.structure, blocActuel) #On vérifie les doublons
					editeur.editer(event, blocActuel) #On change le bloc pour le blocActuel au coordonnée donné par event
					block_picker(event) #On regarde si il essai de piocher un bloc

				elif event.button == 2: #Si il clique sur la molette
					blocActuel = editeur.copier_bloc(event) #On récupère le bloc ciblé, et modifie le bloc actuel
					block_picker(event) #On regarde si il essai de piocher un bloc

				elif event.button == 3: #Si le clique correspond au clic droit
					clicDroit = True
					editeur.editer(event, -1) #Le bloc est effacé et remplacé par du vide (valeur -1) au coordonée donné par event
					block_picker(event) #On regarde si il essai de piocher un bloc

				elif event.button == 4: #Si le clic correspond à un mouvement de la molette vers le haut
					if blocActuel < blocMax: #Et si le bloc actuel est inférieur au dernier bloc possible
						blocActuel += 1 #On incrémente le bloc actuel
					else: #Sinon
						blocActuel = blocMin #On remet le bloc actuel au minimum


				elif event.button == 5: #Si le clic correspond à un mouvement de la molette vers le bas
					if blocActuel > blocMin: #Si le bloc actuel est supérieur au bloc minimum
						blocActuel -= 1 #On décrémente le bloc actuel
					else: #Sinon
						blocActuel = blocMax #On remet le bloc actuel au maximum

			if event.type == MOUSEBUTTONUP: #Si le joueur relâche le clic
				if event.button == 1: #Si ce clique est le clique gauche
					clicGauche = False
				elif event.button == 3: #Si ce clique est le clique droit
					clicDroit = False

			if event.type == MOUSEMOTION: #Si le joueur déplace la souris
				x = event.pos[0]
				y = event.pos[1]

				if clicGauche: #Si le clique gauche est maintenu
					verifier_spawn(editeur.structure, blocActuel) #On vérifie les doublons
					editeur.editer(event, blocActuel) #On modifie les blocs sélectionnés par le curseur
				elif clicDroit: #Si le clique droite est maintenu
					editeur.editer(event, -1) #On modifie le bloc par du vide

			if event.type == KEYDOWN: #Si le joueur appuie sur une touche du clavier
				if event.key == K_s: #Si cette touche est la touche s
					editeur.sauvegarder() #On sauvegarde la carte
				elif event.key == K_DELETE:
					editeur.reset(fenetre)

		fenetre.blit(zone_image, (0,0))
		fenetre.blit(zone_editeur, (345, 0))

		zone_image.fill(NOIR)
		zone_image.blit(bloc_selection, (0,0))
		zone_image.blit(apercu_tileset, (124, 500), editeur.get_bloc(blocActuel, COEF_ZOOM))

		zone_editeur.fill(NOIR) #On nettoie la fenêtre
		editeur.afficher(zone_editeur) #On affiche la carte
		afficher_bloc_selectionne(blocActuel, x, y, fenetre, editeur) #On affiche le bloc au niveau du curseur

		py.display.flip() #On actualise l'affichage

	py.display.quit()


def verifier_spawn(structure, blocActuel):

	"""
		Fonction empêchant le joueur de placer 2 spawn de type joueur
	"""

	if blocActuel == -2: #Si il tente de placer un spawn joueur
		for j in range(len(structure)):
			for i in range(len(structure[0])):
				if structure[j][i] == -2: #Si on trouve un autre spawn joueur dans la carte
					structure[j][i] = -1 #On remplace l'ancien par du vide




py.init() #Initialisation de Pygame
py.font.init()
afficher_menu() #Le programme démarre ici, on affiche le menu pour la première fois