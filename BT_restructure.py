"""player for game"""
import pygame
import os, sys
from pygame.locals import * 
import random
import time

# define font/fill colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREY = (105,105,105)

# define constant variables 
gravity = 1
screen_width = 1700
screen_height = 900
fps = 120

# prepare/load pictures 
pictures = ['cedric.png','daniel.png','willem.png','kevin.png','anpan.png']

pygame.display.set_caption('Hot Tamales Awesome Game')

background = pygame.image.load('olin.png')
bubble_background = pygame.image.load('bubble_background.png')

pygame.time.set_timer(pygame.USEREVENT, 1000)

pygame.mixer.init()                                                     # initializes sound mixer

bubble_pop_sound = pygame.mixer.Sound('bubble_pop.ogg')
player_hit_sound = pygame.mixer.Sound('Frant_edit2.ogg')

class Player(pygame.sprite.Sprite):
    """ Main character for game """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True                   # if False, game over
        self.img_left = pygame.image.load('character1_edit.png')        # 3 pictures for each direction character is facing
        self.img_default = pygame.image.load('character2_edit.png')
        self.img_right = pygame.image.load('character3_edit.png')
        self.image = self.img_default
        self.rect = self.image.get_rect()
        self.gun = Gun()
        self.rect.left = screen_width/2
        self.rect.top = 834

    def update(self, pos):
        self.pos = pos
        if self.alive:
            if self.pos == 1:                                           # if right key is pressed, character moves right
                self.rect.left += self.pos + 5
                if self.rect.left >= screen_width - 48 :                # won't go past edge of screen
                    self.rect.left = screen_width - 48

            elif self.pos == -1:                                        # if left key is pressed, character moves left
                self.rect.left += self.pos - 5
                if self.rect.left <= 0:                                 # won't go past edge of screen
                    self.rect.left = 0

class Gun(pygame.sprite.Sprite):
    """ Weapon that shoots arrow to pop bubbles """
    def __init__(self, x = 0, y = 0):
        pygame.sprite.Sprite.__init__(self)
        self.active = False                                             # won't fire unless space key is pressed
        self.image = pygame.image.load('arrow2.png')
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y

    def update(self):
        if self.active:
            if self.rect.top <= 0:                                      # disappears when hits top of screen                      
                self.active = False
                self.kill()
            else:
                self.rect.top -= 10
        else:
            self.kill()

class Ball(pygame.sprite.Sprite):
    """ Bubbles that character needs to pop """
    def __init__(self, size, speed, x = 0, y = 0):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.speed = speed
        self.pic = random.choice(pictures)                              # randomly chooses between given pictures of fellow classmates
        self.image = pygame.image.load(self.pic)
        self.image = pygame.transform.scale(self.image,(size*10,size*10))
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y

    def update(self):
        self.rect = self.rect.move(self.speed)

        if self.rect.left < 0 or self.rect.right > screen_width:        # bubbes bounce off of left/right/top/bottom walls
            self.speed[0] = -self.speed[0]
        if self.rect.top < 100 or self.rect.bottom > screen_height:
            self.speed[1] = -self.speed[1]

        self.rect.left = self.walls(self.rect.left, 0 , screen_width)
        self.rect.right = self.walls(self.rect.right, 0 , screen_width)
        self.rect.top = self.walls(self.rect.top, 100 , screen_height)
        self.rect.bottom = self.walls(self.rect.bottom, 0 , screen_height)

        self.speed[1] += gravity                                        # simulates effect of gravity

    def walls(self,number, min_number, max_number):
        self.number = number
        self.min_number = min_number
        self.max_number = max_number
        return min(max(self.number,self.min_number),self.max_number)

