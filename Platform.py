from pygame.sprite import Sprite
from pygame.image import load
import os

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