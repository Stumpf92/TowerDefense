import pygame as pg
import constants as c

class Turret(pg.sprite.Sprite):

    def __init__ (self, sprite_sheet, tile_x, tile_y):
        pg.sprite.Sprite.__init__(self)

        self.cooldown = 1500
        self.last_shot = pg.time.get_ticks()

        ###position variables 
        self.tile_x = tile_x
        self.tile_y = tile_y
        #calc center coordinate:
        self.x = (self.tile_x + 0.5) * c.TILE_SIZE
        self.y = (self.tile_y + 0.5) * c.TILE_SIZE


        #animation variables
        self.sprite_sheet = sprite_sheet
        self.animation_list = self.load_images()
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()

        #update image
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)


    def load_images(self):
        #extract images from spritsheet 
        size = self.sprite_sheet.get_height()
        animation_list = []
        for _ in range(c.ANIMATION_STEPS):
            temp_img = self.sprite_sheet.subsurface(_*size,0,size,size)
            animation_list.append(temp_img)
        return animation_list
    
    def update(self):
        if pg.time.get_ticks() - self.last_shot > self.cooldown:
            self.play_animation()
    

    def play_animation(self):
        #update iamge
        self.image = self.animation_list[self.frame_index]
        if pg.time.get_ticks() - self.update_time > c.ANIMATION_DELAY:
            self.update_time = pg.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0   
            self.last_shot = pg.time.get_ticks() 