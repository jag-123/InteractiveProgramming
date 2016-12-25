"""Bubble Trouble: Olin Edition, designed using model-view-controller, generates bubbles
with pictures of Olin students for the player to pop until the player runs out of lives.
Once a bubble is hit, it splits into two smaller bubbles which travel in opposite directions.
This occurs until the bubble is a sufficiently small size, upon which it disappears when hit. """

import pygame
import os, sys
from pygame.locals import *
import random
import time
import pickle
import re

# define font/fill colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREY = (105,105,105)

# define constant variables
gravity = 1.2
screen_width = 1700
screen_height = 900
fps = 120

CURR_DIR = os.path.dirname(os.path.realpath(__file__))

# prepare/load pictures
pictures = [CURR_DIR + '/images/cedric.png',CURR_DIR + '/images/daniel.png',CURR_DIR + '/images/willem.png',CURR_DIR + '/images/kevin.png',CURR_DIR + '/images/anpan.png',CURR_DIR + '/images/mica.png']
background = pygame.image.load(CURR_DIR + '/images/olin.png')
bubble_background = pygame.image.load(CURR_DIR + '/images/bubble_background.png')

size = 22
cedric = pygame.image.load(CURR_DIR + '/images/cedric.png')
cedric = pygame.transform.scale(cedric,(size*10,size*10))
daniel = pygame.image.load(CURR_DIR + '/images/daniel.png')
daniel = pygame.transform.scale(daniel,(size*10,size*10))
willem = pygame.image.load(CURR_DIR + '/images/willem.png')
willem = pygame.transform.scale(willem,(size*10,size*10))
kevin = pygame.image.load(CURR_DIR + '/images/kevin.png')
kevin = pygame.transform.scale(kevin,(size*10,size*10))
anpan = pygame.image.load(CURR_DIR + '/images/anpan.png')
anpan = pygame.transform.scale(anpan,(size*10,size*10))
mica = pygame.image.load(CURR_DIR + '/images/mica.png')
mica = pygame.transform.scale(mica,(size*10,size*10))

pygame.time.set_timer(pygame.USEREVENT, 1000)

# initialize/load sounds
pygame.mixer.init()

bubble_pop_sound = pygame.mixer.Sound(CURR_DIR + '/sound/bubble_pop.ogg')
player_hit_sound = pygame.mixer.Sound(CURR_DIR + '/sound/Frant_edit2.ogg')

class Player(pygame.sprite.Sprite):
	""" Main character for game """
	def __init__(self,speed):
		pygame.sprite.Sprite.__init__(self)
		self.alive = True                                               # if False, game over
		self.lives = 3
		self.isJumping = False
		self.speed = speed

		self.img_default = pygame.image.load(CURR_DIR + '/images/default_ninja.png')

		self.sheet = pygame.image.load(CURR_DIR +'/images/ninja.png') #sprite sheet for player animation
		self.sprite_row = 0
		self.dt_image = 0.0
		self.column = 0
		self.animation_speed = 0.10

		self.width = 58
		self.height = 64

		self.sheet.set_clip(pygame.Rect(self.column*self.width,self.sprite_row*self.height,self.width,self.height))
		self.image = self.sheet.subsurface(self.sheet.get_clip())

		self.rect = self.image.get_rect()
		self.gun = Gun()
		self.rect.left = screen_width/2 + 200
		self.rect.top = 834

	def jump(self):
		if (self.isJumping == False):
			self.speed = -15
			self.isJumping = True

	def update(self, pos, dt):
		self.pos = pos

		if self.alive:
			self.dt_image += dt
			#print self.rect
			if self.dt_image > self.animation_speed: #changes the subimage to make animation
				self.column += 1
				if self.column >= 6:
					self.column = 0
				self.dt_image = 0

			if self.isJumping:
				self.speed += gravity
				self.rect = self.rect.move(0,self.speed)
				#print self.rect.bottom			
				if self.rect.bottom >= screen_height-10:
					self.speed = 0
					self.isJumping = False

			if self.pos == 1:       # if right key is pressed, character moves right
				self.sheet.set_clip(pygame.Rect(self.column * self.width, self.sprite_row * self.height, self.width, self.height))
				self.image = self.sheet.subsurface(self.sheet.get_clip())
				self.rect.left += self.pos + 5
				if self.rect.left >= screen_width - 48:                # won't go past edge of screen
					self.rect.left = screen_width - 48

			elif self.pos == -1:                                   # if left key is pressed, character moves left
				self.sheet.set_clip(pygame.Rect(self.column * self.width, self.sprite_row * self.height, self.width, self.height))
				self.image = self.sheet.subsurface(self.sheet.get_clip())
				self.image = pygame.transform.flip(self.image, True, False) #flips the image if walking the other way
				self.rect.left += self.pos - 5
				if self.rect.left <= 0:                                 # won't go past edge of screen
					self.rect.left = 0

		else:
			self.image = pygame.image.load(CURR_DIR + '/images/dead_ninja.png') #image for player after it has lost a life

