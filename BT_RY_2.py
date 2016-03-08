"""player for game"""
import pygame
import os, sys
from pygame.locals import *

if not pygame.mixer: print 'Warning, sound disabled' 

gravity = 1
screen_width = 1700
screen_height = 900

def load_sound(name):
    """ Loads specific sound into game """
    class Nonesound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', wav
        raise SystemExit, message
    return sound

class Player(object):
    def __init__(self):
        self.x = 500
        self.y = 834
        self.img_left = pygame.image.load('character1_edit.png')
        self.img_default = pygame.image.load('character2_edit.png')
        self.img_right = pygame.image.load('character3_edit.png')

    def update(self, pos):
        if pos == 1:
            self.x += pos + 4
            screen.blit(self.img_right,(self.x,self.y))
            if self.x >= screen_width - 48 :
                self.x = screen_width - 48

        elif pos == -1:
            self.x += pos - 4
            screen.blit(self.img_left,(self.x,self.y))
            if self.x <= 0:
                self.x = 0

        else:
            screen.blit(self.img_default,(self.x,self.y))

class Gun(pygame.sprite.Sprite):

    def __init__(self, x = 0, y = 0):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.active = False
        self.image = pygame.image.load('arrow2.png')
        self.rect = self.image.get_rect()

    def update(self):
        if self.active:
            #screen.blit(self.image,(self.x,self.y))
            if self.y <= 0:
                self.active = False
            else:
                self.y -= 10
            #self.rect = self.rect.move(0, -10)

class Ball(pygame.sprite.Sprite):
    def __init__(self, size, speed, x = 0, y = 0):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.speed = speed
        self.image = pygame.image.load('small_bubble1.png')
        self.image = pygame.transform.scale(self.image,(size*10,size*10))
        self.rect = self.image.get_rect()

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

    def walls(self,number, min_number, max_number):
        self.number = number
        self.min_number = min_number
        self.max_number = max_number
        return min(max(self.number,self.min_number),self.max_number)

player = Player()
gun1 = Gun()
pos = 0

pygame.init()
pygame.mixer.init()

bubble_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

b = Ball(8,[1,1])
b2 = Ball(12,[1,1])

bubble_list.add(b)
bubble_list.add(b2)
all_sprites_list.add(b)
all_sprites_list.add(b2)

#all_sprites_list.add(gun1)

screen = pygame.display.set_mode((screen_width, screen_height))

done = False

score = 0

b.rect.x = 500
b.rect.y = 100

bubble_pop_sound = load_sound('Bubble_pop.wav')

background = pygame.image.load('background1.png')
#screen.blit(background,(0,0))
while not done:
    #screen.fill((255, 255, 255))
    screen.blit(background,(0,0))

    key = pygame.key.get_pressed()

    for event in pygame.event.get():
        pass     

    if event.type == pygame.QUIT: 
        done = True
    elif key[pygame.K_LEFT] and key[pygame.K_RIGHT]:
        pos = 0
    elif key[pygame.K_RIGHT]:
        pos = 1
    elif key[pygame.K_LEFT]:
        pos = -1
    elif event.type == pygame.KEYUP:
        pos = 0

    if key[pygame.K_SPACE] and gun1.active == False:
        #screen.blit(player.img_default,(player.x,player.y))
        gun1.active = True
        gun1.x = player.x+20
        gun1.y = player.y
        all_sprites_list.add(gun1)

    b.speed[1] += gravity
    b2.speed[1] += gravity

    b.update()
    b2.update()

    bubble_hit_list = pygame.sprite.spritecollide(gun1, bubble_list, True)
    for bubble in bubble_hit_list:
        # pygame.sprite.Group.remove(bubble_list, bubble)
        score +=1
        print score
        bubble_pop_sound.play()
    
    gun1.update()
    player.update(pos)
    all_sprites_list.draw(screen)
    pygame.display.update()