import pygame as pg
import constants as c
from enemy import Enemy



pg.init()

clock = pg.time.Clock()

screen = pg.display.set_mode((c.SCREEN_WIDTH,c.SCREEN_HEIGHT))
pg.display.set_caption('Tower Defense')


#load images
enemy_image = pg.image.load('assets/images/enemies/enemy_1.png').convert_alpha()

#creat group
enemy_group = pg.sprite.Group()

waypoints = [
    (100,100),
    (400,200),
    (400,100),
    (200,300)
]

enemy = Enemy(waypoints,enemy_image)
enemy_group.add(enemy)




run = True
while run:
    clock.tick(c.FPS)
    screen.fill('grey100')

    #draw enemy path
    pg.draw.lines(screen,'grey0', False, waypoints)



    #update groups
    enemy_group.update()

    #draw groups
    enemy_group.draw(screen)
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            


    pg.display.flip()

pg.quit()