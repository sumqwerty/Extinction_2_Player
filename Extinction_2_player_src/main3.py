import pygame as pg
import sys
from random import choice, random
from os import path
from settings3 import *
from sprites3 import *
from tilemap3 import *


# HUD functions
def draw_player_health(surf, x, y, pct, pic, picx, picy):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    if pct > 0:
        pg.draw.rect(surf, col, fill_rect)
        pg.draw.rect(surf, WHITE, outline_rect, 2)
    else:
        smallfont = pg.font.Font("Kenney_Future.ttf", 15)
        text = smallfont.render("Game Over", True, RED)
        surf.blit(text, [x,y])

    surf.blit(pic, [picx,picy])

class Game:
    def __init__(self):
        self.st = True
        self.i = 0
        self.j = 1
        self.show_map = False
        self.mute_audio = False
        pg.mixer.pre_init(44100, -16, 4, 2048)
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.screen_layer = [self.show_start_screen,self.control_screen]
        self.screen_layer_index = 0
        self.load_data()

    def draw_text(self, text, font_name, size, color, x, y, align="topleft"):
        phont = pg.font.Font(font_name, size)
        text_surface = phont.render(text, True, color)
        text_rect = text_surface.get_rect(**{align: (x, y)})
        self.screen.blit(text_surface, text_rect)

    def draw_button(self, x, y, w, h, b_acolor, b_color, text, size, t_color, action=None):
        #self.draw_button(100,100,80,50,GREEN,'Start', 20, RED,'start')
        #print("fffffffff")
        smallfont = pg.font.Font(self.butn_font, size)
        txt = smallfont.render(text, True, t_color)
        cur = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        pg.draw.rect(self.screen, b_color, (x,y,w,h))
        if x + w > cur[0] > x and y + h > cur[1] > y:
            pg.draw.rect(self.screen, b_acolor, (x,y,w,h))
            if click[0] == 1 and action == 'start':
                self.load_data()
                self.new()
                self.run()
                self.show_go_screen()
            if click[0] == 1 and action == 'restart':
                self.load_data()
                self.new()
                self.run()
                self.show_go_screen()
            if click[0] == 1 and action == 'opt':
                self.control_screen()
            if click[0] == 1 and action == 'char':
                self.char_screen()
            if click[0] == 1 and action == 'back':
                self.screen_layer[self.screen_layer_index - 1]()

        self.screen.blit(txt, [x+5,y])
        #self.screen.blit(self.icon_img, [350,400])

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        snd_folder = path.join(game_folder, 'snd')
        music_folder = path.join(game_folder, 'music')
        self.map_folder = path.join(game_folder, 'maps')
        self.title_font = path.join(img_folder, 'ZOMBIE.TTF')
        self.con_font = path.join(img_folder, 'Kenney Pixel.ttf')
        self.char_font = path.join(img_folder, 'Kenney Pixel Square.ttf')
        self.intro_font = path.join(img_folder, 'Kenney Rocket Square.ttf')
        self.hud_font = path.join(img_folder, 'Impacted2.0.ttf')
        self.butn_font = path.join(img_folder, 'Kenney Future.ttf')
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        self.icon_img = pg.image.load(path.join(img_folder, ICON_IMG)).convert_alpha()
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG[self.i])).convert_alpha()
        self.player_health_img = pg.image.load(path.join(img_folder, HEALTH_IMG[self.i])).convert_alpha()
        self.player2_img = pg.image.load(path.join(img_folder, PLAYER_IMG[self.j])).convert_alpha()
        self.player2_health_img = pg.image.load(path.join(img_folder, HEALTH_IMG[self.j])).convert_alpha()

        self.mini_map = pg.image.load(path.join(self.map_folder,'Mini_map1.png'))
        self.mini_map2 = pg.image.load(path.join(self.map_folder,'Mini_map2.png'))
        self.mini_map3 = pg.image.load(path.join(self.map_folder,'Mini_map3.png'))
        self.mini_map4 = pg.image.load(path.join(self.map_folder,'Mini_map4.png'))

        self.mini_map.set_alpha(150)
        self.mini_map2.set_alpha(150)
        self.mini_map3.set_alpha(150)
        self.mini_map4.set_alpha(150)

        self.heal_img_blue = pg.image.load(path.join(img_folder, PLAYER_IMG[0])).convert_alpha()
        self.heal_img_sol = pg.image.load(path.join(img_folder, PLAYER_IMG[1])).convert_alpha()
        self.heal_img_hit = pg.image.load(path.join(img_folder, PLAYER_IMG[2])).convert_alpha()
        self.heal_img_rob = pg.image.load(path.join(img_folder, PLAYER_IMG[3])).convert_alpha()
        self.heal_img_brown = pg.image.load(path.join(img_folder, PLAYER_IMG[4])).convert_alpha()
        self.heal_img_sur = pg.image.load(path.join(img_folder, PLAYER_IMG[5])).convert_alpha()

        self.real_img_blue = pg.image.load(path.join(img_folder, HEALTH_IMG_REAL[0])).convert_alpha()
        self.real_img_sol = pg.image.load(path.join(img_folder, HEALTH_IMG_REAL[1])).convert_alpha()
        self.real_img_hit = pg.image.load(path.join(img_folder, HEALTH_IMG_REAL[2])).convert_alpha()
        self.real_img_rob = pg.image.load(path.join(img_folder, HEALTH_IMG_REAL[3])).convert_alpha()
        self.real_img_brown = pg.image.load(path.join(img_folder, HEALTH_IMG_REAL[4])).convert_alpha()
        self.real_img_sur = pg.image.load(path.join(img_folder, HEALTH_IMG_REAL[5])).convert_alpha()

        self.bullet_images = {}
        self.bullet_images['lg'] = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.bullet_images['sm'] = pg.transform.scale(self.bullet_images['lg'], (10, 10))
        self.bullet_images['rk'] = pg.image.load(path.join(img_folder, ROCKET_IMG)).convert_alpha()
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.splat = pg.image.load(path.join(img_folder, SPLAT)).convert_alpha()
        self.splat = pg.transform.scale(self.splat, (64, 64))
        self.gun_flashes = []
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()
        # lighting effect
        self.fog = pg.Surface((WIDTH, HEIGHT))
        self.fog.fill(NIGHT_COLOR)
        self.light_mask = pg.image.load(path.join(img_folder, LIGHT_MASK)).convert_alpha()
        self.light_mask = pg.transform.scale(self.light_mask, LIGHT_RADIUS)
        self.light_rect = self.light_mask.get_rect()
        self.light2_rect = self.light_mask.get_rect()
        # Sound loading
        pg.mixer.music.load(path.join(music_folder, BG_MUSIC))
        self.effects_sounds = {}
        for type in EFFECTS_SOUNDS:
            self.effects_sounds[type] = pg.mixer.Sound(path.join(snd_folder, EFFECTS_SOUNDS[type]))
        self.weapon_sounds = {}
        for weapon in WEAPON_SOUNDS:
            self.weapon_sounds[weapon] = []
            for snd in WEAPON_SOUNDS[weapon]:
                s = pg.mixer.Sound(path.join(snd_folder, snd))
                s.set_volume(0.3)
                self.weapon_sounds[weapon].append(s)
        self.zombie_moan_sounds = []
        for snd in ZOMBIE_MOAN_SOUNDS:
            s = pg.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(0.2)
            self.zombie_moan_sounds.append(s)
        self.player_hit_sounds = []
        for snd in PLAYER_HIT_SOUNDS:
            self.player_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))
        self.zombie_hit_sounds = []
        for snd in ZOMBIE_HIT_SOUNDS:
            self.zombie_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))

    def new(self):
        # initialize all variables and do all the setup for a new game
        if self.st:
            self.stage = 1
            self.st = False
        #self.b = 1
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        #self.total_mobs = len(self.mobs)
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        if self.stage == 1:
            self.map = TiledMap(path.join(self.map_folder, 'level1.tmx'))
            #self.map = TiledMap(path.join(self.map_folder, 'level4.tmx'))
        elif self.stage == 2:
            self.map = TiledMap(path.join(self.map_folder, 'level2.tmx'))
        elif self.stage == 3:
            self.map = TiledMap(path.join(self.map_folder, 'level3.tmx'))
        elif self.stage == 4:
            self.map = TiledMap(path.join(self.map_folder, 'level4.tmx'))
        self.map_img = self.map.make_map()
        self.map.rect = self.map_img.get_rect()
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)
            #print(tile_object.name)
            if tile_object.name == 'player':
                #print("p1")
                self.player = Player(self, obj_center.x, obj_center.y, "arrow", self.player_img)
            if tile_object.name == 'player2':
                #print("p2")
                self.player2 = Player2(self, obj_center.x, obj_center.y, self.player2_img)
            if tile_object.name == 'zombie':
                #print("mob")
                Mob(self, obj_center.x, obj_center.y)
                self.z_dotx = int(obj_center.x/10)+10
                self.z_doty = int(obj_center.y/10)+80
                self.total_mobs = len(self.mobs)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
            if tile_object.name in ['health', 'shotgun','rocket']:
                Item(self, obj_center, tile_object.name)
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.paused = False
        self.night = False
        self.effects_sounds['level_start'].play()

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        pg.mixer.music.play(loops=-1)

        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
            self.events()
            if self.mute_audio:
                pg.mixer.music.stop()
            else:
                pg.mixer.music.play(-1, 0.0)
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.hg_score = 0
        self.player_life = 0
        self.player2_life = 0

        if self.player.health > 0:
            self.player_life = 0
        if self.player.health <= 0:
            self.player_life = 1

        if self.player2.health > 0:
            self.player2_life = 0
        if self.player2.health <= 0:
            self.player2_life = 1

        # update portion of the game loop
        self.all_sprites.update()
        if self.player.health > 0:
            self.camera.update(self.player)
        else:
            self.camera.update(self.player2)
        #self.camera.update(self.player2)
        # stage change?
        if len(self.mobs) == 0:
            #self.playing = False
            self.stage = self.stage + 1
            self.final_score = self.score
            #print(self.final_score)
            self.show_stage()
            self.new()

        # player hits items
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == 'health' and self.player.health < PLAYER_HEALTH:
                hit.kill()
                if not self.mute_audio:
                    self.effects_sounds['health_up'].play()
                self.player.add_health(HEALTH_PACK_AMOUNT)
                print(self.player.picked)
            if hit.type == 'shotgun':
                hit.kill()
                if not self.mute_audio:
                    self.effects_sounds['gun_pickup'].play()
                self.player.weapon = 'shotgun'
                self.player.pickeds = 1
                #print(self.player.picked)
            if hit.type == 'rocket':
                hit.kill()
                if not self.mute_audio:
                    self.effects_sounds['gun_pickup'].play()
                self.player.weapon = 'rocket'
                self.player.pickedr = 1

        # player2 hits items
        hits = pg.sprite.spritecollide(self.player2, self.items, False)
        for hit in hits:
            if hit.type == 'health' and self.player2.health < PLAYER2_HEALTH:
                hit.kill()
                if not self.mute_audio:
                    self.effects_sounds['health_up'].play()
                self.player2.add_health(HEALTH_PACK_AMOUNT)
            if hit.type == 'shotgun':
                hit.kill()
                if not self.mute_audio:
                    self.effects_sounds['gun_pickup'].play()
                self.player2.weapon = 'shotgun'
                self.player2.pickeds = 1
            if hit.type == 'rocket':
                hit.kill()
                if not self.mute_audio:
                    self.effects_sounds['gun_pickup'].play()
                self.player2.weapon = 'rocket'
                self.player2.pickedr = 1


        # mobs hit player
        if self.player_life == 0:
            hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
            for hit in hits:
                #print(self.player.kill())
                #print(self.b)
                #self.b += 1
                if not self.mute_audio:
                    if random() < 0.7:
                        choice(self.player_hit_sounds).play()
                self.player.health -= MOB_DAMAGE
                hit.vel = vec(0, 0)
                if self.player.health <= 0:
                    if self.player2.health <= 0:
                        self.high_scr = open('.\score\high_score.txt', 'r')
                        score_reading = self.high_scr.read()
                        if str(self.score) > score_reading:
                            self.hg_score = True
                            self.high_scr = open('.\score\high_score.txt', 'w')
                            self.high_scr.write(str(self.score))

                        self.playing = False

                    else:
                        self.player.kill()
                if hits:# and self.player.health > 0:
                    self.player.hit()
                    self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)

        # mobs hit player2
        if self.player2_life == 0:
            hits = pg.sprite.spritecollide(self.player2, self.mobs, False, collide_hit_rect)
            for hit in hits:
                if not self.mute_audio:
                    if random() < 0.7:
                        choice(self.player_hit_sounds).play()
                self.player2.health -= MOB_DAMAGE
                hit.vel = vec(0, 0)
                if self.player2.health <= 0: #and self.player.health <= 0:
                    if self.player.health <= 0:

                        self.high_scr = open('./score/high_score.txt', 'r')
                        score_reading = self.high_scr.read()
                        if str(self.score) > score_reading:
                            self.hg_score = True
                            self.high_scr = open('./score/high_score.txt', 'w')
                            self.high_scr.write(str(self.score))
                        self.playing = False
                    else:
                        self.player2.kill()

                if hits:
                    self.player2.hit()
                    self.player2.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)

        # bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for mob in hits:
            # hit.health -= WEAPONS[self.player.weapon]['damage'] * len(hits[hit])
            for bullet in hits[mob]:
                mob.health -= bullet.damage
            mob.vel = vec(0, 0)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def render_fog(self):
        # draw the light mask (gradient) onto fog image
        self.fog.fill(NIGHT_COLOR)
        self.light_rect.center = self.camera.apply(self.player).center
        self.light2_rect.center = self.camera.apply(self.player2).center
        if self.player.health > 0:
            self.fog.blit(self.light_mask, self.light_rect)
        if self.player2.health > 0:
            self.fog.blit(self.light_mask, self.light2_rect)

        self.screen.blit(self.fog, (0, 0), special_flags=pg.BLEND_MULT)

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply(self.map))
        #self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 2)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 2)

        #pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        if self.night:
            self.render_fog()
        # HUD functions
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH, self.player_health_img, 120, 10)
        draw_player_health(self.screen, 10, 40, self.player2.health / PLAYER2_HEALTH, self.player2_health_img, 120, 40)

        self.draw_text('Zombies: {}'.format(len(self.mobs)), self.hud_font, 30, RED,
                       WIDTH - 10, 10, align="topright")


        self.score = (self.total_mobs - (len(self.mobs))) * 10