class GameModel(object):
    """ Model for game """

    def __init__(self):
        self.width = screen_width
        self.height = screen_height

        self.count = 0
        self.score = 0
        self.lives = 3
        self.player1 = Player()

        self.alive = self.player1.alive

        self.balls = []

        self.character_hit_list = []
        self.bubble_hit_list = []

        self.original_size = 4
        self.original_x_speed = 5
        self.original_y_speed = 3

        self.balls.append(Ball(self.original_size,[self.original_x_speed,self.original_y_speed]))

        self.list_of_bubbles = pygame.sprite.Group()
        self.player_list = pygame.sprite.Group()
        self.gun_list = pygame.sprite.Group()

    # def more_balls(self):
    #     self.count = 0
    #     if not self.balls:
    #         self.count += 1
    #         print self.count
    #     if self.count == 1:
    #         self.balls.append(Ball(4,[5,3]))
    #         print self.count
        # elif self.count == 2:
        #     self.balls.append(Ball(4,[5,3]))
        #     self.balls.append(Ball(4,[-5,3],screen_width))
        #     self.count += 1

        # seconds = (pygame.time.get_ticks())/1000
        # if seconds == 2:
        #     self.balls.append(Ball(4,[5,3]))
        
    def update(self, pos):
        """ Updates all sprites """
        self.list_of_bubbles.update()
        self.player_list.update(pos)
        self.gun_list.update()

        for ball in self.balls:
            self.list_of_bubbles.add(ball)

        self.player_list.add(self.player1)        

    def is_collision(self,player,bubble_list):
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
                self.lives -= 1
                player.gun.active = False
                ball.kill()
                self.split_ball(index)
                pygame.time.delay(500)

                if self.lives <= 0:
                    self.alive = False

    def split_ball(self,index):
        """ Splits bubbles into 2 smaller bubbles once hit by arrow """
        ball = self.balls[index]
        del self.balls[index]

        if ball.size > 2:
            self.balls.append(Ball(ball.size-2,[-3,-3], ball.rect.left - 5, ball.rect.top-200))
            self.balls.append(Ball(ball.size-2,[3,-3], ball.rect.left + 5, ball.rect.top-200))


    def draw_sprites(self):
        """ Draw all sprites onto screen """
        all_sprites_list = [self.list_of_bubbles, self.gun_list, self.player_list]
        return all_sprites_list

