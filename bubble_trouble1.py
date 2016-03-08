"""player for game"""
import pygame

gravity = 1
screen_width = 1700
screen_height = 900

class Player(object):
    def __init__(self):
        self.x = 500
        self.y = 700
        self.img_left = pygame.image.load('character1_edit.png')
        self.img_default = pygame.image.load('character2_edit.png')
        self.img_right = pygame.image.load('character3_edit.png')

    def update(self, pos):
        if pos == 1:
            self.x += pos + 4
            screen.blit(self.img_right,(self.x,self.y))
        elif pos == -1:
            self.x += pos - 4
            screen.blit(self.img_left,(self.x,self.y))
        else:
            screen.blit(self.img_default,(self.x,self.y))

class Gun(object):

    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
        self.active = False
        #pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('arrow2.png')
        #self.rect = self.image.get_rect()

    def update(self):
        if self.active:
            screen.blit(self.image,(self.x,self.y))
            if self.y <= 0:
                self.active = False
            else:
                self.y -= 10
            #self.rect = self.rect.move(0, -10)

player = Player()
gun1 = Gun()
pos = 0

pygame.init()

all_sprites_list = pygame.sprite.Group()

screen = pygame.display.set_mode((screen_width, screen_height))

done = False

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
        screen.blit(player.img_default,(player.x,player.y))
        gun1.active = True
        gun1.x = player.x+20
        gun1.y = player.y
        #all_sprites_list.add(gun1)

    player.update(pos)
    gun1.update()
    pygame.display.update()