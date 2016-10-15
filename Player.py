from pygame.sprite import Sprite, spritecollide
from pygame import Surface
from Weapon import *

class player(Sprite):
	def __init__(self, platforms, elevator, weakLayer, sticks):
		super().__init__()
		self.image = Surface([50, 100])
		self.image.fill((0, 255, 0))
		self.rect = self.image.get_rect()
		self.xSpeed = 0
		self.ySpeed = 0
		self.platforms = platforms
		self.elevator = elevator
		self.sticks = sticks
		self.weakLayer = weakLayer
		self.hp = 100
		self.weapon = Weapon.baseballBat(direction = 1)
		self.direction = 0 # 0 for stop, 1 for right, -1 for left

	def update(self):
		self.calc_grav()
		move = self._sliding()
		if move > 4:
			move = 4
		elif move < -4:
			move = -4
		self.rect.x += move
		self.weapon.rect.x, self.weapon.rect.y = self.rect.x - 5, self.rect.y - 5
		self.weapon.rect.x += move
		self.weapon.update()

		block_hit_list = spritecollide(self, self.platforms, False)
		self._preventMoving(block_hit_list)
		weakLayer_list = spritecollide(self, self.weakLayer, False)
		for each in weakLayer_list:
			if self.ySpeed > 0:
				self.rect.bottom = each.rect.top
			elif self.ySpeed < 0:
				self.rect.top = each.rect.bottom
			self.ySpeed = 0

		self.rect.y += self.ySpeed
		block_hit_list = spritecollide(self, self.platforms, False)
		for block in block_hit_list:
			if self.ySpeed > 0:
				self.rect.bottom = block.rect.top
			elif self.ySpeed < 0:
				self.rect.top = block.rect.bottom
			self.ySpeed = 0

		sticks_hit_list = spritecollide(self, self.sticks, False)

		for stick in sticks_hit_list:
			#lose hp
			#unhurtful for 2 seconds
			pass

		elevator_hit_list = spritecollide(self, self.elevator, False)
		for each in elevator_hit_list:
			if self.rect.bottom >= each.rect.top:
				self.ySpeed = each.speed

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

	def go_right(self):
		self.direction = 1

	def stop(self):
		self.direction = 0

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
