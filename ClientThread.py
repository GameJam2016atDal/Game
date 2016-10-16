from threading import Thread
from Player import player
from Weapon import *

class ClientThread(Thread):
	def __init__(self, client, player, bulletList, playerList):
		Thread.__init__(self)
		self.client = client
		self.bulletList = bulletList
		self.player = player
		self.playerList = playerList

	def run(self):
		self.client.send(b"Success")
		while True:
			data = self.client.recv(10).strip()
			if not data:
				break
			print(data)
			if data == b'0':
				self.player.go_left()
			if data == b'1':
				self.player.jump()
			if data == b'2':
				self.player.go_right()
			if data == b'3':
				if self.player.dead == False:
					bullet = self.player.weapon.shoot()
					if not bullet is None:
						self.bulletList.add(bullet)
			if data == b'4':
				self.player.stop()
			if data.endswith(b'4'):
				self.player.stop()
			if data == b'5':
				self.playerList.remove(self.player.weapon)
				self.player.weapon = Weapon.machineGun(1)
				self.player.weapon.rect.x = self.player.rect.x + 50
				self.player.weapon.update()
				self.playerList.add(self.player.weapon)
			if data == b'6':
				self.playerList.remove(self.player.weapon)
				self.player.weapon = Weapon.grenade_launcher(direction = 1)
				self.player.weapon.rect.x = self.player.rect.x + 50
				self.player.weapon.update()
				self.playerList.add(self.player.weapon)
			if data == b'7':
				self.playerList.remove(self.player.weapon)
				self.player.weapon = Weapon.shotgun(direction = 1)
				self.player.weapon.rect.x = self.player.rect.x + 50
				self.player.weapon.update()
				self.playerList.add(self.player.weapon)
		self.client.close()	
