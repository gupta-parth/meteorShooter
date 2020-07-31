'''
Meteor Shooter by Parth Gupta 
Video Game
'''

print ("Use WASD to move and spacebar to shoot lasers, hit enemies and gain points. Don't forget to dodge the meteors!")

#import modules 
import pygame.mixer
import random
from pygame.locals import *
pygame.font.init()
pygame.init()

#for fps management 
clock = pygame.time.Clock()
FPS = 60

#screen setup
screenWidth = 800
screenHeight = 800
screen = pygame.display.set_mode((screenWidth,screenHeight))

#player ship
red_player_start = pygame.image.load('playerShip1_red.png')
red_player = pygame.transform.scale(red_player_start, (85,60))
red_player_laser = pygame.image.load('laserRed03.png')
player_laser_width, player_laser_height = red_player_laser.get_size()
playerWidth, playerHeight = red_player.get_size()


#enemy ship
start_enemy_ship = pygame.image.load('enemyBlue1.png')
enemy_ship = pygame.transform.scale(start_enemy_ship, (60, 60))
enemy_laser = pygame.image.load('laserBlue06.png')
enemy_laser_width, enemy_laser_height = enemy_laser.get_size()
enemyWidth = 60
enemyHeight = 60

#meteor, this is done so that I can get the width and the height of the meteor by using the get size function. 
start_meteor = pygame.image.load('meteorBrown_med1.png')
meteor = pygame.transform.scale(start_meteor, (70,70))
meteor_width, meteor_height = meteor.get_size()

#font
font = pygame.font.SysFont('timesnewroman', 25, True, False)
font2 = pygame.font.SysFont('timesnewroman', 80, True, False)

#colours
black = (0, 0, 0)
white = (255, 255, 255)

#varibles
score = 0
lives = 3
time = 0

#sounds
laserSound = pygame.mixer.Sound('laser.wav')
laserSound.set_volume(0.01)
blastSound = pygame.mixer.Sound('blast.wav')
blastSound.set_volume(0.1)

#laser class
class Laser:
    def __init__(self, x, y, picture): #initialization
        self.x = x 
        self.y = y
        self.picture = picture #type of laser 
    
    def draw(self, screen):
        screen.blit (self.picture, (self.x, self.y))
    
    def move(self, speed):
        self.y += speed


class Ship:   #super class 
    '''
    this is done to reduce the work that I have to put in to create enemy and player spaceships
    the subclasses enemy and player will inherit attributes and methods from this class and change them if needed
    '''
    
    timer = 60 #half a second timer since the program runs at 60 frames
    
    def __init__ (self, x, y, health = 100):
        self.x = x 
        self.y = y
        self.health = health
        self.alive = False 
        self.laserImage = None
        self.laser_list = [] #laser list to keep track of all the lasers that the ship is spawning
        self.shipImage = None 
        self.laserTimer = 0 #cool down timer for the laser to prevent spamming 
    
    def draw(self, screen):
        screen.blit(self.shipImage, (self.x, self.y))
        for laser in self.laser_list: #go through the laser list and draw all the lasers 
            laser.draw(screen)
            
    def laser_move(self, speed):
        self.laser_timer() #increment the timer 
        for laser in self.laser_list:
            laser.move(speed)
            if laser.y > screenHeight or laser.y < 0: #if the laser if off the screen
                self.laser_list.pop(self.laser_list.index(laser)) #remove it from the laser list 
        
        
    def laser_timer(self):
        if self.laserTimer >= self.timer: #if the laser timer is more than 60
            self.laserTimer = 0 #reset
        elif self.laserTimer > 0: #if it is more than 0
            self.laserTimer += 1 #increment it 
        
    def shoot(self): #shoot the laser 
        if self.laserTimer == 0: #only shoot if its 0
            laser = Laser(self.x + (playerWidth/2), self.y, self.laserImage) #make the laser 
            self.laser_list.append(laser) #add it to the list 
            self.laserTimer = 1 #start the timer 
            
            
