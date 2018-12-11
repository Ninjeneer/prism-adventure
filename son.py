from pygame import mixer

import options

musique_en_cours = False #Booléen permettant de savoir si une musique est jouée

mixer.init(44100, -16, 2, 2048) #On initialise le module son de Pygame
prisme = mixer.Sound("data/sons/prisme.ogg")

def charger_musique_niveaux():
	"""
		Fonction permettant de charger la musique de fond avec son volume
	"""
	mixer.music.load("data/sons/musique-niveaux.ogg")

	volume = options.get_son() / 100
	mixer.music.set_volume(volume)

def charger_musique_boss():
	"""
		Fonction permettant de charger la musique du boss avec son volume
	"""
	mixer.music.load("data/sons/musique-boss.ogg")

	volume = options.get_son() / 100
	mixer.music.set_volume(volume)

def charger_musique_win():
	"""
		Fonction permettant de charger la musique du boss avec son volume
	"""

	mixer.music.load("data/sons/win.ogg")

	volume = options.get_son() / 100
	mixer.music.set_volume(volume)


def charger_musique_gameover():
	"""
		Fonction permettant de charger la musique du boss avec son volume
	"""
	mixer.music.load("data/sons/musique-gameover.ogg")

	volume = options.get_son() / 100
	mixer.music.set_volume(volume)

def charger_musique_prologue():
	"""
		Fonction permettant de charger la musique du prologue avec son volume
	"""
	mixer.music.load("data/sons/musique-prologue.ogg")

	volume = options.get_son() / 100
	mixer.music.set_volume(volume)


def charger_musique_epilogue():
	"""
		Fonction permettant de charger la musique de l'épilogue avec son volume
	"""
	mixer.music.load("data/sons/musique-epilogue.ogg")

	volume = options.get_son() / 100
	mixer.music.set_volume(volume)

def charger_musique_dialogue():
	"""
		Fonction permettant de charger la musique de l'épilogue avec son volume
	"""
	mixer.music.load("data/sons/musique-throne.ogg")

	volume = 0.07
	mixer.music.set_volume(volume)

def charger_musique_menu():
	"""
		Fonction permettant de charger la musique du menu
	"""
	mixer.music.load("data/sons/musique-menu.ogg")

	volume = 0.1
	mixer.music.set_volume(volume)

def stop_all():
	"""
		Fonction permettant d'arrêter tous les sons en cours
	"""

	global musique_en_cours

	mixer.music.stop()
	musique_en_cours = False