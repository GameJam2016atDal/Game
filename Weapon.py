
from pygame.sprite import Sprite
from pygame.image import load
import os

class Bullet(Sprite):
	def __init__(self, direction):
		super().__init__()
		self.image = load(os.getcwd() + '/img/bullet.png')
		self.rect = self.image.get_rect()
		self.speed = 2
		self.direction = direction#1 for right, -1 for left

	def move(self):
		self.rect.x += self.speed * self.direction

class Weapon(Sprite):
	def __init__(self, image, direction):
		super().__init__()
		self.image = load(os.getcwd() + '/img/' + image + '.png')
		self.rect = self.image.get_rect()
		self.direction = direction
		self.shootingBullets = set()

	def shoot(self):
		bullet = Bullet(self.direction)
		bullet.rect.left = self.rect.right
		self.shootingBullets.add(bullet)

	def update(self):
		for each in self.shootingBullets:
			each.move()