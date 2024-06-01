import pygame as pg
from SpaceShip import *
from Meteor import *
from pygame.locals import *



# Pygame initialization

pg.init()

flags = DOUBLEBUF
root = pg.display.set_mode((800,600), flags, 16)





meteors = Meteor(root,10) 

spaceship = Spaceship(root,meteors)

clock = pg.time.Clock()

bg = pg.image.load("bg.jpg")
bg = pg.transform.scale(bg,(800,600))

# Main loop
running = True
while running:
    clock.tick(60)
    pg.display.set_caption(f'{clock.get_fps()}')
    root.blit(bg,(0,0))  
    spaceship.update()
    meteors.update()
    pg.time.delay(10)  # Add delay to control the frame rate
    pg.display.update()


