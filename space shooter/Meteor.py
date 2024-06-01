import pygame as pg
import random as r

class Meteor:

    def __init__(self, root, maxCount=5):
        self.root = root
        self.maxCount = maxCount
        self.meteors = []
        self.lostMeteors = 0
        
        # Load the meteor image once
        self.meteor_Image = pg.image.load("meteor.png")
        self.meteor_Image = pg.transform.scale(self.meteor_Image, (180, 180))
        
        self.createMeteors()

    def createMeteors(self):
        while len(self.meteors) < self.maxCount:
            x = r.randint(10, 700)
            y = r.randint(-800, -100)  # Start above the screen
            speed = 2
            self.meteors.append({'x': x, 'y': y, 'speed': speed})

    def drawMeteor(self, meteor):
        self.root.blit(self.meteor_Image, (meteor['x'], meteor['y']))

    def update(self):
        for meteor in self.meteors:
            meteor['y'] += meteor['speed']
            if meteor['y'] > 650:
                self.lostMeteors += 1
                meteor['y'] = -120  # Reset position to top
                meteor['x'] = r.randint(10, 720)  # Randomize x position again
            self.drawMeteor(meteor)
