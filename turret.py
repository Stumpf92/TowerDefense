import pygame as pg
import constants as c
import math
from turret_data import TURRET_DATA

class Turret(pg.sprite.Sprite):

    def __init__ (self, sprite_sheets, tile_x, tile_y, shot_fx):
        pg.sprite.Sprite.__init__(self)
        self.upgrade_level = 1
        self.range = TURRET_DATA[self.upgrade_level - 1].get("range")
        self.cooldown = TURRET_DATA[self.upgrade_level - 1].get("cooldown")
        self.last_shot = pg.time.get_ticks()
        self.selected = False
        self.target = None


        ###position variables 
        self.tile_x = tile_x
        self.tile_y = tile_y
        #calc center coordinate:
        self.x = (self.tile_x + 0.5) * c.TILE_SIZE
        self.y = (self.tile_y + 0.5) * c.TILE_SIZE

        self.shot_fx = shot_fx


        #animation variables
        self.sprite_sheets = sprite_sheets
        self.animation_list = self.load_images(self.sprite_sheets[self.upgrade_level-1])
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()

        #update image
        self.angle = 90
        self.original_image = self.animation_list[self.frame_index]
        self.image = pg.transform.rotate(self.original_image,self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)

        #create transparent circle to visualize turret range
        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0,0,0,))
        self.range_image.set_colorkey((0,0,0))
        pg.draw.circle(self.range_image, "grey100", (self.range,self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center


    def load_images(self, sprite_sheet):
        #extract images from spritsheet 
        size = sprite_sheet.get_height()
        animation_list = []
        for _ in range(c.ANIMATION_STEPS):
            temp_img = sprite_sheet.subsurface(_*size,0,size,size)
            animation_list.append(temp_img)
        return animation_list
    
    def update(self, enemy_group, world):
        if self.target:
            self.play_animation()
        else:
            if pg.time.get_ticks() - self.last_shot > (self.cooldown / world.game_speed):
                self.pick_target(enemy_group)
            
    
    def pick_target(self, enemy_group):
        x_dist = 0
        y_dist = 0
        for _ in enemy_group:
            if _.health > 0:
                x_dist = _.pos[0] - self.x
                y_dist = _.pos[1] - self.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if dist < self.range:
                    self.target = _
                    self.angle = math.degrees(math.atan2(-y_dist,x_dist))
                    #damage enemy
                    self.target.health -= c.DAMAGE
                    #play soundeffect
                    self.shot_fx.play()
                    break



    def play_animation(self):
        #update iamge
        self.original_image = self.animation_list[self.frame_index]
        if pg.time.get_ticks() - self.update_time > c.ANIMATION_DELAY:
            self.update_time = pg.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0   
            self.last_shot = pg.time.get_ticks()
            self.target = None

    def upgrade(self):
        self.upgrade_level +=1
        self.range = TURRET_DATA[self.upgrade_level - 1].get("range")
        self.cooldown = TURRET_DATA[self.upgrade_level - 1].get("cooldown")
        #create transparent circle to visualize turret range
        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0,0,0,))
        self.range_image.set_colorkey((0,0,0))
        pg.draw.circle(self.range_image, "grey100", (self.range,self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center
        self.animation_list = self.load_images(self.sprite_sheets[self.upgrade_level-1])
        self.original_image = self.animation_list[self.frame_index]
    
    def draw(self,surface):
        self.image = pg.transform.rotate(self.original_image,self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)
        if self.selected == True:
            surface.blit(self.range_image,self.range_rect)
        surface.blit(self.image,self.rect)
