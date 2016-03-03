"""ball is life"""
import pygame

gravity = 1
screen_width = 1700
screen_height = 1000

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

		screen.blit(self.image,self.rect)

	def walls(self,number, min_number, max_number):
		self.number = number
		self.min_number = min_number
		self.max_number = max_number
		return min(max(self.number,self.min_number),self.max_number)

pygame.init()

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
		score +=1
		print score

	all_sprites_list.draw(screen)
	pygame.display.update()