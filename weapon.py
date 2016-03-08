"""gun for player"""
import pygame

WHITE = (255, 255, 255)

class Gun(pygame.sprite.Sprite):

	def __init__(self, x = 500, y = 1000):
		self.x = x
		self.y = y
		self.active = False
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('arrow2.png')
		#self.rect = self.image.get_rect()

	def update(self):
		if self.active:
			if self.y <= 0:
				self.active = False
			else:
				self.y -= 2
			#self.rect = self.rect.move(0, -10)
		screen.blit(self.image,(self.x,self.y))


gun1 = Gun()


pygame.init()

screen = pygame.display.set_mode((1000, 900))

done = False

while not done:
	screen.fill(WHITE)
	for event in pygame.event.get(): 
		if event.type == pygame.QUIT: 
			done = True
	gun1.update()
	pygame.display.update()