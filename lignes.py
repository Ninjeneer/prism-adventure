fichiers = ["bots.py", "boutons.py", "carte.py", "constantes.py", "fireball.py", "main.py", "options.py", "personnage.py", "prologue.py", "son.py", "aide.py"]

n = 0

for file in fichiers:
	fd = open(file, "r")
	contenu = fd.readlines()
	
	n += len(contenu)

print(n)