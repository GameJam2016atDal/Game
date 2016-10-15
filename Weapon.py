
from pygame.sprite import Sprite
from pygame.image import load
from Bullet import Bullet
from Grenade import Grenade
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
	def grenade_launcher(direction):
		g_l = grenade_launcher(direction)
		return g_l

	@staticmethod
	def baseballBat(direction):
		shortweapon = baseballBat(direction)
		return shortweapon

	@staticmethod
	def machineGun(direction):
		gun = machineGun(direction)
		return gun

	def shoot(self):
		bullet = Bullet(self.direction)
		bullet.rect.x, bullet.rect.y = self.rect.x, self.rect.y
		if self.direction > 0:
			bullet.rect.left = self.rect.right
		else:
			bullet.rect.right = self.rect.left
		self.shootingBullets.add(bullet)
		return bullet

	def launch(self):
		grenade = Grenade(self.direction)
		grenade.rect.x, grenade.rect.y = self.rect.x, self.rect.y
		if self.direction > 0:
			grenade.rect.left = self.rect.right+20
		else:
			grenade.rect.right = self.rect.left
		self.shootingBullets.add(grenade)
		return grenade


class grenade_launcher(Weapon):
	def __init__(self, direction):
		super().__init__(image = "grenade", direction = direction)

	def shoot(self):
		if len(self.shootingBullets) < 3:
			return super().launch()

	def changeDirection(self, direction):
		self.direction = direction


class machineGun(Weapon):
	def __init__(self, direction):
		name = 'normalGun-l' if direction == -1 else 'normalGun-r'
		super().__init__(image = name, direction = direction)

	def shoot(self):
		if len(self.shootingBullets) < 5:
			return super().shoot()

	def changeDirection(self, direction):
		name = 'normalGun-l' if direction == -1 else 'normalGun-r'
		self.image = load(os.getcwd() + '/img/' + name + '.png')
		self.direction = direction

class baseballBat(Weapon):
	def __init__(self, direction):
		super().__init__(image = "baseballBat", direction = direction)

	def shoot(self):
		# animation
		# if collision with player lose HP
		return super().shoot()
