#some comments are used for debugging purpose! 
# pygame
import pygame
import random
from math import sqrt
from pygame import mixer
# initialising
pygame.init()

# creating screen
screen = pygame.display.set_mode((800, 600))

running = True

#title and Icon
pygame.display.set_caption("Space Invader")

icon = pygame.image.load("ufo.png")

pygame.display.set_icon(icon)

#background music
mixer.music.load("background.wav")
mixer.music.play(-1)

player_img = pygame.image.load("IFO.png")
pl_X = 370
pl_Y = 400
pl_X_chng = 0
pl_Y_chng = 0

#enemy_img = pygame.image.load("alien.png")
# en_X = random.randint(0,736)
# en_Y = random.randint(25,100)

# en_X_chng = 4
# en_Y_chng = 30

#let's create multiple enemies
ene_img = [pygame.image.load("alien.png") for  i in range(6)]
en_X = [random.randint(0,736) for i in range(6)]
en_Y = [random.randint(35,100) for i in range(6)]
en_X_chng = [4 for i in range(6)]
en_Y_chng = [30  for i in range(6)]

# Background image
back_img = pygame.image.load("101.jpg")
# Ready - can't see the bullet on the screen
# Fire  - The bullet id currently moving
# bullet image
bull_img = pygame.image.load("coronavirus.png")
bull_X = 370
bull_Y = 400

bull_X_chng = 0
bull_Y_chng = 3
bull_state = "Ready"


def player(x, y):
    screen.blit(player_img, (x, y))  # draw img


def fire_bullet(x, y):
    global bull_state
    bull_state = "Fire"
    screen.blit(bull_img, (x+16, y+10))

#display enemy
def enemy(x,y):
    screen.blit(ene_img[0],(x,y))#draw enemy
# qutting pygame window

# distance between enemy and bullet


def dist_bull_ene(x1, y1, x2, y2):
    return sqrt((x1-x2)**2 + (y1-y2)**2)
#score

score = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX  = 10
textY = 10

#to display scores
def show_score(x,y):
    val = font.render("Score : "+str(score),True,(255,255,255))
    screen.blit(val,(x,y))

#game over text
def game_over_text():
    font = pygame.font.Font('freesansbold.ttf',108)
    val = font.render("Game Over!",True,(0,255,255))
    screen.blit(val,(130,100))
    font1 = pygame.font.Font('freesansbold.ttf',64)
    val2 = font1.render("Total Score : "+str(score),True,(255,0,255))
    screen.blit(val2,(150,220))
while running:
    # background colour
    # R->red,G->green,B->blue
    screen.fill((0, 0, 0))
    # adding background image
    screen.blit(back_img, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # if keyStrokes is pressed check whether it right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pl_X_chng = -3
                #print("Left is pressed!")

            if event.key == pygame.K_SPACE:
                if bull_state is "Ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bull_X = pl_X
                    fire_bullet(pl_X, bull_Y)

            if event.key == pygame.K_RIGHT:
                pl_X_chng = 2
                #print("Right is pressed!")
            if event.key == pygame.K_UP:
                pl_Y_chng = -2
                #print("Left is pressed!")
            if event.key == pygame.K_DOWN:
                pl_Y_chng = 2
                #print("Right is pressed!")
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                #print("Key's released!")
                pl_X_chng = 0
                pl_Y_chng = 0
    pl_X += pl_X_chng
    pl_Y += pl_Y_chng
    if pl_X <= 0:
        pl_X = 0
    elif pl_X >= 736:
        pl_X = 736
    if pl_Y <= 0:
        pl_Y = 0
    elif pl_Y >= 536:
        pl_Y = (536)
    player(pl_X, pl_Y)
    #enemy movement
    for i in range(6):    
        #player(en_X[i], en_Y[i], ene_img[i])
        enemy(en_X[i],en_Y[i])
        en_X[i] += en_X_chng[i]

        if en_X[i] <= 0:
            en_X_chng[i] = 1
            en_Y[i] += 20
        elif en_X[i] >= 736:
            en_X_chng[i] = -1
            en_Y[i] += 20
        #game over
        if en_Y[i] >= 420 or dist_bull_ene(en_X[i],en_Y[i],pl_X,pl_Y)<=50.0:
            for j in range(6):
                en_Y[j] = 2000
            pl_X,pl_Y = 2000,2000
            game_over_text()
            break

    #collision-detetcion
        if dist_bull_ene(bull_X, bull_Y, en_X[i], en_Y[i]) <= 30.0:
            bullet_sound = mixer.Sound("explosion.wav")
            bullet_sound.play()
            bull_X = pl_X
            bull_Y = pl_Y
            en_X[i] = random.randint(0,600)
            en_Y[i] = random.randint(25,100)
            score+=5
    # print(en_Y)
    
    # bullet Movement
    # to reset bullet co-ordinates
    if bull_Y <= 0:
        bull_Y = pl_Y
        bull_state = "Ready"

    if bull_state == "Fire":
        fire_bullet(bull_X, bull_Y)
        bull_Y -= bull_Y_chng
    show_score(textX,textY)
    pygame.display.update()  # updating screen
#print("Your score is : ",score)