class Player2(pygame.sprite.Sprite):
	""" Main character for game """
	def __init__(self,speed):
		pygame.sprite.Sprite.__init__(self)
		self.alive = True                                               # if False, game over
		self.lives = 3
		self.isJumping = False
		self.speed = speed

		self.img_default = pygame.image.load(CURR_DIR + '/images/default_ninja_2.png')

		self.sheet = pygame.image.load(CURR_DIR +'/images/ninja2.png') #sprite sheet for player animation
		self.sprite_row = 0
		self.dt_image = 0.0
		self.column = 0
		self.animation_speed = 0.10

		self.width = 58
		self.height = 64

		self.sheet.set_clip(pygame.Rect(self.column*self.width,self.sprite_row*self.height,self.width,self.height))
		self.image = self.sheet.subsurface(self.sheet.get_clip())

		self.rect = self.image.get_rect()
		self.gun = Gun2()
		self.rect.left = screen_width/2 - 200
		self.rect.top = 834

	def jump(self):
		if (self.isJumping == False):
			self.speed = -15
			self.isJumping = True

	def update(self, pos, dt):
		self.pos = pos

		if self.alive:
			self.dt_image += dt
			#print self.rect
			if self.dt_image > self.animation_speed: #changes the subimage to make animation
				self.column += 1
				if self.column >= 6:
					self.column = 0
				self.dt_image = 0

			if self.isJumping:
				self.speed += gravity
				self.rect = self.rect.move(0,self.speed)
				#print self.rect.bottom			
				if self.rect.bottom >= screen_height-10:
					self.speed = 0
					self.isJumping = False

			if self.pos == 1:       # if right key is pressed, character moves right
				self.sheet.set_clip(pygame.Rect(self.column * self.width, self.sprite_row * self.height, self.width, self.height))
				self.image = self.sheet.subsurface(self.sheet.get_clip())
				self.rect.left += self.pos + 5
				if self.rect.left >= screen_width - 48:                # won't go past edge of screen
					self.rect.left = screen_width - 48

			elif self.pos == -1:                                   # if left key is pressed, character moves left
				self.sheet.set_clip(pygame.Rect(self.column * self.width, self.sprite_row * self.height, self.width, self.height))
				self.image = self.sheet.subsurface(self.sheet.get_clip())
				self.image = pygame.transform.flip(self.image, True, False) #flips the image if walking the other way
				self.rect.left += self.pos - 5
				if self.rect.left <= 0:                                 # won't go past edge of screen
					self.rect.left = 0

		else:
			self.image = pygame.image.load(CURR_DIR + '/images/dead_ninja_2.png') #image for player after it has lost a life

