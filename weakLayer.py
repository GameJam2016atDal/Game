
from pygame.sprite import Sprite
from pygame.image import load
import os

class weakLayer(Sprite):
	def __init__(self):
		super().__init__()
		self.image = load(os.getcwd() + '/img/weakLayer.png')
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = (600, 700)
