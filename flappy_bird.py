import random # to generate random numbers
import sys # inorder to use sys.exit to exit the program
import pygame
from pygame.locals import *
import math

#global variables for the game
fps = 32 #frames per second
screenwidth = 300
screenheight = 511
screen = pygame.display.set_mode((screenwidth,screenheight))
groundy = screenheight * 0.93
game_sprites = {} #to store images
game_sounds = {}
PLAYER = "pictures/ply5.png"
BACKGROUND = "pictures/bga.png"
PIPE = "pictures/pipe4.png"

def welcomeScreen():
    "' shows welcome page of the screen'"
    playerx = int(screenwidth/5)
    playery = int((screenheight - game_sprites["player"].get_height())/2)
    messagex = int((screenwidth - game_sprites["player"].get_width())/80)
    messagey = int(screenheight*0.13)
    basex = 0

    while True:
        for event in pygame.event.get():
            #to close the program
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            #to start the game
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP) :
                return
            else:
                screen.blit(game_sprites["background"],(0,0))
                # screen.blit(game_sprites["player"],(playerx,playery))
                screen.blit(game_sprites["message"],(messagex,messagey))
                screen.blit(game_sprites["base"],(basex,groundy))
                pygame.display.update()
                fpsclock.tick(fps)

def mainGame():
    score = 0
    playerx = int(screenwidth/5)
    playery = int(screenheight/2)
    basex = 0

    #create 2 pipes to blit on the screen 
    newpipe1 = getRandomPipe()
    newpipe2 = getRandomPipe()

    # my list for upper pipes
    upperPipes=[
        {"x" : screenwidth+200 , "y" : newpipe1[0]["y"]},
        {"x" : screenwidth+200+(screenwidth/2) , "y" : newpipe2[0]["y"]},
    ]
    # my list for lower pipes
    lowerPipes=[
        {"x" : screenwidth+200 , "y" : newpipe1[1]["y"]},
        {"x" : screenwidth+200+(screenwidth/2) , "y" : newpipe2[1]["y"]},
    ]
    #for speed
    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1
    playerFlapAccV = -8 #velocity of bird while flapping
    playerFlapped = False #only true when bird is flapping

    while True : #game loop
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN  and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP) :
                if playery > 0 :
                    playerVelY = playerFlapAccV
                    playerFlapped = True
                    game_sounds["wing"].play()
        crashTest = isCollide(playerx,playery,upperPipes,lowerPipes) #returns True when the player is crashed 
        if crashTest:
            return
        #check for score
        playerMidPos = playerx + game_sprites["player"].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe["x"] +game_sprites["pipe"][0].get_width()/2
            if pipeMidPos <=playerMidPos < pipeMidPos +4:
                score += 1
                print(f"Your score is {score}")
                game_sounds["point"].play()
        
        if playerVelY < playerMaxVelY and not playerFlapped :
            playerVelY += playerAccY
        if playerFlapped :
            playerFlapped = False
        playerHeight = game_sprites["player"].get_height()
        playery = playery + min(playerVelY , groundy - playery - playerHeight)

        # move pipes to the left
        for upperPipe, lowerPipe in zip(upperPipes , lowerPipes) :
            upperPipe["x"] += pipeVelX
            lowerPipe["x"] += pipeVelX


        if  0 < upperPipes[0]["x"] < 5 or 0 < upperPipes[1]["x"] < 5 :
            newpipe = getRandomPipe()
            print("a",len(upperPipes))
            upperPipes.append(newpipe[0])
            print("b",len(upperPipes))
            lowerPipes.append(newpipe[1])


        
        
        # if the pipe is out of screen remove it  
        if  upperPipes[0]["x"] < -game_sprites["pipe"][0].get_width():
            
            upperPipes.pop(0)
            lowerPipes.pop(0)

        #let's blit our sprites now
        screen.blit(game_sprites["background"],(0,0))

        for upperPipe, lowerPipe in zip(upperPipes , lowerPipes) :
            screen.blit(game_sprites["pipe"][0] , (upperPipe["x"],upperPipe["y"]))
            screen.blit(game_sprites["pipe"][1] , (lowerPipe["x"],lowerPipe["y"]))
        screen.blit(game_sprites["base"],(basex,groundy))
        screen.blit(game_sprites["player"],(playerx,playery))

        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += game_sprites["numbers"][digit].get_width()
        Xoffset = (screenwidth - width)/2
        for digit in myDigits:
            screen.blit(game_sprites["numbers"][digit],(Xoffset , screenheight*0.12))
            Xoffset += game_sprites["numbers"][digit].get_width()
        pygame.display.update()
        fpsclock.tick(fps)
def getRandomPipe():
    "'generate position for two pipes '"
    pipeHeight = game_sprites["pipe"][0].get_height()
    offset = screenheight/3
    y2 = offset + random.randrange(0,int(screenheight - game_sprites["base"].get_height() - 1.2 *offset))
    pipeX = screenwidth + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {"x":pipeX,"y": -y1} #upper pipe
        , {"x": pipeX,"y": y2} #lower pipe x remains same for both

    ]
    return pipe

#updated collision but the problem is that i couldnt resolvew the distance issue because the distance of pipes is assigned by you so i hope you would adjust that accordignly.


def isCollide(playerx, playery, upperPipes, lowerPipes):
    playerHeight = game_sprites["player"].get_height()
    playerWidth = game_sprites["player"].get_width()
    
    # Ground collision
    if playery + playerHeight >= groundy:
        game_sounds["hit"].play()
        return True

    # Distance-based pipe collision detection
    for pipe in upperPipes + lowerPipes:
        pipe_center_x = pipe['x'] + game_sprites['pipe'][0].get_width() / 2
        pipe_center_y = pipe['y'] + game_sprites['pipe'][0].get_height() / 2
        distance = math.sqrt((playerx + playerWidth / 2 - pipe_center_x) ** 2 + (playery + playerHeight / 2 - pipe_center_y) ** 2)
        
        # Adjusting the collision distance threshold
##        collision_distance = (playerWidth / 2) + (game_sprites['pipe'][0].get_width() / 2)  # Subtract a small value for better accuracy
##        print(collision_distance)
        if distance < 130:
            game_sounds['hit'].play()
            return True

    return False


if __name__ == "__main__":
    #game starts from here
    pygame.init()
    fpsclock = pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird: The Great Escape")
    # Assuming all digits should be 24x36 pixels
    game_sprites["numbers"] = [
    pygame.transform.scale(pygame.image.load(f"pictures/bb{i}.png").convert_alpha(), (24, 36))
    for i in range(10)]

    game_sprites["message"] = pygame.image.load("pictures/intro.png").convert_alpha()
    game_sprites["base"] = pygame.image.load("pictures/floor.png").convert_alpha()
    game_sprites["pipe"] = (pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180) ,
                            pygame.image.load(PIPE).convert_alpha() ) #for both pipes up and down
    #game sounds
    game_sounds["die"] = pygame.mixer.Sound("music/sfx_die.wav")
    game_sounds["hit"] = pygame.mixer.Sound("music/sfx_hit.wav")
    game_sounds["point"] = pygame.mixer.Sound("music/sfx_point.wav")
    game_sounds["swoosh"] = pygame.mixer.Sound("music/sfx_swooshing.wav")
    game_sounds["wing"] = pygame.mixer.Sound("music/sfx_wing.wav")

    game_sprites["background"] = pygame.image.load(BACKGROUND).convert()
    game_sprites["player"] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen() #shows screeen till user presses a button or tap anything
        mainGame() #main game function

    
