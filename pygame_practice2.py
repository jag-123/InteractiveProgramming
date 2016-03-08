"""
sprite stuff
"""
import pygame
import random

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
Aqua = (0,255,255)
Blue = (0,0,255)
Fuchsia = (255,0,255)
Gray = (128,128,128)
Green = (0,128,0)
Lime = (0,255,0)
Maroon = (128, 0 ,0)
Navy_Blue = (0,0,128)
Olive = (128,128,0)
Purple = (128,0,128)
Silver = (192,192,192)
Teal = (0,128,128)
Yellow = (255,255,0)

class Rectangle(pygame.sprite.Sprite):

    def __init__(self, color, width, height):

        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        #blank surface
        self.image.fill(color)
 
        self.rect = self.image.get_rect()
 
pygame.init()

screen_width = 900
screen_height = 900
screen = pygame.display.set_mode([screen_width, screen_height])
caption = pygame.display.set_caption('Jeremy is awesome') 
# list of sprites
rectangle_list = pygame.sprite.Group()
 
# This is a list of every sprite. 
all_sprites_list = pygame.sprite.Group()
 
for i in range(50):
    # This represents a block
    block = Rectangle(Navy_Blue, 20, 15)
 
    # Set a random location for the block
    block.rect.x = random.randrange(screen_width-20)
    block.rect.y = random.randrange(screen_height-15)
 
    # Add the block to the list of objects
    rectangle_list.add(block)
    all_sprites_list.add(block)
 
# Create a RED player block
player = Rectangle(RED, 20, 15)
all_sprites_list.add(player)
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
score = 0
 
if __name__ == '__main__':
    while not done:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                done = True
     
        # Clear the screen
        screen.fill(Fuchsia)
     
        # Get the current mouse position. This returns the position
        # as a list of two numbers.
        pos = pygame.mouse.get_pos()
     
        # Fetch the x and y out of the list,
           # just like we'd fetch letters out of a string.
        # Set the player object to the mouse location
        player.rect.x = pos[0]
        player.rect.y = pos[1]
     
        # See if the player block has collided with anything.
        blocks_hit_list = pygame.sprite.spritecollide(player, rectangle_list, True)
     
        # Check the list of collisions.
        for block in blocks_hit_list:
            score += 1
            print(score)
     
        # Draw all the spites
        all_sprites_list.draw(screen)
     
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
     
        # Limit to 60 frames per second
        clock.tick(60)
     
    pygame.quit()