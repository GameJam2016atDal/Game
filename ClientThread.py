from threading import Thread
from Player import player

class ClientThread(Thread):
	def __init__(self, client, player, bulletList):
		Thread.__init__(self)
		self.client = client
		self.bulletList = bulletList
		self.player = player

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
				bullet = self.player.weapon.shoot()
				if not bullet is None:
					self.bulletList.add(bullet)
			if data == b'4':
				self.player.stop()
		self.client.close()	
