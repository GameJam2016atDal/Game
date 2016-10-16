from pygame.sprite import Sprite
from pygame.image import load
from pygame.time import get_ticks
import os

class giantSpike(Sprite):
	def __init__(self):
		super().__init__()
		self.image = load(os.getcwd() + '/img/giantSpike.png')
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = (620, -70)
		self.movable = False
		self.speed = 20
		self.moveUpSpeed = 8
		self.startTime = None
		self.currentTime = None
		self.moveUp = False
		self.plat = None
		self.chain = chain()
		self.chain.rect.x, self.chain.rect.y = self.rect.x + 10, self.rect.y - 680

	def update(self):
		self.plat.rect.x, self.plat.rect.y = self.rect.x + 10, self.rect.y - 7
		self.chain.rect.x, self.chain.rect.y = self.rect.x + 10, self.rect.y - 680
		if self.movable == False:
			return
		if self.rect.y <= 700 and self.moveUp == False:
			self.plat.rect.y += self.speed
			self.plat.speed = self.speed
			self.rect.y += self.speed
		else:
			self.currentTime = get_ticks()
			if (self.currentTime - self.startTime) / 1000 > 5:
				if self.rect.y >= -70:
					self.moveUp = True
					self.plat.rect.y -= self.moveUpSpeed
					self.plat.speed = -self.moveUpSpeed
					self.rect.y -= self.moveUpSpeed
				else:
					self.moveUp = False
					self.movable = False
					self.plat.speed = 0

class chain(Sprite):
	def __init__(self):
		super().__init__()
		self.image = load(os.getcwd() + '/img/chain.png')
		self.rect = self.image.get_rect()