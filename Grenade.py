from pygame.sprite import Sprite
from pygame.image import load
import os

class Grenade(Sprite):

    initial_y = None
    initial_x = None

    def __init__(self, direction):
        super().__init__()
        self.image = load(os.getcwd() + '/img/grenade.png')
        self.rect = self.image.get_rect()
        self.speed = 2
        self.direction = direction#1 for right, -1 for left

    def move(self):
        if not self.initial_y:
            self.initial_y = self.rect.y
        if not self.initial_x:
            self.initial_x = self.rect.x
        self.rect.x += self.speed * self.direction
        self.rect.y =  pow(abs( self.rect.x - self.initial_x ), 1.1) + self.initial_y