class GameController(object):
    """ Controller for game. 
    When certain key is pressed, does specific action """
    def __init__(self, model):
        self.model = model
        self.done = False
        self.pause = False

    def player_mvmt(self):
        """ Organizes keypresses """
        key = pygame.key.get_pressed()
        self.pause = False
        player1 = Player()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                self.done = True
            elif key[pygame.K_p]:
                self.pause = True

        if key[pygame.K_LEFT] and key[pygame.K_RIGHT]:
            self.model.player1.pos = 0
            self.model.player1.image = self.model.player1.img_default
        elif key[pygame.K_RIGHT]:
            self.model.player1.pos = 1
            self.model.player1.image = self.model.player1.img_right
        elif key[pygame.K_LEFT]:
            self.model.player1.pos = -1
            self.model.player1.image = self.model.player1.img_left
        else:
            self.model.player1.image = self.model.player1.img_default

        if key[pygame.K_SPACE] and self.model.player1.gun.active == False:
            self.model.gun_list.add(self.model.player1.gun)
            self.model.player1.gun.active = True
            self.model.player1.gun.rect.left = self.model.player1.rect.left+20
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
        self.pause_surf = self.font2.render('PRESS P TO UNPAUSE', False, WHITE)
        self.obj_surf = self.font1.render('BUBBLE TROUBLE: OLIN EDITION', False, GREY)
        self.instructions_surf = self.font.render('LEFT AND RIGHT ARROW KEYS TO MOVE', False, WHITE)
        self.instructions_surf2 = self.font.render('SPACE TO SHOOT', False, WHITE)
        self.start_surf = self.font.render('PRESS P TO PAUSE', False, WHITE)
        self.start_surf2 = self.font.render('PRESS ANY KEY TO START', False, BLACK)
        self.game_over_surf = self.font2.render('GAME OVER', False, RED)
        self.restart_surf = self.font2.render('PRESS R TO RESTART', False, RED)

    def draw(self, alive):
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
        livestext = font.render('Lives remaining: ' + str(self.model.lives), 2, [255,255,255])
        boxsize = livestext.get_rect()
        livesXpos = (screen_width-boxsize[2])/2
        self.screen.blit(livestext,[livesXpos,70])

    def start(self):
        """ Draws start screen for game """
        self.draw(True)
        self.screen.blit(bubble_background, (0,0))

        Obj_rect = self.obj_surf.get_rect()                                   # wordy, but used to center text on screen 
        ObjText_x = self.screen.get_width() / 2 - Obj_rect.width / 2
        ObjText_y = (self.screen.get_height() / 2 - Obj_rect.height / 2) - 150
        self.screen.blit(self.obj_surf, (ObjText_x, ObjText_y-100))

        # Obj2_rect = self.obj_surf2.get_rect()
        # Obj2Text_x = self.screen.get_width() / 2 - Obj2_rect.width / 2
        # self.screen.blit(self.obj_surf2, (Obj2Text_x, ObjText_y+70))

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
        #self.screen.blit(pause_background, (0,0))
        self.screen.blit(self.pause_surf, (PauseText_x,PauseText_y))

        pygame.display.flip()

    def draw_game_over(self):
        """ Draws game over screen for game """
        self.screen.blit(bubble_background, (0,0))

        GameOverText_rect = self.game_over_surf.get_rect()
        GameOverText_x = self.screen.get_width() / 2 - GameOverText_rect.width / 2
        GameOverText_y = self.screen.get_height() / 2 - GameOverText_rect.height / 2 - 300
        self.screen.blit(self.game_over_surf, [GameOverText_x, GameOverText_y])
        

        RestartText_rect = self.restart_surf.get_rect()
        RestartText_x = self.screen.get_width() / 2 - RestartText_rect.width / 2
        self.screen.blit(self.restart_surf, (RestartText_x, GameOverText_y+100))
        pygame.display.flip()

#Creates a histogram of items(minus the last 4 characters) in a list 
    def hit_list(self,l):
        hist = dict()
        for item in l:
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
        self.font.render('You shot:', False, RED)
        t1 = self.score_sheet(self.hit_list(l1))
        for score, person in t1:
            self.font.render('{} : {}'.format(person,score),False, RED)
        self.font.render('You were touched by:', False, RED)
        t2 = self.score_sheet(self.hit_list(l2))
        for score, person in t2:
            self.font.render('{} : {}'.format(person,score),False, RED)
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
        start_ticks = pygame.time.get_ticks()
        while not done:

            if self.pause:
                self.view.pause()
                for event in pygame.event.get():
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_p:
                            self.pause = False
                    elif event.type == pygame.QUIT:
                        done = True
            elif self.model.alive:
                self.model.player1.pos = 0
                done, self.pause = self.controller.player_mvmt()
                self.model.update(self.model.player1.pos)
                self.model.is_collision(self.model.player1, self.model.list_of_bubbles)
                #self.model.more_balls()
                self.view.draw(self.model.alive)
                self.clock.tick(fps)
                seconds = (pygame.time.get_ticks()-start_ticks)/10
                if seconds == 100:
                    self.model.balls.append(Ball(4,[5,3]))
                elif seconds > 3000:
                    self.model.balls.append(Ball(6,[5,3]))
            else:
                print self.view.score_sheet(self.view.hit_list(self.model.bubble_hit_list))
                print self.view.score_sheet(self.view.hit_list(self.model.character_hit_list))
                #self.view.draw_score_sheet(self.model.bubble_hit_list,self.model.character_hit_list)
                self.model.score = 0
                self.model.lives = 3
                done = True
    
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