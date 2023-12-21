import pygame as pg
import json
import constants as c
from world import World
from enemy import Enemy



pg.init()

clock = pg.time.Clock()

screen = pg.display.set_mode((c.SCREEN_WIDTH,c.SCREEN_HEIGHT))
pg.display.set_caption('Tower Defense')


#load images
#map
map_image = pg.image.load('levels/level.png').convert_alpha()
#enemies
enemy_image = pg.image.load('assets/images/enemies/enemy_1.png').convert_alpha()

#load json data for level
with open('levels/level.tmj') as file:
    world_data = json.load(file)


#creat world
world = World(world_data,map_image)
world.process_data()

#creat group
enemy_group = pg.sprite.Group()



enemy = Enemy(world.waypoints,enemy_image)
enemy_group.add(enemy)




run = True
while run:
    clock.tick(c.FPS)
    screen.fill('grey100')
    # draw level
    world.draw(screen)

    #draw enemy path
    pg.draw.lines(screen,'grey0', False, world.waypoints)



    #update groups
    enemy_group.update()

    #draw groups
    enemy_group.draw(screen)
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            


    pg.display.flip()

pg.quit()