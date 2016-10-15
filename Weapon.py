
from pygame.sprite import Sprite
from pygame.image import load
from Bullet import Bullet
import os

class Weapon(Sprite):
	def __init__(self, image, direction):
		super().__init__()
		self.name = image
		self.image = load(os.getcwd() + '/img/' + image + '.png')
		self.rect = self.image.get_rect()
		self.direction = direction
		self.shootingBullets = set()

	@staticmethod
	def baseballBat(direction):
		shortweapon = baseballBat(direction)
		return shortweapon

	@staticmethod
	def machineGun(direction):
		gun = machineGun(direction)
		return gun

	def shoot(self):
		#if
		bullet = Bullet(self.direction)
		bullet.rect.x, bullet.rect.y = self.rect.x, self.rect.y
		bullet.rect.left = self.rect.right
		self.shootingBullets.add(bullet)
		return bullet



class machineGun(Weapon):
	def __init__(self, direction):
		name = 'normalGun-l' if direction == -1 else 'normalGun-r'
		super().__init__(image = name, direction = direction)

	def shoot(self):
		if len(self.shootingBullets) < 5:
<<<<<<< HEAD
			super().shoot()

class baseballBat(Weapon):
	def __init__(self, direction):
		super().__init__(image = "baseballBat", direction = direction)

	def shoot(self):
		# animation
		# if collision with player lose HP
=======
			return super().shoot()

	def changeDirection(self, direction):
		name = 'normalGun-l' if direction == -1 else 'normalGun-r'
		self.image = load(os.getcwd() + '/img/' + name + '.png')
		self.direction = direction
>>>>>>> 81dc9e22972dc1cfd21404817028349baa851ffb
