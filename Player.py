from pygame.sprite import Sprite, spritecollide
from pygame.image import load
import os
import pygame
from pygame.time import get_ticks
from Weapon import *
from random import randint

class player(Sprite):
	def __init__(self, platforms, elevator, weakLayer, bulletList, sticks, giantSpike):
		super().__init__()
		pygame.mixer.pre_init()
		self.spriteName = 'b'
		self.image = load(os.getcwd() + '/img/sprite-' + self.spriteName + '/' + self.spriteName + '-r1.png')
		self.rect = self.image.get_rect()
		self.xSpeed = 0
		self.ySpeed = 0
		self.platforms = platforms
		self.elevator = elevator
		self.sticks = sticks
		self.weakLayer = weakLayer
		self.bulletList = bulletList
		self.hp = 100
		self.weapon = Weapon.machineGun(direction = 1)
		self.direction = 0 # 0 for stop, 1 for right, -1 for left
		self.unhurtful = False # When player is hit, there are 1 sec for him to be unhurtful
		self.start_tick = None
		self.spriteCount = 0
		self.hit_sound = pygame.mixer.Sound(os.getcwd() + '/music/hit.wav')
		self.death_sound = pygame.mixer.Sound(os.getcwd() + '/music/death.wav')
		self.giantSpike = giantSpike

	def update(self):

		if not self.start_tick is None:
			currentTime = get_ticks()
			if self.hp > 0:
				if (currentTime - self.start_tick) / 1000 > 1:
					self.unhurtful = False
					# Revert back
					self._updateSprite()
			else:
				if (currentTime - self.start_tick) / 1000 > 5:
					initialLocations = [(968, 400), (280, 400), (968, 250), (280, 250)]
					self.image = load(os.getcwd() + '/img/sprite-' + self.spriteName + '/' + self.spriteName + '-r1.png')
					initialLocation = initialLocations[randint(0, 3)]
					self.rect.x, self.rect.y = initialLocation
					self.weapon.rect.x, self.weapon.rect.y = self.rect.x, self.rect.y
					self.hp = 100
				else:
					self.image = load(os.getcwd() + '/img/sprite-' + self.spriteName + '/d.png')
					self.weapon.rect.right = self.rect.left
					return
		self._updateSprite()
		self.calc_grav()
		if self.rect.right > 1440:
			self.rect.right = 1440
		if self.rect.left < 0:
			self.rect.left = 0
		move = self._sliding()
		if move > 4:
			move = 4
		elif move < -4:
			move = -4
		self.rect.x += move
		self.weapon.update()
		self.weapon.rect.y = self.rect.y + 50
		if self.direction == 1:
			self.weapon.rect.x = self.rect.x + 20
		elif self.direction == -1:
			self.weapon.rect.x = self.rect.x - 30
		self.weapon.rect.x += move
		self.weapon.update()

		weakLayer_list = spritecollide(self, self.weakLayer, False)
		for each in weakLayer_list:
			if self.ySpeed > 0:
				self.rect.bottom = each.rect.top
			elif self.ySpeed < 0:
				self.rect.top = each.rect.bottom
			self.ySpeed = 0

		block_hit_list = spritecollide(self, self.platforms, False)
		self._preventMoving(block_hit_list)

		self.rect.y += self.ySpeed
		block_hit_list = spritecollide(self, self.platforms, False)
		for block in block_hit_list:
			if self.ySpeed > 0:
				self.rect.bottom = block.rect.top
			elif self.ySpeed < 0:
				self.rect.top = block.rect.bottom
			self.ySpeed = 0

		sticks_hit_list = spritecollide(self, self.sticks, False)
		if len(sticks_hit_list) > 0:
			if self.unhurtful == False:
				self.start_tick = get_ticks()
				self._updateSprite()
				self.hp -= 10
				self.hit_sound.play()
				if self.hp <= 0:
					#death
					self.death_sound.play()
				else:
					self.unhurtful = True

		bullet_hit_list = spritecollide(self, self.bulletList, False)
		for each in bullet_hit_list:
			if self.unhurtful == False :
				self.start_tick = get_ticks()
				self._updateSprite()
				self.hp -= 20
				self.hit_sound.play()
				if self.hp <= 0:
					#death
					self.death_sound.play()
				else:
					self.unhurtful = True

		elevator_hit_list = spritecollide(self, self.elevator, False)
		for each in elevator_hit_list:
			if self.rect.bottom < each.rect.top:
				self.ySpeed = each.speed
			else:
				self.rect.bottom = each.rect.top

		giantSpike_hit_list = spritecollide(self, self.giantSpike, False)
		for each in giantSpike_hit_list:
			if each.rect.bottom >= self.rect.top and self.unhurtful == False:
				self.start_tick = get_ticks()
				self._updateSprite()
				self.hp -= 90
				self.hit_sound.play()
				if self.hp <= 0:
					#Dead
					self.death_sound.play()
				else:
					self.unhurtful = True


	def _updateSprite(self):
		if self.spriteCount == 3:
			self.spriteCount = 0
		pic = os.getcwd() + '/img/sprite-'
		pic += self.spriteName + '/' + self.spriteName + '-'
		if self.direction == 1:
			pic += 'r'
		elif self.direction == -1:
			pic += 'l'
		else:
			return
		pic += str(self.spriteCount)
		if self.unhurtful == True:
			pic += 'h'
		pic += '.png'
		self.spriteCount += 1
		self.image = load(pic)

	def _preventMoving(self, obstacle):
		for each in obstacle:
			if self.xSpeed > 0:
				self.rect.right = each.rect.left
			elif self.xSpeed < 0:
				self.rect.left = each.rect.right
			self.xSpeed = 0

	def calc_grav(self):
		if self.ySpeed == 0:
			self.ySpeed = 1
		else:
			self.ySpeed += .35
		if self.rect.y >= 850 - self.rect.height and self.ySpeed >= 0:
			self.ySpeed = 0
			self.rect.y = 850 - self.rect.height

	def jump(self):
		self.rect.y += 1.3
		platform_hit_list = spritecollide(self, self.platforms, False)
		weakLayer_list = spritecollide(self, self.weakLayer, False)
		elevator_list = spritecollide(self, self.elevator, False)
		self.rect.y -= 1.3

		if len(platform_hit_list) > 0 or len(weakLayer_list) > 0 or len(elevator_list) > 0:
			self.ySpeed = -9


	def go_left(self):
		self.direction = -1
		self.weapon.changeDirection(self.direction)

	def go_right(self):
		self.direction = 1
		self.weapon.changeDirection(self.direction)

	def stop(self):
		self.direction = 0
		self.spriteCount = 0

	def _sliding(self):
		slidingRatio = 0.15
		maxSpeed = 4
		if self.direction != 0 and (self.xSpeed == maxSpeed or self.xSpeed == -maxSpeed):
			return self.xSpeed
		if self.direction == -1:
			if self.xSpeed > 0:
				self.xSpeed = 0
			self.xSpeed -= slidingRatio
			return self.xSpeed
		elif self.direction == 1:
			if self.xSpeed < 0:
				self.xSpeed = 0
			self.xSpeed += slidingRatio
			return self.xSpeed
		else:
			if self.xSpeed > 0.1:
				self.xSpeed -= slidingRatio
			elif self.xSpeed < 0.1:
				self.xSpeed += slidingRatio
			else:
				self.xSpeed = 0
			return self.xSpeed
