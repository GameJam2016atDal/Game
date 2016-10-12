#!/Users/Cheng/Developer/Python/PyGame/venv/bin/python
import pygame, os
#from pygame.locals import *
from pygame.sprite import Sprite
from pygame.image import load

BGCOLOUR = (249, 250, 255)

class platform(Sprite):
	def __init__(self, img):
		super().__init__()
		self.image = load(os.getcwd() + '/img/' + img + '.png')
		self.rect = self.image.get_rect()

	@staticmethod
	def generatePlatforms():
		imgs = ['platform1', 'layer2_l', 'layer2', 'pillar_l', 'pillar_r', 'shortStage', 'shortStage', 'shortStage', 'shortStage', 'topStage', 'topStage']
		coordinates = [(0, 800), (270, 690), (780, 690), (270, 700), (1100, 700), (300, 500), (840, 500), (300, 350), (840, 350), (170, 200), (780, 200)]
		platFormList = list()
		for (eachImg, eachCoordinate) in zip(imgs, coordinates):
			plat = platform(img = eachImg)
			plat.rect.x, plat.rect.y = eachCoordinate
			platFormList.append(plat)
		return platFormList

	@staticmethod
	def generateSticks():
		imgs = ['sticks', 'sticks', 'bottomSticks']
		coordinates = [(0, 690), (1330, 690), (350, 720)]
		stickList = list()
		for (eachImg, eachCoordinate) in zip(imgs, coordinates):
			stick = platform(img = eachImg)
			stick.rect.x, stick.rect.y = eachCoordinate
			stickList.append(stick)
		return stickList

class player(Sprite):
	def __init__(self, platforms, sticks):
		super().__init__()
		self.image = pygame.Surface([50, 100])
		self.image.fill((0, 255, 0))
		self.rect = self.image.get_rect()
		self.xSpeed = 0
		self.ySpeed = 0
		self.platforms = platforms
		self.sticks = sticks

	def update(self):
		self.calc_grav()
		self.rect.x += self.xSpeed
		block_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
		for block in block_hit_list:
			if self.xSpeed > 0:
				self.rect.right = block.rect.left
			elif self.xSpeed < 0:
				self.rect.left = block.rect.right

		self.rect.y += self.ySpeed
		block_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
		for block in block_hit_list:
			if self.ySpeed > 0:
				self.rect.bottom = block.rect.top
			elif self.ySpeed < 0:
				self.rect.top = block.rect.bottom
			self.ySpeed = 0
	
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
		platform_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
		self.rect.y -= 1.3
		if len(platform_hit_list) > 0 or self.rect.bottom >= 850:
			self.ySpeed = -9
	
	def go_left(self):
		self.xSpeed = -4
	
	def go_right(self):
		self.xSpeed = 4
	
	def stop(self):
		self.xSpeed = 0

def main():
	pygame.init()
	screenSize = (1440, 850)
	fullScreen = False
	screen = pygame.display.set_mode(screenSize, fullScreen)
	cwd = os.getcwd()
	screen.fill(BGCOLOUR)

	platformList = pygame.sprite.Group()
	plats = platform.generatePlatforms()
	for plat in plats:
		platformList.add(plat)
	platformList.draw(screen)

	stickList = pygame.sprite.Group()
	sticks = platform.generateSticks()
	for stick in sticks:
		stickList.add(stick)
	stickList.draw(screen)

	Player = player(platforms = platformList, sticks = stickList)

	Player.rect.x = 30
	Player.rect.y = 500
	plat.player = Player
	platformList.add(plat)
	activeList = pygame.sprite.Group()
	activeList.add(Player)
	clock = pygame.time.Clock()
	gaming = True

	while gaming:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gaming = False
				break
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					gaming = False
					break
				if event.key == pygame.K_LEFT:
					Player.go_left()
				if event.key == pygame.K_RIGHT:
					Player.go_right()
				if event.key == pygame.K_UP:
					Player.jump()
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT and Player.xSpeed < 0:
					Player.stop()
				if event.key == pygame.K_RIGHT and Player.xSpeed > 0:
					Player.stop()
		screen.fill(BGCOLOUR)
		platformList.draw(screen)
		activeList.update()
		activeList.draw(screen)
		stickList.update()
		stickList.draw(screen)
		clock.tick(60)
		pygame.display.flip()
	pygame.quit()

if __name__ == '__main__':
	main()
