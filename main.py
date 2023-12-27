import pygame as pg
import json
import constants as c
from world import World
from enemy import Enemy
from turret import Turret
from button import Button

pg.init()

clock = pg.time.Clock()

screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL,c.SCREEN_HEIGHT))
pg.display.set_caption('Tower Defense')

###############
#GAME VARIABLES
###############

placing_turrets = False
selected_turret = None

#############
#LOAD IMAGES
#############
#map
map_image = pg.image.load('levels/level.png').convert_alpha()

#loading turret sheets
turret_spritesheets = []
for x in range(1, c.TURRET_LEVELS + 1):
    turret_sheet = pg.image.load(f'assets/images/turrets/turret_{x}.png').convert_alpha()
    turret_spritesheets.append(turret_sheet)
#individual image for mouse cursor
cursor_turret = pg.image.load('assets/images/turrets/cursor_turret.png').convert_alpha()
#enemies
enemy_image = pg.image.load('assets/images/enemies/enemy_1.png').convert_alpha()
#buttons
buy_turret_image= pg.image.load('assets/images/buttons/buy_turret.png').convert_alpha()
cancel_image= pg.image.load('assets/images/buttons/cancel.png').convert_alpha()
upgrade_turret_image= pg.image.load('assets/images/buttons/upgrade_turret.png').convert_alpha()


#load json data for level
with open('levels/level.tmj') as file:
    world_data = json.load(file)


def create_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    #calculate the sequential number of the tile
    mouse_tile_num = mouse_tile_y * c.COLS + mouse_tile_x
    #check if tile is grass
    if world.tile_map[mouse_tile_num] == 7:
        #check if space is free
        space_is_free = True
        for turret in turret_group:
            if turret.tile_x == mouse_tile_x and turret.tile_y == mouse_tile_y:
                space_is_free = False
        if space_is_free == True:
            new_turret = Turret(turret_spritesheets, mouse_tile_x, mouse_tile_y)
            turret_group.add(new_turret)

def select_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    for turret in turret_group:
        if turret.tile_x == mouse_tile_x and turret.tile_y == mouse_tile_y:
            return turret
    
def clear_selection():
    for turret in turret_group:
        turret.selected = False



#creat world
world = World(world_data,map_image)
world.process_data()

#creat group
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()



enemy = Enemy(world.waypoints,enemy_image)
enemy_group.add(enemy)

#creat buttons
turret_button = Button(c.SCREEN_WIDTH + 30, 120, buy_turret_image, True)
cancel_button = Button(c.SCREEN_WIDTH + 50, 180, cancel_image, True)
upgrade_turret_button = Button(c.SCREEN_WIDTH + 5, 180, upgrade_turret_image, True)




run = True
while run:
    clock.tick(c.FPS)

    #################
    #UPDATING SECTION
    #################
    enemy_group.update()
    turret_group.update(enemy_group)

    #highlight selected turret
    if selected_turret:
        selected_turret.selected = True

    ##################
    #DRAWING SECTION
    ##################

    screen.fill('grey100')
    # draw level
    world.draw(screen)

    #draw enemy path
    pg.draw.lines(screen,'grey0', False, world.waypoints)  

    #draw groups
    enemy_group.draw(screen)
    for turret in turret_group:
        turret.draw(screen)

    #draw buttons
    if turret_button.draw(screen):
        placing_turrets = True
    if placing_turrets == True:
        # show cursor turret
        cursor_rect = cursor_turret.get_rect()
        cursor_pos = pg.mouse.get_pos()
        cursor_rect.center = cursor_pos
        if cursor_pos[0] < c.SCREEN_WIDTH:
            screen.blit(cursor_turret,cursor_rect)

        if cancel_button.draw(screen):
            placing_turrets = False
    
    if selected_turret:
        if upgrade_turret_button.draw(screen):
            if selected_turret.upgrade_level < c.TURRET_LEVELS:
                selected_turret.upgrade()
    
    for event in pg.event.get():
        if event.type == pg.QUIT :
            run = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                run = False
                print("ESC QUIT")
        #mouseclick
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pg.mouse.get_pos()
            #check if mouse is on game area
            if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
                # clear selection with click
                selected_turret = None
                clear_selection()
                if placing_turrets == True:
                    create_turret(mouse_pos)
                else:
                    selected_turret = select_turret(mouse_pos)
            


    pg.display.flip()

pg.quit()