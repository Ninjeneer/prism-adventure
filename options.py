# coding: utf-8

FICHIER_OPTIONS = "data/options.opt" #On définit le chemin du fichier

def test_fichier():
	"""
		Fonction permettant de tester si le fichier existe avant de lire dedans
		Si le fichier n'existe pas, il est créé avec une valeur par défaut
	"""

	try:
		fichier = open(FICHIER_OPTIONS, "r") #On tente de lire dans le fichier
	except IOError: #Si il n'existe pas
		fichier = open(FICHIER_OPTIONS, "w") #On le crée
		fichier.write("100") #Et on ajoute la valeur par défaut 100
	finally:
		fichier.close() #Peu importe les situations, on ferme le fichier à la fin


def get_son():
	"""
		Fonction permettant de récupérer la valeur du son dans les options
	"""

	test_fichier() #On regarde si le fichier existe, si non, il est créé

	with open(FICHIER_OPTIONS, "r") as fichier:
		son = fichier.read() #On récupère le contenu du fichier

	try:
		son = int(son)
	except:
		son = 100

	if 0 <= son <= 100: #Si la valeur du son se trouve entre 0 et 100
		return son #On retourne sa valeur
	else: #Sinon
		return 100 #On remet la valeur par défaut

def save_son(volume):
	"""
		Fonction permettant de sauvegarder le volume du son
	"""

	test_fichier() #On regarde si le fichier existe, si non, il est créé

	try:
		volume = str(volume) #On converti le volume en string
	except:
		volume = "100"

	with open(FICHIER_OPTIONS, "w") as fichier:
		fichier.write(volume) #On écrit le volume du son