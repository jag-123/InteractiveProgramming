"""player for game"""
import pygame

class Player(object):
	def __init__(self):
		self.x = 500
		self.y = 700
		self.img_left = pygame.image.load('character1.png')
		self.img_default = pygame.image.load('character2.png')
		self.img_right = pygame.image.load('character3.png')

	def update(self, pos):
		if pos == 1:
			self.x += pos
			screen.blit(self.img_right,(self.x,self.y))
		elif pos == -1:
			self.x += pos
			screen.blit(self.img_left,(self.x,self.y))
		else:
			screen.blit(self.img_default,(self.x,self.y))

player = Player()
pos = 0

pygame.init()

screen = pygame.display.set_mode((1000, 900))

done = False

while not done:
	screen.fill((255, 255, 255))
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


	player.update(pos)
	pygame.display.update()