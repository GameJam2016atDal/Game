from pygame.sprite import Sprite
from pygame.image import load
from Bullet import Bullet
import os
import copy

class shotgunShell(Bullet):
    def __init__(self, direction):
        super().__init__(direction)
        self.image = load(os.getcwd() + '/img/bullet.png')
        self.rect = self.image.get_rect()
        self.speed = 6
        self.initial_x = None
        self.bounced = False
        self.direction = direction#1 for right, -1 for left
        self.y = 0

    def outOfRange(self):
        if abs(self.rect.x - self.initial_x) > 150:
            return True
        else:
            return False


    def move(self):
        if not self.initial_x:
            self.initial_x = self.rect.x
        if self.y == 1:
            self.rect.x += self.speed * self.direction * 0.5
            self.rect.y += self.speed * self.direction * 0.5
        elif self.y == -1:
            self.rect.x += self.speed * self.direction * 0.5
            self.rect.y -= self.speed * self.direction * 0.5
        else:
            self.rect.x += self.speed * self.direction