class Gun(pygame.sprite.Sprite):
    """ Weapon that shoots arrow to pop bubbles """
    def __init__(self, x = 0, y = 0):
        pygame.sprite.Sprite.__init__(self)
        self.active = False                                             # won't fire unless space key is pressed
        self.sheet = pygame.image.load(CURR_DIR + '/images/fireball_0.png') #fireball sprite sheet
        self.sprite_row = 0
        self.dt_image = 0.0
        self.column = 0
        self.animation_speed = 0.10

        self.width = 18
        self.height = 35

        self.sheet.set_clip(pygame.Rect(self.column*self.width,self.sprite_row*self.height,self.width,self.height))
        self.image = self.sheet.subsurface(self.sheet.get_clip())

        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y

    def update(self, dt):
        self.dt_image += dt

        if self.active:

            if self.dt_image > self.animation_speed: #animation to make the fireball change
                self.column += 1
                if self.column >= 7:
                    self.column = 0
                self.dt_image = 0

            self.sheet.set_clip(pygame.Rect(self.column*self.width,self.sprite_row*self.height,self.width,self.height))
            self.image = self.sheet.subsurface(self.sheet.get_clip())

            if self.rect.top <= 0:                                      # disappears when hits top of screen
                self.active = False
                self.kill()
            else:
                self.rect.top -= 17
        else:
            self.kill()

class Gun2(pygame.sprite.Sprite):
    """ Second weapon that shoots arrow to pop bubbles """
    def __init__(self, x = 0, y = 0):
        pygame.sprite.Sprite.__init__(self)
        self.active = False                                             # won't fire unless space key is pressed
        self.image = pygame.image.load(CURR_DIR + '/images/arrow2.png')

        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y

    def update(self, dt):
        if self.active:
            if self.rect.top <= 0:                                      # disappears when hits top of screen
                self.active = False
                self.kill()
            else:
                self.rect.top -= 17
        else:
            self.kill()

class Ball(pygame.sprite.Sprite):
    """ Bubbles that character needs to pop """
    def __init__(self, size, speed, x = 0, y = 0):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.speed = speed
        self.pic = random.choice(pictures)                              # randomly chooses between given pictures of Olin faces
        self.image = pygame.image.load(self.pic)
        self.image = pygame.transform.scale(self.image,(size*10,size*10))
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y

    def update(self):
        self.rect = self.rect.move(self.speed)
        if self.rect.left < 0 or self.rect.right > screen_width:        # bubbles bounce off of left/right/top/bottom walls
            self.speed[0] = -self.speed[0]
        if self.rect.top < 100 or self.rect.bottom > screen_height:
            self.speed[1] = -self.speed[1]

        self.rect.left = self.walls(self.rect.left, 0 , screen_width)
        self.rect.right = self.walls(self.rect.right, 0 , screen_width)
        self.rect.top = self.walls(self.rect.top, 100 , screen_height)
        self.rect.bottom = self.walls(self.rect.bottom, 0 , screen_height)

        self.speed[1] += gravity                                        # simulates effect of gravity

    def walls(self,number, min_number, max_number):
        """ helper function for ball to bounce off of walls """
        self.number = number
        self.min_number = min_number
        self.max_number = max_number
        return min(max(self.number,self.min_number),self.max_number) # min and max are used to find the correct number for the wall