class Player(Ship): #class for the player
    def __init__ (self, x, y, health = 100): #default health is 100
        super().__init__(x, y, health) #gets the attributes from the super class
        self.shipImage = red_player #use the red player image for the ship
        self.laserImage = red_player_laser
        self.total_health = health
        self.alive = True 
        

class Enemy(Ship):
    timer = 30 #  1 second for enemies, overwrites the timer varible of the superclass
    
    def __init__ (self, x, y, health = 10):
        super().__init__(x,y, health)
        self.shipImage = enemy_ship
        self.laserImage = enemy_laser
        self.total_health = health 
    
    def move(self, speed):
        self.y += speed #add to the y coordinate to move the object 


class Meteor: #set up meteor class 
    start_meteor = pygame.image.load('meteorBrown_big1.png')
    meteor = pygame.transform.scale(start_meteor, (70,70))
      
    def __init__ (self, x, y):
        self. x = x
        self.y = y 
        self.alive = False 
    
    def move(self, speed):
        self.y += speed
    
    def draw(self, screen):
        screen.blit(self.meteor, (self.x, self.y))
        

class Star: #set up star class 
    def __init__(self, x, y, colour):
        self.x = x
        self.y = y 
        self.colour = colour
        self.star_vel = 1 #speed for the stars 
    
    def move(self):
        self.y += self.star_vel
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, (self.x, self.y), 0) #draw pixel circle stars 

    
def redrawGameScreen(): #drawing the screen function
    screen.fill(black) #fill in a black background 
    for star in stars: #draw all the stars in the stars list 
        star.draw(screen)
        
    for enemy in enemies_max: #go through the enemy list 
        if enemy.alive: #if they are alive 
            enemy.draw(screen) #draw them 
    
    for meteor in meteors: #go through the meteor list 
        if meteor.alive: #if they are alive 
            meteor.draw(screen) #draw them 
    
    player.draw(screen) #draw the player 
    text = font.render('Score: ' + str(score), False, white) #draw texts 
    screen.blit(text, (0, 0))
    text2 = font.render('Lives: ' + str(lives), False, white)
    screen.blit(text2, (700, 0))
    text3 = font.render('Health: ' + str(player.health), False, white)
    screen.blit(text3, (670,30))
    pygame.display.flip() #flip everything on the screen


def quitGame():
    screen.fill(black)
    gameOver = font2.render('Game Over!', False, white)
    screen.blit(gameOver, (200, 350))
    pygame.display.flip()
    pygame.time.delay(1000) #give some time for the player to read the message
    pygame.quit()

player = Player(300, 700) #create player 
player_speed = 5 #player movement speed
player_laser_speed = -5 #laser speed is negative because the lasers are going up 

#enemy list and variables 
enemies_max = []
enemy_speed = 2
enemy_laser_speed = 6

#meteor list and variables
meteors = []
meteor_speed = 2

wave_length = 2

stars = [] #create background stars 
for i in range(30):
    star = Star(random.randrange(0, screenWidth), random.randrange(-900, -100), white)
    stars.append(star) #add it to the list 

