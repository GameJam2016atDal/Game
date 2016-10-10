#!/Users/Cheng/Developer/Python/PyGame/venv/bin/python
import pygame, os
from pygame.locals import *
from pygame.sprite import Sprite
from pygame.image import load

screenSize = (1440, 850)
fullScreen = False
screen = pygame.display.set_mode(screenSize, fullScreen)
cwd = os.getcwd()
thumbup = pygame.image.load(cwd + '/img/background.png')
coordinate = (0, 0)
screen.blit(thumbup, coordinate)

class platform(Sprite):
	def __init__(self):
		super().__init__()
		self.image = load(os.getcwd() + '/img/platform1.png')
		self.rect = self.image.get_rect()

plat = platform()
plat.rect.y = 700
spriteList = pygame.sprite.Group()
spriteList.add(plat)
spriteList.draw(screen)

class player(Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.Surface([50, 100])
		self.image.fill((0, 255, 0))
		self.rect = self.image.get_rect()
		self.xSpeed = 0
		self.ySpeed = 0

	def update(self):
		self.calc_grav()
		self.rect.x += self.xSpeed
		block_hit_list = pygame.sprite.spritecollide(self, spriteList, False)
		for block in block_hit_list:
			if self.xSpeed > 0:
				self.rect.right = block.rect.left
			elif self.xSpeed < 0:
				self.rect.left = block.rect.right

		self.rect.y += self.ySpeed
		block_hit_list = pygame.sprite.spritecollide(self, spriteList, False)
		for block in block_hit_list:
			if self.ySpeed > 0:
				self.rect.bottom = block.rect.top
			elif self.ySpeed < 0:
				self.rect.top = block.rect.bottom
			self.ySpeed = 0
	
	def calc_grav(self):
		self.ySpeed = 1 if self.ySpeed == 0 else 0.35	
		if self.rect.y >= 850 - self.rect.height and self.ySpeed >= 0:
			self.ySpeed = 0
			self.rect.y = 850 - self.rect.height

	def jump(self):
		self.rect.y += 2
		platform_hit_list = pygame.sprite.spritecollide(self, spriteList, False)
		self.rect.y -= 2
		if len(platform_hit_list) > 0 or self.rect.bottom >= 850:
			self.ySpeed = -10
	
	def go_left(self):
		self.xSpeed = -6
	
	def go_right(self):
		self.xSpeed = 6
	
	def stop(self):
		self.xSpeed = 0

# Player = player()

# Player.rect.x = 30
# Player.rect.y = 500
# activeList = pygame.sprite.Group()
# activeList.add(Player)
# clock = pygame.time.Clock()
# activeList.draw(screen)

while True:
	event = pygame.event.wait()
	if event.type == pygame.QUIT:
		break
	if event.type == pygame.KEYDOWN:
		if event.key == pygame.K_LEFT:
			print('left')
			Player.go_left()
		if event.key == pygame.K_RIGHT:
			print('right')
			Player.go_right()
		if event.key == pygame.K_UP:
			Player.jump()
	# activeList.update()
	# activeList.draw(screen)
	clock.tick(60)
	pygame.display.flip()
pygame.quit()
