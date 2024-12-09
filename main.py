#IMPORTANT: some functions in this file are functions defined in npcStructure.py, so i suggest going there when first looking at this code
import pygame, sys
from npcStructure import *

pygame.init()

developerMode = True

base_width = 1440
base_height = 900

gameColors = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "grey": (54, 51, 50)}

for k, v in gameColors.items():
   gameColors[str(k)] = v

mac = False
if sys.platform == "darwin":
    mac = True

# The above code checks if the platform is Mac, as there are a few limitations that pygame has only for mac users.

usersDisplaySize = pygame.display.Info()






pygame.display.set_caption("Wherever Whenever!")




differentAspectRatio = False
if (usersDisplaySize.current_w / usersDisplaySize.current_h) != (1920/1080):
    differentAspectRatio = True

if differentAspectRatio == False:
    screen = pygame.display.set_mode((usersDisplaySize.current_w//2, usersDisplaySize.current_h//2), pygame.RESIZABLE)
elif differentAspectRatio == True:
    screen = pygame.display.set_mode((usersDisplaySize.current_w//2, ((usersDisplaySize.current_w//2)*0.5625)), pygame.RESIZABLE)

def scaleX(x):
    global screen
    width = screen.get_size()[0]
    height = screen.get_size()[1]
    # if window is wider than 16/9
    if (width/height) > (16/9):
        # too wide means we need vertical bezels
        # lets keep the height the same
        idealWidth = height * (16 / 9)
        totalBezelsWidth = width - idealWidth
        bezelWidth = totalBezelsWidth / 2

        # now we are going to imagine a graph. with x on the x axis, and the imaginary coordinates on the y axis. lets find the equation of this line
        # point 1 bezelWidth, imaginary Coordinate 0
        # point 2 (width-bezelWidth), imaginary coordinate 1920

        gradient = (1920)/((width-bezelWidth)-(bezelWidth))
        yIntercept = 0 - (gradient*bezelWidth)

        return int((gradient*x)+yIntercept)

    # if window is less wide than 16/9
    elif (width/height) <= (16/9):
        scale = 1920 / width
        return int(scale * x)
    
def unscaleX(x):
    global screen
    width = screen.get_size()[0]
    height = screen.get_size()[1]
    # if window is wider than 16/9
    if (width/height) > (16/9):
        # too wide means we need vertical bezels
        # lets keep the height the same
        idealWidth = height * (16 / 9)
        totalBezelsWidth = width - idealWidth
        bezelWidth = totalBezelsWidth / 2

        #now we are going to imagine a graph. with x on the x axis, and the imaginary coordinates on the y axis. lets find the equation of this line
        # point 1 bezelWidth, imaginary Coordinate 0
        # point 2 (width-bezelWidth), imaginary coordinate 1920

        gradient =((width-bezelWidth)-(bezelWidth))/(1920)
        yIntercept = bezelWidth - (gradient*0)

        return int((gradient*x)+yIntercept)

    # if window is less wide than 16/9
    elif (width/height) <= (16/9):
        scale = 1920 / width
        return int(x / scale)
    
def scaleY(y):
    global screen
    width = screen.get_size()[0]
    height = screen.get_size()[1]
    # if window is wider than 16/9 we want vertical bezels. vertical bezels affect x cord not y
    if (width/height) > (16/9):
        scale = 1080/height
        return int(y * scale)
    elif (width/height) <= (16/9):
        idealHeight = width * (9/16)
        totalBezelsHeight = height - idealHeight
        bezelHeight = totalBezelsHeight / 2

        # now we need to imagine a graph. x axis being a real y coordinates and y axis being the imaginary equivelent
        # we know that at these points:
        # point 1, bezelHeight, imaginary=0
        #point 2, (height-bezelHeight), imaginary=1080

        gradient = (1080)/((height-bezelHeight)-(bezelHeight))
        yIntercept = 0 - (gradient*bezelHeight)
        return int((gradient*y) + yIntercept)
    # if window is less wide than 16/9 we want horizontal bezels. horizontal bezels will affect the y cord but not x

def unscaleY(y):
    global screen
    width = screen.get_size()[0]
    height = screen.get_size()[1]
    
    if (width / height) > (16 / 9):
        # Inverse scaling for wider than 16:9
        scale = 1080 / height
        return int(y / scale)
    
    elif (width / height) <= (16 / 9):
        # Inverse linear transformation for 16:9 or narrower aspect ratio
        idealHeight = width * (9 / 16)
        totalBezelsHeight = height - idealHeight
        bezelHeight = totalBezelsHeight / 2

        gradient = 1080 / (height - 2 * bezelHeight)
        yIntercept = -gradient * bezelHeight

        # Reversing the formula: y = (output - yIntercept) / gradient
        return int((y - yIntercept) / gradient)
    
def unscaleWidth(width):
    point0 = unscaleX(0)
    pointX = unscaleX(width)
    return int(pointX-point0)

def unscaleHeight(height):
    point0 = unscaleY(0)
    pointY = unscaleY(height)
    return int(pointY-point0)

def displayConvo(screen, convo):
        img = pygame.image.load('chatbox.png')
        img = pygame.transform.scale(img, (unscaleWidth(1920), unscaleHeight(1080)))
        imgRect = img.get_rect()
        imgRect.topleft = (unscaleX(0), unscaleY(0))
        screen.blit(img, imgRect)
        print(convo.text)
        for response in convo.responses:
            print(response.responseText)
        if convo.name == 'start':
            return 'start2'
        elif convo.name == "start2":
            return ''
        
def talkToNPC(screen, npc):
    nextConvo = 'start'
    while nextConvo != '':
        convo = npc.getConversation(nextConvo)
        nextConvo = displayConvo(screen, convo)

def main():
    global screen
    global developerMode
    npcPrototype = False
    newNpcPrototype = False
    shapeTest = False
    fullscreen = False
    mainMenu = True
    startup = True
    closeWindow = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            screen.fill(gameColors["grey"])
            
            if event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                if mac == False and key=="f11":
                    fullscreen = not fullscreen  # Toggle state
                    if fullscreen:
                    # Enable fullscreen
                        oldWidth = screen.get_width()
                        oldHeight = screen.get_height()
                        pygame.display.quit()
                        pygame.display.set_caption("Wherever Whenever!")
                        pygame.display.init()
                        screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
                    else:
                        # Return to windowed mode
                        pygame.display.quit()
                        pygame.display.set_caption("Wherever Whenever!")
                        pygame.display.init()
                        screen = pygame.display.set_mode((oldWidth, oldHeight), pygame.RESIZABLE)
            
            
            # This tries to size the window correctly so black borders can be avoided
            if screen.get_size()[0] != usersDisplaySize.current_w:
                if screen.get_size()[0] / screen.get_size()[1] > (16/9) + 0.01 or screen.get_size()[0] / screen.get_size()[1] < (16/9) - 0.01:
                    pygame.display.set_mode((screen.get_size()[0], screen.get_size()[0]*0.5625), pygame.RESIZABLE)


            # THIS DRAWS BLACK BORDERS if user aaspect ratio is different
                #pygame.draw.rect(screen, gameColors["white"], pygame.Rect(unscaleX(0), unscaleY(0), unscaleX))
            if screen.get_size()[0]/screen.get_size()[1] > (16/9):
                pygame.draw.rect(screen, gameColors["black"], pygame.Rect(0,0, (unscaleX(0)-0), (screen.get_size()[1])))
                pygame.draw.rect(screen, gameColors["black"], pygame.Rect(unscaleX(1920),0, (unscaleX(0)-0), (screen.get_size()[1])))
            elif screen.get_size()[0]/screen.get_size()[1] < (16/9):
                pygame.draw.rect(screen, gameColors["black"], pygame.Rect(0,0, (screen.get_size()[0]), (unscaleY(0)-0)))
                pygame.draw.rect(screen, gameColors["black"], pygame.Rect(0,unscaleY(1080), (screen.get_size()[0]), (unscaleY(0)-0)))

            if mainMenu == True:
                mainMenuImg = pygame.image.load('mainmenu.png')
                mainMenuImg = pygame.transform.scale(mainMenuImg, (unscaleWidth(1920), unscaleHeight(1080)))
                mainMenuRect = mainMenuImg.get_rect()
                mainMenuRect.topleft = (unscaleX(0), unscaleY(0))
                screen.blit(mainMenuImg, mainMenuRect)
            #Draw vertical bezels yet
            if developerMode == True:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        print(f"{scaleX(pygame.mouse.get_pos()[0])}x{scaleY(pygame.mouse.get_pos()[1])}")
                    if event.type == pygame.KEYDOWN:
                        key = pygame.key.name(event.key)
                        if developerMode == True:
                            if key == "n":
                                npcPrototype = True
                            if key == "s":
                                shapeTest = True
                            if key == "d": #dialouge test
                                newNpcPrototype = True
                                
                    if shapeTest == True:
                        pygame.draw.rect(screen, gameColors["red"], pygame.Rect(unscaleX(0), unscaleY(0), unscaleWidth(60), unscaleHeight(60)))
                        
                    if npcPrototype == True:
                        img = pygame.image.load('npcchatbox.png')
                        img = pygame.transform.scale(img, (unscaleWidth(1920), unscaleHeight(1080)))
                        imgRect = img.get_rect()
                        imgRect.topleft = (unscaleX(0), unscaleY(0))
                        screen.blit(img, imgRect)
                        font = pygame.font.SysFont("Arial", int(unscaleHeight(81)))
                        npcName = font.render('Natalia M', True, gameColors["white"])
                        screen.blit(npcName, (unscaleX(546), unscaleY(690)))

                    if newNpcPrototype == True:
                        NPCData = NPC.fetchNpcData()
                        for npcIndividual in NPCData:
                            if npcIndividual.name == "Natalia M":
                                natalia = npcIndividual
                        talkToNPC(screen, natalia)

            pygame.display.flip()


main()
