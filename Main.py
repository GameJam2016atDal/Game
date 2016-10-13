from game import game

if __name__ == '__main__':
	Game = game(screenSize = (1440, 850))
	Game.addPlayer()
	Game.start()