gameOn = True #game flag 
while gameOn:
    clock.tick(FPS) #runs the program at 60 fps
    time += 1
    if time == 600: #if 10 seconds have passed 
        wave_length += 1 #add more enemies and meteors
        time = 0 #reset 
    
    if len(enemies_max) == 0: #if there are no enemies 
        for i in range(wave_length):
            enemy = Enemy(random.randrange(0, screenWidth - enemyWidth), random.randrange(-2000, -700)) #create enemeies
            enemy.alive = True 
            enemies_max.append(enemy) #add them to the list 
            
    if len(meteors) == 0: #if there are no meteors 
        for i in range(wave_length):
            meteor = Meteor(random.randrange(0, screenWidth), random.randrange(-1000, -100)) #create meteors 
            meteor.alive = True 
            meteors.append(meteor) #add them to the list 
            
    if player.health == 0: #if player health is 0
        if lives > 0: #if lives is greate than 0
            lives -= 1 #subtract 1
            player.health = 100 #adjust the health 
    if lives == 0 and player.health == 0: #if there are no lives remaining and the health is 0
        quitGame() #call the quitGame function
  
    for event in pygame.event.get(): #get all the events happening 
        if event.type == QUIT: 
            gameOn = False #set the game flag to false if user wants to quit 
    
    keys = pygame.key.get_pressed() #get all the keys pressed by the user 
    
    #if statements are used so that the player can move diagonally as well
    if keys[K_w] and player.y - player_speed > 0:
        player.y -= player_speed
    if keys[K_a] and player.x - player_speed > 0:
        player.x -= player_speed 
    if keys[K_d] and player.x + player_speed + playerWidth < screenWidth: #contains the player in the window
        player.x += player_speed 
    if keys[K_s] and player.y + player_speed + playerHeight < screenHeight:
        player.y += player_speed 
    if keys[K_SPACE]:
        player.shoot() #shoot the laser 
        laserSound.play() #play the sound
    player.laser_move(player_laser_speed) #move the laser 
        
    for laser in player.laser_list: #go through all the lasers in the player laser list
        for enemy in enemies_max: #go through all the enemies 
            if laser.x + player_laser_width > enemy.x and laser.x < enemy.x + enemyWidth and laser.y < enemy.y + enemyHeight and laser.y + player_laser_height > enemy.y: #if hitbox occurs 
                score += 10 #add to the score 
                blastSound.play() #play the blast sound 
                enemies_max.pop(enemies_max.index(enemy)) #remove the enemy 
                player.laser_list.pop(player.laser_list.index(laser)) #remove the laser 
    
    
    for enemy in enemies_max: #go through all the enemies 
        enemy.shoot() #shoot the laser 
        enemy.laser_move(enemy_laser_speed)#move the laser 
        enemy.move(enemy_speed) #move the enemy 
        if enemy.y > screenHeight: #remvoe the enemy if it goes offscreen
            enemies_max.pop(enemies_max.index(enemy))              
        for laser in enemy.laser_list: #go through all the enemy lasers 
            if laser.x + enemy_laser_width > player.x and laser.x < player.x + playerWidth and laser.y + enemy_laser_height > player.y and laser.y < player.y + playerHeight: #if it hits the player 
                if player.health >= 10: #if the player health is greater or equal to 10
                    player.health -= 10 #reduce the health 
                    enemy.laser_list.pop(enemy.laser_list.index(laser)) #remove the laser 
                
    
    for meteor in meteors: #go through all the meteors 
        meteor.move(meteor_speed) #move them 
        if meteor.x + meteor_width > player.x and meteor.x < player.x + playerWidth and meteor.y + meteor_height > player.y and meteor.y < player.y + playerHeight: #if the meteor hits the player 
            if player.health >= 20: #if the player health is greater than or equal to 20 
                player.health -= 20 #reduce the health
                meteors.pop(meteors.index(meteor)) #remove the meteor 
                
            elif player.health < 20: #otherwise if the health is less than 20
                if lives > 0: #if lives is greater than 0
                    lives -= 1 #decrement the lives 
                    player.health = 100 #adjust the health 
                    meteors.pop(meteors.index(meteor)) #remove the meteor 
        if meteor.y > screenHeight: #if meteor goes offscreen
            meteors.pop(meteors.index(meteor)) #remove the meteor 
        
        
    
    for star in stars: #go through all the stars 
        star.move() #move them 
        if star.y == screenHeight: #if it reaches the end 
            star.x = random.randrange(0, screenWidth - 6) #set new coordinates 
            star.y = 0 #set at the top of the screen
    
    redrawGameScreen() #draw everything on the window     
            
            
pygame.quit() #quit the game 
