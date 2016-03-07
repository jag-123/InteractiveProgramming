"""player for game"""
import pygame
import os, sys
from pygame.locals import *

if not pygame.mixer: print 'Warning, sound disabled' 

gravity = 1
screen_width = 1700
screen_height = 900
fps = 120
score = 0
lives = 3

def load_sound(name):
    """ Loads specific sound into game """
    class Nonesound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('data', name)
    sound = pygame.mixer.Sound(fullname)
    return sound

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.img_left = pygame.image.load('character1_edit.png')
        self.img_default = pygame.image.load('character2_edit.png')
        self.img_right = pygame.image.load('character3_edit.png')
        self.image = self.img_default
        self.rect = self.image.get_rect()
        self.gun = Gun()
        self.rect.left = screen_width/2
        self.rect.top = 834

    def update(self):
        if pos == 1:
            self.rect.left += pos + 5
            if self.rect.left >= screen_width - 48 :
                self.rect.left = screen_width - 48

        elif pos == -1:
            self.rect.left += pos - 5
            if self.rect.left <= 0:
                self.rect.left = 0

class Gun(pygame.sprite.Sprite):

    def __init__(self, x = 0, y = 0):
        pygame.sprite.Sprite.__init__(self)
        self.active = False
        self.image = pygame.image.load('arrow2.png')
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y

    def update(self):
        if self.active:
            if self.rect.top <= 0:
                self.active = False
                self.kill()
            else:
                self.rect.top -= 10
        else:
            self.kill()

class Ball(pygame.sprite.Sprite):
    def __init__(self, size, speed, x = 0, y = 0):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.speed = speed
        self.image = pygame.image.load('small_bubble1.png')
        self.image = pygame.transform.scale(self.image,(size*10,size*10))
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y

    def update(self):
        self.rect = self.rect.move(self.speed)

        if self.rect.left < 0 or self.rect.right > screen_width:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 100 or self.rect.bottom > screen_height:
            self.speed[1] = -self.speed[1]

        self.rect.left = self.walls(self.rect.left, 0 , screen_width)
        self.rect.right = self.walls(self.rect.right, 0 , screen_width)
        self.rect.top = self.walls(self.rect.top, 100 , screen_height)
        self.rect.bottom = self.walls(self.rect.bottom, 0 , screen_height)

        self.speed[1] += gravity

    def walls(self,number, min_number, max_number):
        self.number = number
        self.min_number = min_number
        self.max_number = max_number
        return min(max(self.number,self.min_number),self.max_number)

class Game(object):

    def __init__(self):
        self.game_over = False
        self.balls = []
        self.balls.append(Ball(10,[6,4]))
        #self.balls.append(Ball(3,[-5,3],screen_width,100))
        #self.balls.append(Ball(10,[4,2]))
        #self.balls.append(Ball(12,[3,1]))
        self.list_of_bubbles = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()

    def score(self):
        font = pygame.font.SysFont('ubuntu',50)
        scoretext = font.render('Score: ' + str(score), 2, [255,255,255])
        boxsize = scoretext.get_rect()
        scoreXpos = (screen_width-boxsize[2])/2
        screen.blit(scoretext,[scoreXpos,20])

    def lives_left(self):
        font = pygame.font.SysFont('ubuntu',40)
        livestext = font.render('Lives remaining: ' + str(lives), 2, [255,255,255])
        boxsize = livestext.get_rect()
        livesXpos = (screen_width-boxsize[2])/2
        screen.blit(livestext,[livesXpos,70])

    def startround_counter(self):
        font = pygame.font.SysFont('ubuntu',150)
        timertext = font.render(str(counter+1), 2, [255,0,0])
        boxsize = timertext.get_rect()
        timerXpos = (screen_width-boxsize[2])/2
        screen.blit(timertext,[timerXpos,400])
        pygame.time.delay(1000)

    def is_collision(self,player,bubble_list):
        for index, ball in enumerate(self.balls):
            if player.gun.active and pygame.sprite.collide_rect(player.gun, ball):
                global score
                score +=1
                bubble_pop_sound.play()
                player.gun.active = False
                ball.kill()
                self.split_ball(index)

            if pygame.sprite.collide_rect(player,ball):
                global lives
                lives -= 1
                player.gun.active = False
                ball.kill()
                self.split_ball(index)
                pygame.time.delay(500)

                if lives == 0:
                    self.game_over = True
                    #player.kill()

    def split_ball(self,index):
        ball = self.balls[index]
        self.balls.pop(index)
        if ball.size > 2:
            self.balls.append(Ball(ball.size-2,[-3,-3], ball.rect.left - 5, ball.rect.top-200))
            self.balls.append(Ball(ball.size-2,[3,-3], ball.rect.left + 5, ball.rect.top-200))

    def update(self):
        for ball in self.balls:
            self.list_of_bubbles.add(ball)
            self.all_sprites_list.add(ball)

game = Game()
# if not game.balls:
#     game.balls.append(Ball(10,[6,4]))
player1 = Player()
pos = 0

pygame.init()
pygame.display.set_caption('Hot Tamales Awesome Game')
pygame.mixer.init()

game.all_sprites_list.add(player1)

screen = pygame.display.set_mode((screen_width, screen_height))

bubble_pop_sound = load_sound('Bubble_pop.wav')

background = pygame.image.load('background1.png')

counter = 3
pygame.time.set_timer(pygame.USEREVENT, 1000)

done = False
while not done:
    screen.blit(background,(0,0))

    game.score()
    game.lives_left()

    key = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.USEREVENT:
            if counter > -1:
                counter -= 1
                game.startround_counter()

    if counter == -1:
        game.is_collision(player1, game.list_of_bubbles)
        game.update()

        for sprite in game.all_sprites_list:
            sprite.update()

    if event.type == pygame.QUIT: 
        done = True
    elif key[pygame.K_LEFT] and key[pygame.K_RIGHT]:
        pos = 0
        player1.image = player1.img_default
    elif key[pygame.K_RIGHT]:
        pos = 1
        player1.image = player1.img_right
    elif key[pygame.K_LEFT]:
        pos = -1
        player1.image = player1.img_left
    elif event.type == pygame.KEYUP:
        pos = 0
        player1.image = player1.img_default

    if key[pygame.K_SPACE] and player1.gun.active == False:
        game.all_sprites_list.add(player1.gun)
        player1.gun.active = True
        player1.gun.rect.left = player1.rect.left+20
        player1.gun.rect.top = player1.rect.top
        player1.image = player1.img_default

    if game.game_over:
        font = pygame.font.SysFont('ubuntu',150)
        text = font.render("Game Over", True, (255,0,0))
        text_rect = text.get_rect()
        text_x = screen.get_width() / 2 - text_rect.width / 2
        text_y = screen.get_height() / 2 - text_rect.height / 2
        screen.blit(text, [text_x, text_y])

    game.all_sprites_list.draw(screen)
    pygame.display.update()

    clock = pygame.time.Clock()

    clock.tick(fps)

pygame.quit()
sys.exit()