import pygame
import socket
import sys
import os
from ClientThread import ClientThread
from Platform import platform
from Player import player
from Elevator import Elevator
from weakLayer import weakLayer
from random import randint
from Grenade import Grenade
from pygame.time import get_ticks
from giantSpike import giantSpike
from Weapon import *

class game:
	def __init__(self, screenSize, fullScreen = False, backgroundColour = (249, 250, 255)):
		pygame.init()
		self._bgColour = backgroundColour
		self.screenSize = screenSize
		self.screen = pygame.display.set_mode(screenSize, fullScreen)
		self.screen.fill(self._bgColour)
		self.playerList = None
		self._generatePlatform()
		self._generateSticks()
		self._generateElevators()
		self._generateWeakLayer()
		self._generateGiantSpike()
		self.bulletList = pygame.sprite.Group()
		self.weakLayerBrokenTime = None
		self.characterList = ['a', 'b', 'c', 'x', 'y', 'z']
		self.usedCharacters = set()
		try:
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.socket.bind(('0.0.0.0', 7777))
		except:
			print('Connection Error')

	def _generateGiantSpike(self):
		self.giantSpike = giantSpike()
		self.giantSpikeList = pygame.sprite.Group()
		self.giantSpikeList.add(self.giantSpike)
		self.giantSpikePlat = Elevator('elevator')
		self.giantSpikePlat.speed = 0
		self.giantSpikePlat.rect.x, self.giantSpikePlat.rect.y = self.giantSpike.rect.x + 10, self.giantSpike.rect.y - 5
		self.giantSpike.plat = self.giantSpikePlat
		self.elevatorList.add(self.giantSpikePlat)
		self.chainGroup = pygame.sprite.Group()
		self.chainGroup.add(self.giantSpike.chain)

	def _generatePlatform(self):
		self.platformList = pygame.sprite.Group()
		plats = platform.generatePlatforms()
		for plat in plats:
			self.platformList.add(plat)

	def _generateSticks(self):
		self.stickList = pygame.sprite.Group()
		sticks = platform.generateSticks()
		for stick in sticks:
			self.stickList.add(stick)

	def _generateElevators(self):
		self.elevatorList = pygame.sprite.Group()
		self.elevators = Elevator.generateElevators()
		for each in self.elevators:
			self.elevatorList.add(each)

	def _generateWeakLayer(self):
		self.weakLayer = weakLayer()
		self.weakLayerGroup = pygame.sprite.Group()
		self.weakLayerGroup.add(self.weakLayer)

	def addPlayer(self):
		charRand = randint(0, 5)
		while charRand in self.usedCharacters:
			charRand = randint(0, 5)
		name = self.characterList[charRand]
		Player = player(character = name, platforms = self.platformList, elevator = self.elevatorList, weakLayer = self.weakLayerGroup, bulletList = self.bulletList, sticks = self.stickList, giantSpike = self.giantSpikeList)
		initialLocations = [(968, 400), (280, 400), (968, 250), (280, 250)]
		initialLocation = initialLocations[randint(0, 3)]
		Player.rect.x, Player.rect.y = initialLocation
		Player.weapon.rect.x, Player.weapon.rect.y = initialLocation
		if self.playerList is None:
			self.playerList = pygame.sprite.Group()
		self.playerList.add(Player)
		self.playerList.add(Player.weapon)
		return Player

		# self.Player = player(platforms = self.platformList, elevator = self.elevatorList, weakLayer = self.weakLayerGroup, bulletList = self.bulletList, sticks = self.stickList, giantSpike = self.giantSpikeList)
		# initialLocations = [(968, 400), (280, 400), (968, 250), (280, 250)]
		# initialLocation = initialLocations[randint(0, 3)]
		# self.Player.rect.x, self.Player.rect.y = initialLocation
		# self.Player.weapon.rect.x, self.Player.weapon.rect.y = initialLocation
		# if self.playerList is None:
		# 	self.playerList = pygame.sprite.Group()
		# self.playerList.add(self.Player)
		# self.playerList.add(self.Player.weapon)

	def _update(self):
		self.screen.fill(self._bgColour)
		self.platformList.update()
		self.platformList.draw(self.screen)
		self.elevatorList.update()
		self.elevatorList.draw(self.screen)

		currentTime = get_ticks()
		if not self.weakLayerBrokenTime is None and (currentTime - self.weakLayerBrokenTime) / 1000 > 10:
			self._generateWeakLayer()
			for each in self.playerList:
				try:
					each.weakLayer = self.weakLayerGroup
				except:
					pass

		for each in self.elevators:
			if each.rect.x != 630:
				each.move()
		for each in self.bulletList:
			each.move()

			if isinstance(each, shotgunShell):
				if each.outOfRange():

					self.bulletList.remove(each)
					for eachPlayer in self.playerList:
						try:
							print("out of range")
							eachPlayer.shootingBullets.remove(each)
						except:
							pass

			giantSpike_hit_list = pygame.sprite.spritecollide(each, self.giantSpikeList, False)
			if len(giantSpike_hit_list) > 0:
				self.bulletList.remove(each)
				for eachPlayer in self.playerList:
					try:
						eachPlayer.shootingBullets.remove(each)
					except:
						pass
				if self.giantSpike.moveUp == False:
					self.giantSpike.startTime = get_ticks()
					self.giantSpike.movable = True

			weak_hit_list = pygame.sprite.spritecollide(each, self.weakLayerGroup, True)
			if len(weak_hit_list) > 0:
				self.weakLayerBrokenTime = get_ticks()
				self.bulletList.remove(each)
				for eachPlayer in self.playerList:
					try:
						eachPlayer.shootingBullets.remove(each)
					except:
						pass

			block_hit_list = pygame.sprite.spritecollide(each, self.platformList, False)
			elevator_hit_list = pygame.sprite.spritecollide(each, self.elevatorList, False)

			if len(block_hit_list) > 0 or len(elevator_hit_list) > 0:
				if isinstance(each, Grenade) and not each.bounced:
					each.bounced = True
					each.move()
					each.move()
					each.move()
				else:
					self.bulletList.remove(each)
					for eachPlayer in self.playerList:
						try:
							print("hit block")
							eachPlayer.shootingBullets.remove(each)
						except:
							pass
			if each.rect.right >= 1440 or each.rect.left <= 0:
				self.bulletList.remove(each)
				for eachPlayer in self.playerList:
					try:
						print("out of bounds")
						eachPlayer.shootingBullets.remove(each)
					except:
						pass

		weak_hit_list = pygame.sprite.spritecollide(self.giantSpike, self.weakLayerGroup, True)
		if len(weak_hit_list) > 0:
			self.weakLayerBrokenTime = get_ticks()
		# if self.giantSpike.moveUp == False and self.giantSpike.movable == False and len(self.weakLayerGroup) == 0:
		# 	self._generateWeakLayer()

		self.bulletList.update()
		self.bulletList.draw(self.screen)
		self.playerList.update()
		self.playerList.draw(self.screen)
		self.stickList.update()
		self.stickList.draw(self.screen)
		self.weakLayerGroup.update()
		self.weakLayerGroup.draw(self.screen)
		self.giantSpikeList.update()
		self.giantSpikeList.draw(self.screen)
		self.chainGroup.update()
		self.chainGroup.draw(self.screen)
		pygame.display.flip()

	def start(self):
		self.socket.listen(10)
		clock = pygame.time.Clock()
		self.gaming = True

		pygame.mixer.music.load(os.getcwd()+'/music/Androids.wav')
		pygame.mixer.music.play(-1)
		pygame.mixer.music.set_volume(0.25)
		self.begin = False
		addressSet = set()
		playerCount = 0
		while self.begin != True:
			client, addr = self.socket.accept()
			if not client is None and not (addr in addressSet):
				addressSet.add(addr)
				player = self.addPlayer()
				playerCount += 1
				thread = ClientThread(client, player, self.bulletList, self.playerList)
				thread.start()
			print(playerCount)
			if playerCount == 2:
				self.begin = True
		while self.gaming:
		# 	for event in pygame.event.get():
		# 		if event.type == pygame.QUIT:
		# 			self.gaming = False
		# 			break
		# 		if event.type == pygame.KEYDOWN:
		# 			if event.key == pygame.K_ESCAPE:
		# 				self.gaming = False
		# 				break
		# 			if event.key == pygame.K_LEFT:
		# 				self.Player.go_left()
		# 			if event.key == pygame.K_RIGHT:
		# 				self.Player.go_right()
		# 			if event.key == pygame.K_UP:
		# 				self.Player.jump()
		# 			if event.key == pygame.K_SPACE:
		# 				bullet = self.Player.weapon.shoot()
		# 				if not bullet is None:
		# 					self.bulletList.add(bullet)
		# 			if event.key == pygame.K_1:
		# 				self.playerList.remove(self.Player.weapon)
		# 				self.Player.weapon = Weapon.machineGun(1)
		# 				self.Player.weapon.rect.x = self.Player.rect.x + 50
		# 				self.Player.weapon.update()
		# 				self.playerList.add(self.Player.weapon)
		# 			if event.key == pygame.K_2:
		# 				self.playerList.remove(self.Player.weapon)
		# 				self.Player.weapon = Weapon.grenade_launcher(direction = 1)
		# 				self.Player.weapon.rect.x = self.Player.rect.x + 50
		# 				self.Player.weapon.update()
		# 				self.playerList.add(self.Player.weapon)

		# 		if event.type == pygame.KEYUP:
		# 			if event.key == pygame.K_LEFT and self.Player.xSpeed < 0:
		# 				self.Player.stop()
		# 			if event.key == pygame.K_RIGHT and self.Player.xSpeed > 0:
		# 				self.Player.stop()
			clock.tick(60)
			self._update()
		pygame.quit()
