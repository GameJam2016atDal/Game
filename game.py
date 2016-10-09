#!/Users/Cheng/Developer/Python/PyGame/venv/bin/python
import pygame, os
from pygame.locals import *
from pygame.sprite import Sprite
from pygame.image import load

class platform(Sprite):
	def __init__(self):
		super().__init__()
		self.image = load(os.getcwd() + '/platform.png')
		self.rect = self.image.get_rect()

screenSize = (1440, 850)
fullScreen = False
screen = pygame.display.set_mode(screenSize, fullScreen)
cwd = os.getcwd()
thumbup = pygame.image.load(cwd + '/background.png')
coordinate = (0, 0)
screen.blit(thumbup, coordinate)
plat = platform()
spriteList = pygame.sprite.Group()
spriteList.add(plat)
spriteList.draw(screen)

pygame.display.flip()
while True:
	event = pygame.event.wait()
	if event.type == pygame.QUIT:
		break
pygame.quit()
