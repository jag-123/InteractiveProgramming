"""ball is life"""
import pygame
import os, sys
from pygame.locals import *

if not pygame.mixer: print 'Warning, sound disabled'

gravity = 1
screen_width = 1700
screen_height = 1000

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

pygame.init()
pygame.mixer.init()

bubble_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

b = Ball(8,[1,1])
b2 = Ball(12,[1,1])

bubble_list.add(b)
all_sprites_list.add(b)
all_sprites_list.add(b2)

screen = pygame.display.set_mode((screen_width, screen_height))

done = False

score = 0

b.rect.x = 500
b.rect.y = 100

bubble_pop_sound = load_sound('Bubble_pop.wav')

while not done:
	screen.fill((0,0,0))
	for event in pygame.event.get(): 
		if event.type == pygame.QUIT: 
			done = True

	b.speed[1] += gravity
	b2.speed[1] += gravity

	b.update()
	b2.update()

	bubble_hit_list = pygame.sprite.spritecollide(b2, bubble_list, True)
	for bubble in bubble_hit_list:
		# pygame.sprite.Group.remove(bubble_list, bubble)
		score +=1
		print score
		bubble_pop_sound.play()

	all_sprites_list.draw(screen)
	pygame.display.update()