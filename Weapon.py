import pygame
from pygame.sprite import Sprite
from pygame.image import load
from Bullet import Bullet
from Grenade import Grenade
from shotgunShell import shotgunShell
import os

class Weapon(Sprite):
	def __init__(self, image, direction):
		super().__init__()
		pygame.mixer.pre_init()
		self.name = image
		self.image = load(os.getcwd() + '/img/' + image + '.png')
		self.rect = self.image.get_rect()
		self.direction = direction
		self.shootingBullets = set()
		self.sound = pygame.mixer.Sound(os.getcwd() + '/music/'+image+'.wav')


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

	@staticmethod
	def shotgun(direction):
		sg = shotgun(direction)
		return sg

	def shoot(self):
		self.sound.play()
		bullet = Bullet(self.direction)
		bullet.rect.x, bullet.rect.y = self.rect.x, self.rect.y
		if self.direction > 0:
			bullet.rect.left = self.rect.right
		else:
			bullet.rect.right = self.rect.left
		self.shootingBullets.add(bullet)
		return bullet

	def launch(self):
		self.sound.play()
		grenade = Grenade(self.direction)
		grenade.rect.x, grenade.rect.y = self.rect.x, self.rect.y
		if self.direction > 0:
			grenade.rect.left = self.rect.right+25
		else:
			grenade.rect.right = self.rect.left
		self.shootingBullets.add(grenade)
		return grenade

	def shootshot(self): # if you know how to duplicate objects in python you can cut this code back lol
		self.sound.play()
		bullet = shotgunShell(self.direction)
		bullet_up = shotgunShell(self.direction)
		bullet_down = shotgunShell(self.direction)

		bullet.rect.x, bullet.rect.y = self.rect.x, self.rect.y
		bullet_up.rect.x, bullet_up.rect.y = self.rect.x, self.rect.y
		bullet_down.rect.x, bullet_down.rect.y = self.rect.x, self.rect.y

		if self.direction > 0:
			bullet.rect.left = self.rect.right
			bullet_up.rect.left = self.rect.right
			bullet_down.rect.left = self.rect.right
		else:
			bullet.rect.right = self.rect.left
			bullet_up.rect.right = self.rect.left
			bullet_down.rect.right = self.rect.left


		bullet_up.y = 1
		bullet_down.y = -1
		self.shootingBullets.add((bullet, bullet_up, bullet_down))
		return (bullet, bullet_up, bullet_down)


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

class shotgun(Weapon):
	def __init__(self, direction):
		name = 'shotgun-l' if direction == -1 else 'shotgun-r'
		super().__init__(image = name, direction = direction)

	def shoot(self):
		if len(self.shootingBullets) < 1:
			return super().shootshot()

	def changeDirection(self, direction):
		name = 'shotgun-l' if direction == -1 else 'shotgun-r'
		self.image = load(os.getcwd() + '/img/' + name + '.png')
		self.direction = direction

class baseballBat(Weapon):
	def __init__(self, direction):
		super().__init__(image = "baseballBat", direction = direction)

	def shoot(self):
		# animation
		# if collision with player lose HP
		return super().shoot()
