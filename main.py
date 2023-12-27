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
game_over = False
game_outcome = 0 #-1 is loss and 1 is win
level_started = False
last_enemy_spawn = pg.time.get_ticks()
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
enemy_images = {
    "weak" : pg.image.load('assets/images/enemies/enemy_1.png').convert_alpha(),
    "medium" : pg.image.load('assets/images/enemies/enemy_2.png').convert_alpha(),
    "strong" : pg.image.load('assets/images/enemies/enemy_3.png').convert_alpha(),
    "elite" : pg.image.load('assets/images/enemies/enemy_4.png').convert_alpha()
}
enemy_image = pg.image.load('assets/images/enemies/enemy_1.png').convert_alpha()
#buttons
buy_turret_image= pg.image.load('assets/images/buttons/buy_turret.png').convert_alpha()
cancel_image= pg.image.load('assets/images/buttons/cancel.png').convert_alpha()
upgrade_turret_image= pg.image.load('assets/images/buttons/upgrade_turret.png').convert_alpha()
begin_image= pg.image.load('assets/images/buttons/begin.png').convert_alpha()
restart_image= pg.image.load('assets/images/buttons/restart.png').convert_alpha()
fast_forward_image= pg.image.load('assets/images/buttons/fast_forward.png').convert_alpha()

# gui
heart_image= pg.image.load('assets/images/gui/heart.png').convert_alpha()
coin_image= pg.image.load('assets/images/gui/coin.png').convert_alpha()
logo_image= pg.image.load('assets/images/gui/logo.png').convert_alpha()

#load sound
shot_fx = pg.mixer.Sound('assets/audio/shot.wav')
shot_fx.set_volume(0.5)



#load json data for level
with open('levels/level.tmj') as file:
    world_data = json.load(file)

#load fonts
text_font = pg.font.SysFont("Consolas", 24 , bold = True)
large_font = pg.font.SysFont("Consolas", 36)


#function for outputting Text on Screen

def draw_text(text, font , text_col, x, y):
    img = font.render (text, True, text_col)
    screen.blit(img,(x,y))

def display_data():
    #draw panel
    pg.draw.rect(screen, "maroon", (c.SCREEN_WIDTH, 0, c.SIDE_PANEL, c.SCREEN_HEIGHT))
    pg.draw.rect(screen, "grey0", (c.SCREEN_WIDTH, 0, c.SIDE_PANEL, 400), 2)
    screen.blit(logo_image, (c.SCREEN_WIDTH, 400))
    #display data
    draw_text("LEVEL" + str(world.level), text_font, "grey100", c.SCREEN_WIDTH + 10, 10)
    screen.blit(heart_image,(c.SCREEN_WIDTH+10,35))
    draw_text(str(world.health), text_font, "grey100", c.SCREEN_WIDTH + 50, 40)
    screen.blit(coin_image,(c.SCREEN_WIDTH+10,65))
    draw_text(str(world.money), text_font, "grey100", c.SCREEN_WIDTH + 50, 70)


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
            new_turret = Turret(turret_spritesheets, mouse_tile_x, mouse_tile_y, shot_fx)
            turret_group.add(new_turret)
            world.money -= c.BUY_COST

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
world.process_enemies()

#creat group
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()


#creat buttons
turret_button = Button(c.SCREEN_WIDTH + 30, 120, buy_turret_image, True)
cancel_button = Button(c.SCREEN_WIDTH + 50, 180, cancel_image, True)
upgrade_turret_button = Button(c.SCREEN_WIDTH + 5, 180, upgrade_turret_image, True)
begin_button = Button(c.SCREEN_WIDTH + 60, 300, begin_image, True)
restart_button = Button(310, 300, restart_image, True)
fast_forward_button = Button(c.SCREEN_WIDTH + 50, 300, fast_forward_image, False)




run = True
while run:
    clock.tick(c.FPS)

    #################
    #UPDATING SECTION
    #################

    if game_over == False:
        #check if palyer has lost
        if world.health <= 0:
            game_over = True
            game_outcome = -1
        #check if player has won
        if world.level > c.TOTAL_LEVELS:
            game_over = True
            game_outcome = 1

        enemy_group.update(world)
        turret_group.update(enemy_group, world)

        #highlight selected turret
        if selected_turret:
            selected_turret.selected = True

    ##################
    #DRAWING SECTION
    ##################

    # draw level
    world.draw(screen)

    #draw enemy path
    pg.draw.lines(screen,'grey0', False, world.waypoints)  

    #draw groups
    enemy_group.draw(screen)
    for turret in turret_group:
        turret.draw(screen)

    display_data()
    
    if game_over == False:
        #check if lvl is started
        if level_started == False:
            if begin_button.draw(screen):
                level_started = True
        else:
        #spawn enemies
            #fast foward option
            world.game_speed = 1
            if fast_forward_button.draw(screen):
                world.game_speed = 2
            if pg.time.get_ticks() - last_enemy_spawn > c.SPAWN_COOLDOWN:
                if world.spawned_enemies < len(world.enemy_list):
                    enemy_type = world.enemy_list[world.spawned_enemies]
                    enemy = Enemy(enemy_type, world.waypoints,enemy_images)
                    enemy_group.add(enemy)
                    world.spawned_enemies += 1
                    last_enemy_spawn = pg.time.get_ticks()
        #check if wave is finished
        if world.check_level_complete() == True:
            world.money += c.LEVEL_COMPPLET_REWARD
            world.level += 1
            level_started = False
            last_enemy_spawn = pg.time.get_ticks()
            world.reset_level()
            world.process_enemies()



        #draw buttons
        draw_text(str(c.BUY_COST), text_font, "grey100", c.SCREEN_WIDTH + 215, 135)
        screen.blit(coin_image, (c.SCREEN_WIDTH+260, 130))
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
            draw_text(str(c.UPGRADE_COST), text_font, "grey100", c.SCREEN_WIDTH + 215, 195)
            screen.blit(coin_image, (c.SCREEN_WIDTH+260, 190))
            if upgrade_turret_button.draw(screen):
                if selected_turret.upgrade_level < c.TURRET_LEVELS:
                    if world.money >= c.UPGRADE_COST:
                        selected_turret.upgrade()
                        world.money -= c.UPGRADE_COST
    else:
        pg.draw.rect(screen, "dodgerblue", (200,200,400,200), border_radius = 30)
        if game_outcome == -1:
            draw_text("GAME OVER", large_font, "grey0", 310, 230)
        elif game_outcome == 1:
            draw_text("YOU WIN", large_font, "grey0", 315, 230)
        if restart_button.draw(screen):
            game_over = False
            level_started = False
            placing_turrets = False
            selected_turret = None
            last_enemy_spawn = pg.time.get_ticks()
            world = World(world_data,map_image)
            world.process_data()
            world.process_enemies()
            #empty groups
            enemy_group.empty()
            turret_group.empty()


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
                    if world.money >= c.BUY_COST:
                        create_turret(mouse_pos)
                else:
                    selected_turret = select_turret(mouse_pos)
            


    pg.display.flip()

pg.quit()