#        if self.stage == 1:
        self.draw_text('Score: {}'.format(self.score), self.hud_font, 30, YELLOW,
                        WIDTH - 180, 10, align="topright")

        self.draw_text('Stage: {}'.format(self.stage), self.hud_font, 30, WHITE,
                        WIDTH - 320, 10, align="topright")

#        else:
#            self.draw_text('Score: {}'.format(self.final_score), self.hud_font, 30, WHITE,
#                            WIDTH - 300, 10, align="topright")

        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", self.title_font, 105, RED, WIDTH / 2, HEIGHT / 2, align="center")

        if self.player.health > 0:
            self.draw_text("Player 1", self.char_font, 15, RED, 20, 8, align="topleft")
        if self.player2.health > 0:
            self.draw_text("Player 2", self.char_font, 15, BLUE, 20, 38, align="topleft")


        #drawing mini_map and player dots
        if self.show_map:
            dot_x1, dot_y1 = int((self.player.pos.x/10)+10),int((self.player.pos.y/10)+80) #coordinates of dot with respect to player's
            dot_x2, dot_y2 = int((self.player2.pos.x/10)+10),int((self.player2.pos.y/10)+80)
            pg.draw.line(self.screen, BLUE, (8,78),(330,78), 2)
            pg.draw.line(self.screen, BLUE, (330,78),(330,270), 2)
            pg.draw.line(self.screen, BLUE, (330,270),(8,270), 2)
            pg.draw.line(self.screen, BLUE, (8,270),(8,78), 2)
            if self.stage == 1:
                self.screen.blit(self.mini_map, [10,80])
            if self.stage == 2:
                self.screen.blit(self.mini_map2, [10,80])
            if self.stage == 3:
                self.screen.blit(self.mini_map3, [10,80])
            if self.stage == 4:
                self.screen.blit(self.mini_map4, [10,80])
            if self.player.health > 0:
                pg.draw.circle(self.screen, RED, (dot_x1, dot_y1), 2)
            if self.player2.health > 0:
                pg.draw.circle(self.screen, YELLOW, (dot_x2, dot_y2), 2)

        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
                if event.key == pg.K_p:
                    self.paused = not self.paused
                if event.key == pg.K_n:
                    self.night = not self.night
                if event.key == pg.K_m:
                    self.show_map = not self.show_map
                if event.key == pg.K_l:
                    self.mute_audio = not self.mute_audio



    def show_start_screen(self):
        start_screen = True
        self.screen_layer_index = 0
        while start_screen:
            self.clock.tick(10)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    #waiting = False
                    self.quit()
            self.screen.fill(BLACK)
            self.draw_text("EXTINCTION", self.title_font, 100, RED,
                            WIDTH / 2, HEIGHT / 4, align="center")

            #self.draw_text("Press a key to start", self.title_font, 75, WHITE,
            #                WIDTH / 2, HEIGHT * 3 / 4, align="center")

            #pg.draw.rect(self.screen, GREEN, (10,(HEIGHT/4)+100,10,10))
            #draw_button(self, x, y, w, h, b_color, text, size, t_color, action=None)

            self.screen.blit(self.icon_img, [360,400])
            self.draw_button(200, HEIGHT/2, 130, 40, GREEN, DARK_GREEN, 'Start', 30, RED,'start')
            self.draw_button(700, HEIGHT/2, 140, 40, YELLOW, DARK_YELLOW, 'Option', 30, RED,'opt')
            pg.display.flip()
            #self.wait_for_key()

    def show_go_screen(self):
        self.st = True
        go_screen = True
        while go_screen:
            #self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    #waiting = False
                    self.quit()
            self.screen.fill(BLACK)
            self.draw_text("GAME OVER", self.title_font, 100, RED,
                            WIDTH / 2, HEIGHT / 2, align="center")
            #self.draw_text("Press a key to start", self.title_font, 75, WHITE,
            #                WIDTH / 2, HEIGHT * 3 / 4, align="center")

            if self.hg_score:
                self.draw_text('New High Score: {}'.format(self.score), self.hud_font, 30, YELLOW,
                                WIDTH/2, (HEIGHT/2) + 100, align="center")

            else:
                self.draw_text('Your Score: {}'.format(self.score), self.hud_font, 30, YELLOW,
                                WIDTH/2, (HEIGHT/2) + 100, align="center")

            self.draw_button(150, (HEIGHT/2)+200, 180, 40,LIGHT_BLUE, BLUE, 'Restart', 30, RED,'restart')
            pg.display.flip()
        #self.wait_for_key()

    def control_screen(self):
        con_screen = True
        self.screen_layer_index = 1
        while con_screen:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    #waiting = False
                    self.quit()
            self.screen.fill(BLACK)
            #CONTROLS
            self.draw_text("CONTROLS", self.hud_font, 100, RED,
                            WIDTH / 2, 50, align="center")

            self.draw_text("PLAYER 1 FIRE- SPACE", self.con_font, 70, RED,
                            WIDTH / 2, 160, align="center")
            self.draw_text("PLAYER 2 FIRE- Z", self.con_font, 70, RED,
                            WIDTH / 2, 220, align="center")
            self.draw_text("PLAYER 1 MOVEMENT- ARROW KEYS", self.con_font, 70, RED,
                            WIDTH / 2, 280, align="center")
            self.draw_text("PLAYER 2 MOVEMENT- A, S, W, D", self.con_font, 70, RED,
                            WIDTH / 2, 340, align="center")
            self.draw_text("PLAYER 1 WEAPON CHANGE- 1, 2", self.con_font, 70, RED,
                            WIDTH / 2, 400, align="center")
            self.draw_text("PLAYER 2 WEAPON CHANGE- <, >", self.con_font, 70, RED,

                            WIDTH / 2, 460, align="center")

            #pause and night mode
            self.draw_text("PAUSE- P", self.con_font, 70, RED,
                            WIDTH / 2, 520, align="center")
            self.draw_text("NIGHT MODE- N", self.con_font, 70, RED,
                            WIDTH / 2, 580, align="center")

            self.draw_button((WIDTH/2)-125, 620, 255, 40, YELLOW, DARK_YELLOW, 'Characters', 30, RED,'char')
            self.draw_button((WIDTH/2)-52, 670, 105, 40, GREEN, DARK_GREEN, 'Back', 30, RED,'back')
            
            pg.display.flip()
            #self.clock.tick(10)


    def char_screen(self):
        chr_screen = True
        picked1 = 0
        picked2 = 0
        x = 100
        y = 125
        x1 = 250
        y1 = 295
        self.i = 0
        self.j = 1
        self.screen_layer_index = 2
        while chr_screen:

            cur = pg.mouse.get_pos()
            click = pg.mouse.get_pressed()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    #waiting = False
                    self.quit()
            self.screen.fill(BLACK)
            #self.draw_text("PLAYER 1 FIRE- SPACE", self.con_font, 70, RED,
            #                WIDTH / 2, 70, align="center")
            self.draw_text("Characters", self.hud_font,80,RED,WIDTH/2,50,align="center")
            self.draw_text("P-1", self.char_font,30,RED,20,130,align="topleft")
            self.screen.blit(self.heal_img_blue, [100,130])
            self.screen.blit(self.heal_img_sol, [250,130])
            self.screen.blit(self.heal_img_hit, [400,130])
            self.screen.blit(self.heal_img_rob, [550,130])
            self.screen.blit(self.heal_img_brown, [700,130])
            self.screen.blit(self.heal_img_sur, [850,130])


            self.draw_text("P-2", self.char_font,30,BLUE,20,300,align="topleft")
            self.screen.blit(self.heal_img_blue, [100,300])
            self.screen.blit(self.heal_img_sol, [250,300])
            self.screen.blit(self.heal_img_hit, [400,300])
            self.screen.blit(self.heal_img_rob, [550,300])
            self.screen.blit(self.heal_img_brown, [700,300])
            self.screen.blit(self.heal_img_sur, [850,300])

            if 900 > cur[0] > 100 and 350 > cur[1] > 100:
                if 150 > cur[0] > 100 and 180 > cur[1] > 130:
                    if click[0] == 1:
                        PLAYER_HEALTH = 100
                        x = 100
                        self.i = 0
                        picked1 = 1
                if 300 > cur[0] > 250 and 180 > cur[1] > 130:
                    if click[0] == 1:
                        PLAYER_HEALTH = 100
                        x = 250
                        self.i = 1
                        picked1 = 1
                if 450 > cur[0] > 400 and 180 > cur[1] > 130:
                    if click[0] == 1:
                        PLAYER_HEALTH = 100
                        x = 400
                        self.i = 2
                        picked1 = 1
                if 600 > cur[0] > 550 and 180 > cur[1] > 130:
                    if click[0] == 1:
                        PLAYER_HEALTH = 170
                        x = 550
                        self.i = 3
                        picked1 = 1
                if 750 > cur[0] > 700 and 180 > cur[1] > 130:
                    if click[0] == 1:
                        PLAYER_HEALTH = 100
                        x = 700
                        self.i = 4
                        picked1 = 1
                if 900 > cur[0] > 850 and 180 > cur[1] > 130:
                    if click[0] == 1:
                        PLAYER_HEALTH = 200
                        x = 850
                        self.i = 5
                        picked1 = 1

                if 150 > cur[0] > 100 and 350 > cur[1] > 300:
                    if click[0] == 1:
                        x1 = 100
                        y1 = 295
                        self.j = 0
                        picked2 = 1
                if 300 > cur[0] > 250 and 350 > cur[1] > 300:
                    if click[0] == 1:
                        x1 = 250
                        y1 = 295
                        self.j = 1
                        picked2 = 1
                if 450 > cur[0] > 400 and 350 > cur[1] > 300:
                    if click[0] == 1:
                        x1 = 400
                        y1 = 295
                        self.j = 2
                        picked2 = 1
                if 600 > cur[0] > 550 and 350 > cur[1] > 300:
                    if click[0] == 1:
                        x1 = 550
                        y1 = 295
                        self.j = 3
                        picked2 = 1
                if 750 > cur[0] > 700 and 350 > cur[1] > 300:
                    if click[0] == 1:
                        x1 = 700
                        y1 = 295
                        self.j = 4
                        picked2 = 1
                if 900 > cur[0] > 850 and 350 > cur[1] > 300:
                    if click[0] == 1:
                        x1 = 850
                        y1 = 295
                        self.j = 5
                        picked2 = 1

            self.draw_button((WIDTH/2)-65, 450, 130, 40, GREEN, DARK_GREEN, 'Start', 30, RED,'start')
            self.draw_button((WIDTH/2)-52, 510, 105, 40, GREEN, DARK_GREEN, 'Back', 30, RED,'back')
            self.screen.blit(self.real_img_blue,[100,500])
            self.screen.blit(self.real_img_sol,[(WIDTH-286),500])

            if picked1 == 1:
                pg.draw.line(self.screen, RED, (x,y), (x+50,y),2)
                pg.draw.line(self.screen, RED, (x,y), (x,y+50),2)
                pg.draw.line(self.screen, RED, (x+50,y), (x+50,y+50),2)
                pg.draw.line(self.screen, RED, (x+50,y+50), (x,y+50),2)
                if self.i == 0:
                    self.draw_text("Man Blue", self.con_font,50,RED,130,450,align="topleft")
                    self.screen.blit(self.real_img_blue,[100,500])
                if self.i == 1:
                    self.draw_text("Soldier", self.con_font,50,RED,150,450,align="topleft")
                    self.screen.blit(self.real_img_sol,[100,500])
                if self.i == 2:
                    self.draw_text("Hit Man", self.con_font,50,RED,150,450,align="topleft")
                    self.screen.blit(self.real_img_hit,[100,500])
                if self.i == 3:
                    self.draw_text("Robot", self.con_font,50,RED,130,450,align="topleft")
                    self.screen.blit(self.real_img_rob,[100,500])
                if self.i == 4:
                    self.draw_text("Man Brown", self.con_font,50,RED,120,450,align="topleft")
                    self.screen.blit(self.real_img_brown,[100,500])
                if self.i == 5:
                    self.draw_text("Survivor", self.con_font,50,RED,130,450,align="topleft")
                    self.screen.blit(self.real_img_sur,[100,500])

            if picked2 == 1:
                pg.draw.line(self.screen, BLUE, (x1,y1), (x1+50,y1),2)
                pg.draw.line(self.screen, BLUE, (x1,y1), (x1,y1+50),2)
                pg.draw.line(self.screen, BLUE, (x1+50,y1), (x1+50,y1+50),2)
                pg.draw.line(self.screen, BLUE, (x1+50,y1+50), (x1,y1+50),2)
                if self.j == 0:
                    self.draw_text("Man Blue", self.con_font,50,BLUE,760,450,align="topleft")
                    self.screen.blit(self.real_img_blue,[(WIDTH-286),500])
                if self.j == 1:
                    self.draw_text("Soldier", self.con_font,50,BLUE,780,450,align="topleft")
                    self.screen.blit(self.real_img_sol,[(WIDTH-286),500])
                if self.j == 2:
                    self.draw_text("Hit Man", self.con_font,50,BLUE,780,450,align="topleft")
                    self.screen.blit(self.real_img_hit,[(WIDTH-286),500])
                if self.j == 3:
                    self.draw_text("Robot", self.con_font,50,BLUE,780,450,align="topleft")
                    self.screen.blit(self.real_img_rob,[(WIDTH-286),500])
                if self.j == 4:
                    self.draw_text("Man Brown", self.con_font,50,BLUE,750,450,align="topleft")
                    self.screen.blit(self.real_img_brown,[(WIDTH-286),500])
                if self.j == 5:
                    self.draw_text("Survivor", self.con_font,50,BLUE,760,450,align="topleft")
                    self.screen.blit(self.real_img_sur,[(WIDTH-286),500])

            if picked1 == 0:
                self.draw_text("Man Blue", self.con_font,50,RED,130,450,align="topleft")
                pg.draw.line(self.screen, RED, (x,y), (x+50,y),2)
                pg.draw.line(self.screen, RED, (x,y), (x,y+50),2)
                pg.draw.line(self.screen, RED, (x+50,y), (x+50,y+50),2)
                pg.draw.line(self.screen, RED, (x+50,y+50), (x,y+50),2)
            if picked2 == 0:
                self.draw_text("Soldier", self.con_font,50,BLUE,780,450,align="topleft")
                pg.draw.line(self.screen, BLUE, (x1,y1), (x1+50,y1),2)
                pg.draw.line(self.screen, BLUE, (x1,y1), (x1,y1+50),2)
                pg.draw.line(self.screen, BLUE, (x1+50,y1), (x1+50,y1+50),2)
                pg.draw.line(self.screen, BLUE, (x1+50,y1+50), (x1,y1+50),2)





            pg.display.flip()
            #self.clock.tick(10)


    def show_stage(self):
        shw_stage = True
        no = 0
        while shw_stage:
            no += 1
            cur = pg.mouse.get_pos()
            click = pg.mouse.get_pressed()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    #waiting = False
                    self.quit()
            self.screen.fill(BLACK)
            self.draw_text('Stage: {}'.format(self.stage), self.hud_font, 80, YELLOW,
                            WIDTH/2, (HEIGHT/2), align="center")

            pg.display.flip()
            if no == 3:
                shw_stage = False

            self.clock.tick(1)


    def wait_for_key(self):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

# create the game object
g = Game()
g.show_start_screen()
##while True:
##    g.new()
##    g.run()
##    g.show_go_screen()
