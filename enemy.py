import pygame as pg
from pygame.math import Vector2

class Enemy(pg.sprite.Sprite):
    def __init__ (self, waypoints, image):
        pg.sprite.Sprite.__init__(self)
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])
        self.target_waypoint = 1
        self.speed = 2
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self):
        self.move()

    def move(self):
        #define target waypoint
        self.taget = Vector2(self.waypoints[self.target_waypoint])
        self.movement = self.target - self.pos

        # calc distance to target
        dist = self.movement.length()
        # check if remaining distance is greater then speed
        if dist >= self.speed:
            self.pos += self.movement.normalize() * self.speed
        else:
            self.pos += self.movement.normalize() * dist
            self.target_waypoint += 1

        self.rect.center = self.pos
