
from pygame.sprite import Sprite, spritecollide
from pygame.image import load
import os

class Elevator(Sprite):
	def __init__(self, image):
		super().__init__()
		self.image = load(os.getcwd() + '/img/' + image + '.png')
		self.rect = self.image.get_rect()
		self.speed = 2
		self._Top = 200
		self._Bottom = 670
	
	@staticmethod
	def generateElevators():
		imgs = ['elevator', 'elevator']
		coordinators = [(20, 670), (1260, 670)]
		elevatorList = list()
		for (eachImg, eachCoordinate) in zip(imgs, coordinators):
			elevator = Elevator(image = eachImg)
			elevator.rect.x, elevator.rect.y = eachCoordinate
			elevatorList.append(elevator)
		return elevatorList
		
	def move(self):
		if self.rect.y <= self._Top or self.rect.y >= self._Bottom:
			self.speed *= -1
		self.rect.y += self.speed
