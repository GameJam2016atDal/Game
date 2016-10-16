from pygame.sprite import Sprite
from pygame.image import load
from Bullet import Bullet
import os

class Grenade(Bullet):

    def __init__(self, direction):
        super().__init__(direction)
        self.image = load(os.getcwd() + '/img/grenade.png')
        self.rect = self.image.get_rect()
        self.speed = 6
        self.initial_y = None
        self.initial_x = None
        self.bounced = False
        self.direction = direction#1 for right, -1 for left


    def move(self):
        if not self.bounced:
            if not self.initial_y:
                self.initial_y = self.rect.y
            if not self.initial_x:
                self.initial_x = self.rect.x
            self.rect.x += self.speed * self.direction
            self.rect.y =  pow(abs( self.rect.x - self.initial_x ), 1.1) + self.initial_y
        else:
            self.rect.x += self.speed * self.direction
            self.rect.y += -1 * abs(self.speed * self.direction)
