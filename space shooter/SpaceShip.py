import pygame as pg

class Spaceship:
    def __init__(self, root, meteor):
        self.root = root
        self.meteor = meteor
        self.resetGame()

        # Load the spaceship image once
        self.image = pg.image.load("spaceShip.png")
        self.resized_image = pg.transform.scale(self.image, (90, 90))
        self.font = pg.font.Font(None, 74)
        self.score = 0

    def resetGame(self):
        self.meteor.lostMeteors = 0
        self.ship_x = 400
        self.ship_y = 500
        self.speed = 6
        self.dx = 0
        self.bulletSpeed = 10
        self.bullets = []
        self.bullet_cooldown = 200  # milliseconds
        self.last_shot_time = pg.time.get_ticks()
        self.game_over = False
        self.meteor.meteors = []
        self.meteor.createMeteors()

    def drawShip(self):
        ship_rect = pg.Rect(self.ship_x, self.ship_y, 90, 90)
        self.root.blit(self.resized_image, ship_rect)

    def moveShip(self):
        self.dx = 0  # Reset movement

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.dx = -self.speed
        if keys[pg.K_d]:
            self.dx = self.speed
        if keys[pg.K_SPACE]:
            self.shootBullet()
        if keys[pg.K_r] and self.game_over:
            self.resetGame()

        # Update the ship position and check boundaries
        self.ship_x = max(0, min(self.ship_x + self.dx, 710))  # 800 - 90

    def gameOver(self):
        self.game_over = True
        self.score = 0
        
        text = self.font.render('Game Over', True, (255, 0, 0))
        self.root.blit(text, (250, 300))
        font = pg.font.Font(None, 36)
        text = font.render('     Press R to play again', True, (255, 255, 255))
        self.root.blit(text, (230, 380))
        #pg.display.flip()

    def checkCol(self):
        ship_rect = pg.Rect(self.ship_x, self.ship_y, 50, 50)

        # Copy bullets and meteors to avoid modifying the list while iterating
        bullets_to_remove = []
        meteors_to_remove = []

        for meteor in self.meteor.meteors:
            meteor_rect = pg.Rect(meteor['x'] + 55, meteor['y'] + 70, 45, 45)
            if ship_rect.colliderect(meteor_rect):
                self.gameOver()
                return

            for bullet in self.bullets:
                bullet_rect = pg.Rect(bullet[0] - 2.5, bullet[1] - 2.5, 2, 2)
                if meteor_rect.colliderect(bullet_rect):
                    bullets_to_remove.append(bullet)
                    meteors_to_remove.append(meteor)
                    self.score += 1

        for bullet in bullets_to_remove:
            self.bullets.remove(bullet)
        for meteor in meteors_to_remove:
            self.meteor.meteors.remove(meteor)
            self.meteor.createMeteors()

    def shootBullet(self):
        current_time = pg.time.get_ticks()
        if current_time - self.last_shot_time > self.bullet_cooldown:
            bullet_x = self.ship_x + 45  # Center of the ship
            bullet_y = self.ship_y
            self.bullets.append([bullet_x, bullet_y])  # Append as a list to allow mutation
            self.last_shot_time = current_time

    def updateBullets(self):
        for bullet in self.bullets:
            bullet[1] -= self.bulletSpeed  # Update the y-coordinate of the bullet
            pg.draw.circle(self.root, (255, 255, 255), (bullet[0], bullet[1]), 5)

        # Remove bullets that have moved off the screen
        self.bullets = [bullet for bullet in self.bullets if bullet[1] > 0]

    def update(self):
        
        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.root.blit(score_text,(520,50))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_r and self.game_over:
                self.resetGame()
        
        if self.meteor.lostMeteors == 3:
            self.game_over = True
        
        

        if not self.game_over:
            lostMeteors_text = self.font.render(f'{self.meteor.lostMeteors}', True, (255, 255, 255))
            
            self.root.blit(lostMeteors_text,(50,50))
           
            self.moveShip()
            self.drawShip()
            self.updateBullets()
            self.checkCol()
        else:
            self.gameOver()
            