# coding: utf-8

#########################
# PYGAME BUTTON CREATOR #
#                       #
#          BY           #
#                       #
#     LOAN ALOUACHE     #
#########################

"""
	USAGE : 
		button1 = PyButton(window=PYGAME_WINDOW, coord=(x,y), size=(w,h), color=(R,G,B), text=("your text", FONT_SIZE, (R,G,B)), border=(SIZE, (R,G,B)))
"""


import pygame as py
from pygame.locals import *

class PyButton():

	"""
		Allows you to create and handle Buttons in pygame
	"""

	def __init__(self, window, coord, size, color, text=("", 15, (0,0,0)), border=(0, (0,0,0))):
		self.window = window #Window blit destination (Pygame window)
		self.coord  = coord  #Position of the button (tuple)
		self.size   = size   #Size of the button (tuple)
		self.color  = color  #Color of the button (tuple)
		self.text   = text   #Text inside the button (tuple)
		self.border = border #Border of the button (tuple)


	def print(self):

		"""
			Print the button on the screen
			Order to print : Border -> Button Skin -> Text
		"""

		if self.border[0] > 0:
			#If a border is set
			border = py.Surface((self.size[0] + self.border[0]*2 , self.size[1] + self.border[0]*2))
			border.fill(self.border[1])

			#Define the border's coord
			border_x = self.coord[0] - self.border[0]
			border_y = self.coord[1] - self.border[0]
			coord_border = (border_x, border_y)

			self.window.blit(border, coord_border)


		#Create the Button skin
		button = py.Surface(self.size)
		button.fill(self.color)

		self.window.blit(button, self.coord)

		if self.text != "":
			#If a text is set

			py.font.init()
			#Create a font with default pygame font, and user-defined size
			font = py.font.Font(None, self.text[1])
			#Create a text as an image using user-defined text-color
			render_text = font.render(self.text[0], 1, self.text[2])

			#Define the text's coord
			text_x = self.coord[0] + self.size[0] / 2 - render_text.get_width() / 2
			text_y = self.coord[1] + self.size[1] / 2 - render_text.get_height() / 2
			coord_text = (text_x, text_y)

			self.window.blit(render_text, coord_text)



	def click(self, event):

		"""
			Check if the button is clicked
			Return true if it is, else return false
		"""

		x1 = self.coord[0] #Top-Left corner
		x2 = self.coord[0] + self.size[0] #Top-Right corner
		y1 = self.coord[1] #Bottom-Left corner
		y2 = self.coord[1] + self.size[1] #Bottom-right corner

		if event.pos[0] >= x1 and event.pos[0] <= x2 and event.pos[1] >= y1 and event.pos[1] <= y2: #If the click is in the button area
			return True
		else:
			return False