class GameModel(object):
    """ Model for game """

    def __init__(self):
        self.width = screen_width
        self.height = screen_height

        self.count = 1
        self.score = 0
        self.player1 = Player(0)
        self.player2 = Player2(0)

        self.balls = []

        self.character_hit_list = []
        self.bubble_hit_list = []

        self.more_balls()

        self.list_of_bubbles = pygame.sprite.Group()
        self.gun_list = pygame.sprite.Group(self.player1.gun)
        self.player_sprite = pygame.sprite.Group(self.player1)
        self.player2_sprite = pygame.sprite.Group(self.player2)

    def more_balls(self):
        """ Generates/adds more balls once the player has cleared all other balls """
        for i in range(self.count):
            self.balls.append(Ball(random.randint(8,12),[3,5], random.randint(1,screen_width), random.randint(1,screen_height-(screen_height/3))))

    def update(self, pos, pos2, dt):
        """ Updates all sprites """
        self.list_of_bubbles.update()
        self.player_sprite.update(pos,dt)
        self.player2_sprite.update(pos2,dt)
        self.gun_list.update(dt)

        for ball in self.balls:
            self.list_of_bubbles.add(ball)

        self.player_sprite.add(self.player1)
        self.player2_sprite.add(self.player2)

    def is_collision(self,player):
        """ Checks for collisions between sprites """
        for index, ball in enumerate(self.balls):
            if player.gun.active and pygame.sprite.collide_rect(player.gun, ball):
                self.bubble_hit_list.append(ball.pic)
                bubble_pop_sound.play()
                self.score +=1
                player.gun.active = False
                ball.kill()
                self.split_ball(index)

            if pygame.sprite.collide_mask(player,ball):
                self.character_hit_list.append(ball.pic)
                player_hit_sound.play()

                #player.image = pygame.image.load(CURR_DIR + '/images/dead_ninja.png') #image for player after it has lost a life

                player.lives -= 1
                player.gun.active = False
                ball.kill()
                self.split_ball(index)
                #pygame.time.delay(500)

                if player.lives <= 0:
                    player.alive = False

    def split_ball(self,index):
        """ Splits bubbles into 2 smaller bubbles once hit by arrow """
        ball = self.balls[index]
        del self.balls[index]

        if ball.size > 4:                                               # smallest ball size is 2
            self.balls.append(Ball(ball.size-2,[-3,-3], ball.rect.left - 5, ball.rect.top-200))
            self.balls.append(Ball(ball.size-2,[3,-3], ball.rect.left + 5, ball.rect.top-200))

        if not self.balls:
            self.count += 1
            self.more_balls()

    def draw_sprites(self):
        """ Draw all sprites onto screen """
        #print self.player_sprite
        all_sprites_list = [self.list_of_bubbles, self.gun_list, self.player_sprite, self.player2_sprite]
        return all_sprites_list

