import pygame
from pygame import mixer
from pygame.locals import *
import os
from random import randint

playerWalk = []

playerX = 100
playerY = 400

cloudX = 400
cloudY = 0

EnemyX = 400
EnemyY = 450

EnemySpeed = 5

EnemyWidth = 200
EnemyHeight = 100

walkCount = 0

jumped = False

airTime = 0

pygame.init()

channel = mixer.Channel(0)

jump = mixer.Sound("sound/jump.wav")

font = pygame.font.Font("font.otf",20)

win = pygame.display.set_mode((800,600))

pygame.display.set_caption("Dino game@RaderH2O")
# Load player images :
for i in range(5):
    playerWalk.append(pygame.image.load(os.path.join(os.path.dirname(__file__),"img",f"p{i}.png")))


# Cloud :
class Cloud:
    def show(cloudX,cloudY):
        win.blit(pygame.image.load("img/cloud.png"),(cloudX,cloudY))

# Enemy :
class Enemy:
    EnemyX = 0

    def show(EnemyX,EnemyY,EnemyWidth,EnemyHeight):
        win.blit(pygame.transform.scale(pygame.image.load("img/crocodile.png"),(EnemyWidth,EnemyHeight)),(EnemyX,EnemyY))

    def move(speed):
        global EnemyX
        EnemyX -= speed

    def check():
        global EnemyX
        if EnemyX < -200:
            EnemyX = 800
            return True
        return False

done = False

jumpVal = 0

score = 0

# Clock :
clock = pygame.time.Clock()

while not done:
    walkCount += 0.2
    if walkCount >= 40:
        walkCount = 0

    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        elif event.type == KEYDOWN:
            if event.key == K_q:
                done = True
            if event.key == K_SPACE:
                if jumped != True:
                    channel.play(jump,0)
                    jumped = True
                    jumpVal = 19
    
    if jumped and airTime < 20:
        airTime += 1
        playerY -= jumpVal
        jumpVal -= 2
    elif airTime >= 20:
        jumped = False
        jumpVal = 19
        airTime = 0

    win.blit(pygame.image.load("img/bg.png"),(0,0))
    cloud = Cloud
    if cloudX > -100:
        cloudX -= 1.5
    elif cloudX < 0:
        cloudX = 800
        cloudY = randint(0,100)
    cloud.show(int(cloudX),int(cloudY))
    win.blit(pygame.transform.scale(playerWalk[int(walkCount % 5)],(64,64)),(playerX,playerY))
    enemy = Enemy
    enemy.show(EnemyX,EnemyY,EnemyWidth,EnemyHeight)
    enemy.move(EnemySpeed)
    if enemy.check():
        if EnemySpeed < 18:
            EnemySpeed += 1
    win.blit(font.render("\"Q\" - Quit                \"Space\" - Jump",False,(250,250,250)),(10,50))
    pygame.display.update()
    if EnemyX + EnemyWidth > playerX and EnemyX + EnemyWidth < playerX + 64 and EnemyY - EnemyHeight < playerY - 40:
        pygame.time.delay(1000)
        done = True

    clock.tick(40)

pygame.quit()