class GameController(object):
    """ Controller for game.
    When certain key is pressed, does specific action """
    def __init__(self, model):
        self.model = model
        self.done = False
        self.pause = False

    def player_mvmt(self, dt = 0):
        """ Organizes keypresses """
        key = pygame.key.get_pressed()
        self.pause = False
        player1 = Player(0)
        player2 = Player2(0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            elif key[pygame.K_p]:
                self.pause = True

        if key[pygame.K_w]:
            self.model.player2.jump()

        if key[pygame.K_a] and key[pygame.K_d]:
            self.model.player2.pos = 0
            self.model.player2.image = self.model.player2.img_default
        elif key[pygame.K_d]:
            self.model.player2.pos = 1
        elif key[pygame.K_a]:
            self.model.player2.pos = -1
        else:
            self.model.player2.image = self.model.player2.img_default

        if key[pygame.K_LSHIFT] and self.model.player2.gun.active == False and self.model.player2.alive == True:
            self.model.gun_list.add(self.model.player2.gun)
            self.model.player2.gun.active = True
            self.model.player2.gun.rect.left = self.model.player2.rect.left + 20 #makes sure the gun and the player are at the same location
            self.model.player2.gun.rect.top = self.model.player2.rect.top
            player2.image = player2.img_default


        if key[pygame.K_UP]:
            self.model.player1.jump()

        if key[pygame.K_LEFT] and key[pygame.K_RIGHT]:
            self.model.player1.pos = 0
            self.model.player1.image = self.model.player1.img_default
        elif key[pygame.K_RIGHT]:
            self.model.player1.pos = 1
        elif key[pygame.K_LEFT]:
            self.model.player1.pos = -1
        else:
            self.model.player1.image = self.model.player1.img_default

        if key[pygame.K_SPACE] and self.model.player1.gun.active == False and self.model.player1.alive == True:
            self.model.gun_list.add(self.model.player1.gun)
            self.model.player1.gun.active = True
            self.model.player1.gun.rect.left = self.model.player1.rect.left + 20 #makes sure the gun and the player are at the same location
            self.model.player1.gun.rect.top = self.model.player1.rect.top
            player1.image = player1.img_default

        return (self.done, self.pause)

class GameView(object):
    """ View for game """
    def __init__(self, model):
        pygame.init()
        self.width = screen_width
        self.height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.model = model
        pygame.font.init()

        self.font = pygame.font.SysFont('dodge', 40)
        self.font1 = pygame.font.SysFont('zorque', 100)
        self.font2 = pygame.font.SysFont('zorque', 60)
        self.font3 = pygame.font.SysFont('zorque', 50)
        self.font4 = pygame.font.SysFont('zorque', 30)

        self.pause_surf = self.font2.render('PRESS P TO UNPAUSE', False, WHITE)
        self.obj_surf = self.font1.render('BUBBLE TROUBLE: OLIN EDITION', False, GREY)
        self.instructions_surf = self.font.render('LEFT AND RIGHT ARROW KEYS TO MOVE', False, WHITE)
        self.instructions_surf2 = self.font.render('SPACE TO SHOOT', False, WHITE)
        self.start_surf = self.font.render('PRESS P TO PAUSE', False, WHITE)
        self.start_surf2 = self.font.render('PRESS ANY KEY TO START', False, BLACK)
        self.game_over_surf = self.font2.render('GAME OVER', False, RED)
        self.restart_surf = self.font2.render('PRESS R TO RESTART', False, RED)
        self.score_surf = self.font3.render('You shot: ', False, GREY)
        self.score_surf2 = self.font3.render('You were killed by: ', False, GREY)

        if os.path.exists(CURR_DIR + '/hiscore.txt'):
            hiscore = str(pickle.load(open(CURR_DIR + '/hiscore.txt')))
        else: hiscore = '0'
        self.hiscore_surf = self.font1.render('High Score: ' + hiscore, False, BLACK)
        pygame.display.set_caption('Hot Tamales Game')

    def draw(self):
        """ Redraws the game window """
        self.screen.blit(background, (0,0))

        self.draw_score()
        self.draw_lives_left()

        drawn = self.model.draw_sprites()
        for sprite in drawn:
            sprite.draw(self.screen)
        pygame.display.flip()

    def draw_score(self):
        """ Draws score on screen """
        font = pygame.font.SysFont('dejavusans',50)
        scoretext = font.render('Score: ' + str(self.model.score), 2, [255,255,255])
        boxsize = scoretext.get_rect()
        scoreXpos = (screen_width-boxsize[2])/2
        self.screen.blit(scoretext,[scoreXpos,20])

    def draw_lives_left(self):
        """ Draws how many lives the player has left on screen """
        font = pygame.font.SysFont('dejavusans',40)
        livestext1 = font.render('P1 lives: ' + str(self.model.player1.lives), 2, [0,255,0])
        livestext2 = font.render('P2 lives: ' + str(self.model.player2.lives), 2, [255,0,0])
        boxsize1 = livestext1.get_rect()
        boxsize2 = livestext2.get_rect()
        livesXpos1 = (screen_width-boxsize1[2])/2
        livesXpos2 = (screen_width-boxsize2[2])/2
        self.screen.blit(livestext1,[livesXpos1,70])
        self.screen.blit(livestext2,[livesXpos2,120])

    def start(self):
        """ Draws start screen for game """
        self.draw()
        self.screen.blit(bubble_background, (0,0))

        """ Game Title-- Bubble Trouble: Olin Edition """
        Obj_rect = self.obj_surf.get_rect()                                   # centers text on screen
        ObjText_x = self.screen.get_width() / 2 - Obj_rect.width / 2
        ObjText_y = (self.screen.get_height() / 2 - Obj_rect.height / 2) - 150
        self.screen.blit(self.obj_surf, (ObjText_x, ObjText_y-100))

        """ Game Instructions: Press these keys to play """
        Instruct_rect = self.instructions_surf.get_rect()
        InstructText_x = self.screen.get_width() / 2 - Instruct_rect.width / 2
        self.screen.blit(self.instructions_surf, (InstructText_x,ObjText_y+170))

        Instruct2_rect = self.instructions_surf2.get_rect()
        Instruct2Text_x = self.screen.get_width() / 2 - Instruct2_rect.width / 2
        self.screen.blit(self.instructions_surf2, (Instruct2Text_x,ObjText_y+220))

        Start_rect = self.start_surf.get_rect()
        StartText_x = self.screen.get_width() / 2 - Start_rect.width / 2
        self.screen.blit(self.start_surf, (StartText_x, ObjText_y+270))

        Start2_rect = self.start_surf2.get_rect()
        Start2Text_x = self.screen.get_width() / 2 - Start2_rect.width / 2
        self.screen.blit(self.start_surf2, (Start2Text_x, ObjText_y+370))
        pygame.display.flip()

    def pause(self):
        """ Draws pause screen for game """
        Pause_rect = self.pause_surf.get_rect()
        PauseText_x = self.screen.get_width() / 2 - Pause_rect.width / 2
        PauseText_y = self.screen.get_height() / 2 - Pause_rect.height / 2
        self.screen.fill(BLACK)
        self.screen.blit(self.pause_surf, (PauseText_x,PauseText_y))

        """ Draws Olin faces to give player better look at their pretty pics """
        self.screen.blit(mica,(200, 100))
        self.screen.blit(daniel,(200, 600))
        self.screen.blit(willem,(750, 100))
        self.screen.blit(kevin,(1300, 100))
        self.screen.blit(anpan,(1300, 600))
        self.screen.blit(cedric,(750, 600))

        pygame.display.flip()

    def draw_game_over(self):
        """ Draws game over screen for game """
        self.screen.blit(bubble_background, (0,0))

        """ Game Over """
        GameOverText_rect = self.game_over_surf.get_rect()
        GameOverText_x = self.screen.get_width() / 2 - GameOverText_rect.width / 2
        GameOverText_y = self.screen.get_height() / 2 - GameOverText_rect.height / 2 - 250
        self.screen.blit(self.game_over_surf, [GameOverText_x, GameOverText_y])

        """ Press R to Restart """
        RestartText_rect = self.restart_surf.get_rect()
        RestartText_x = self.screen.get_width() / 2 - RestartText_rect.width / 2
        self.screen.blit(self.restart_surf, (RestartText_x, GameOverText_y+60))

        """ You shot: """
        ScoreText_rect = self.score_surf.get_rect()
        ScoreText_x = self.screen.get_width() / 2 - ScoreText_rect.width / 2
        self.screen.blit(self.score_surf, (ScoreText_x, GameOverText_y+165))

        """ You were killed by: """
        ScoreText2_rect = self.score_surf2.get_rect()
        ScoreText2_x = self.screen.get_width() / 2 - ScoreText2_rect.width / 2
        self.screen.blit(self.score_surf2, (ScoreText2_x, GameOverText_y+520))

        """ Who you shot and who killed you based on histogram """
        self.draw_score_sheet(self.model.bubble_hit_list, self.model.character_hit_list)

        """ High Score """
        HiscoreText_rect = self.hiscore_surf.get_rect()
        HiscoreText_x = self.screen.get_width() / 2 - HiscoreText_rect.width / 2
        self.screen.blit(self.hiscore_surf, (HiscoreText_x, 30))

        pygame.display.flip()

#Creates a histogram of items(minus the last 4 characters) in a list
    def hit_list(self,l):
        hist = dict()
        for item in l:
            item = item.replace(CURR_DIR,'')
            item = re.sub('/.*?/', '', item)
            item = item[:-4]
            hist[item] = hist.get(item,0) + 1
        return hist

    def score_sheet(self,hit_list):
        t = []
        for key, value in hit_list.items():
            t.append((value,key))
        t.sort(reverse = True)
        return t

    def draw_score_sheet(self,l1,l2):
        t1 = self.score_sheet(self.hit_list(l1))
        y1 = 385
        for score, person in t1:
            self.score_sheet1 = self.font4.render('{} : {}'.format(person,score),False, WHITE)
            SheetText_rect = self.score_sheet1.get_rect()
            SheetText_x = self.screen.get_width() / 2 - SheetText_rect.width / 2
            self.screen.blit(self.score_sheet1, (SheetText_x, y1))
            y1 += 50
        y2 = 740
        t2 = self.score_sheet(self.hit_list(l2))
        for score, person in t2:
            self.score_sheet2 = self.font4.render('{} : {}'.format(person,score),False, WHITE)
            SheetText2_rect = self.score_sheet2.get_rect()
            SheetText2_x = self.screen.get_width() / 2 - SheetText2_rect.width / 2
            self.screen.blit(self.score_sheet2, (SheetText2_x, y2))
            y2 += 50

class GameMain(object):
    """ Main class """
    def __init__(self, width = screen_width, height = screen_height):
        self.width = width
        self.height = height
        self.model = GameModel()
        self.view = GameView(self.model)
        self.controller = GameController(self.model)
        self.clock = pygame.time.Clock()
        self.pause = False

    def replay(self):
        """ Resets values when game restarts """
        self.model = GameModel()
        self.view = GameView(self.model)
        self.controller = GameController(self.model)
        self.clock = pygame.time.Clock()
        self.pause = False

    def main_menu(self):
        """ Displays main menu and waits for user input """
        start = False
        self.view.start()
        while not start:
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    start = True

    def GameLoop(self):
        """ Game loop """
        done = False

        lastGetTicks = pygame.time.get_ticks()

        while not done:

            if self.pause:
                self.view.pause()
                for event in pygame.event.get():
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_p:
                            self.pause = False
                    elif event.type == pygame.QUIT:
                        done = True
            elif self.model.player1.alive or self.model.player2.alive:
                t = pygame.time.get_ticks()
                dt = (t- lastGetTicks) / 1000.0
                lastGetTicks = t

                self.model.player1.pos = 0
                self.model.player2.pos = 0

                done, self.pause = self.controller.player_mvmt()

                self.model.update(self.model.player1.pos, self.model.player2.pos, dt)
                if self.model.player1.alive:
                    self.model.is_collision(self.model.player1)
                if self.model.player2.alive:
                    self.model.is_collision(self.model.player2)
                self.view.draw()

                self.clock.tick(fps)
            else:
                pygame.time.delay(1000)
                self.model.player1.lives = 3
                self.model.player2.lives = 3
                done = True
                if os.path.exists(CURR_DIR + '/hiscore.txt'):
                    count = pickle.load(open(CURR_DIR + '/hiscore.txt', 'rb'))
                else: count = 0
                if self.model.score > count:
                    count = self.model.score
                pickle.dump(count,open(CURR_DIR + '/hiscore.txt', 'wb'))

def game_over(MainWindow):
    """ Player can restart """
    start = True
    while start:
        MainWindow.view.draw_game_over()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    MainWindow.replay()
                    MainWindow.GameLoop()
            elif event.type == pygame.QUIT:
                start = False
                break

if __name__ == '__main__':
    MainWindow = GameMain()
    MainWindow.main_menu()
    MainWindow.GameLoop()
    game_over(MainWindow)
