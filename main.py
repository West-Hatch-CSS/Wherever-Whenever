import pygame, sys

pygame.init()

developerMode = True
npcPrototype = False
shapeTest = False

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



def scaleX(input_x):
    base_width = 1920
    global screen
    usersDisplaySize = screen.get_size()[0]
    scale = usersDisplaySize/base_width
    return int(input_x // scale)


def unscaleX(input_x):
    base_width = 1920
    global screen
    usersDisplaySize = screen.get_size()[0]
    return input_x * (usersDisplaySize/base_width)

def unscaleWidth(input_x):
    point0 = unscaleX(0)
    pointX = unscaleX(input_x)
    return pointX - point0

def scaleY(input_y):
    global screen
    width = screen.get_size()[0]
    height = screen.get_size()[1]

    realBezelsHeight = height - (width/(16/9))

    gradient = (1080)/((height - (realBezelsHeight/2))-realBezelsHeight/2)
    yIntercept = 0 - (gradient * (realBezelsHeight/2))
    return int((gradient*input_y)+yIntercept)




def unscaleY(transformed_y):
    global screen
    width = screen.get_size()[0]
    height = screen.get_size()[1]

    realBezelsHeight = height - (width / (16 / 9))
    gradient = 1080 / ((height - (realBezelsHeight / 2)) - realBezelsHeight / 2)
    yIntercept = 0 - (gradient * (realBezelsHeight / 2))

    # Reverse the transformation to get the original input_y
    input_y = (transformed_y - yIntercept) / gradient
    return input_y
    

def unscaleHeight(input_x):
    point0 = unscaleY(0)
    pointX = unscaleY(input_x)
    return pointX - point0

pygame.display.set_caption("Wherever Whenever!")


if developerMode == True:
    print(f"Your Display DimensionsL {usersDisplaySize.current_w}x{usersDisplaySize.current_h}")

differentAspectRatio = False
if (usersDisplaySize.current_w / usersDisplaySize.current_h) != (1920/1080):
    differentAspectRatio = True
    print("Your display has an unsusual aspect ratio. In order to prevent weird scaling, parts of the screen will be black")

if differentAspectRatio == False:
    screen = pygame.display.set_mode((usersDisplaySize.current_w//2, usersDisplaySize.current_h//2), pygame.RESIZABLE)
elif differentAspectRatio == True:
    screen = pygame.display.set_mode((usersDisplaySize.current_w//2, ((usersDisplaySize.current_w//2)*0.5625)), pygame.RESIZABLE)


startup = True
closeWindow = False
while closeWindow == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            closeWindow = True
        
        screen.fill(gameColors["grey"])

        if event.type == pygame.VIDEORESIZE or startup == True:
            if (screen.get_size()[0], screen.get_size()[1]) != (usersDisplaySize.current_w, usersDisplaySize.current_h): #if the game isnt fullscreen
                if screen.get_size()[0]/screen.get_size()[1] < (16/9-0.01) or screen.get_size()[0]/screen.get_size()[1] > (16/9+0.01):
                    screen = pygame.display.set_mode((screen.get_size()[0], (screen.get_size()[0]*0.5625)), pygame.RESIZABLE)
                    print(screen.get_size()[0], (screen.get_size()[0]*0.5625))
                    print(screen.get_size()[0], (screen.get_size()[1]))
                
            startup = False


        if differentAspectRatio == True:
            #we need to find the bottm right coord of the top bezel

            topBezelHeight = unscaleY(0) # unlike unscaleX(0), it is not in te exact corner of a window
            topBezelWidth = unscaleWidth(1920)

            pygame.draw.rect(screen, gameColors["black"], pygame.Rect(0, 0, topBezelWidth, topBezelHeight))
            
            topLeftCornerY = unscaleY(1080)
            # as its on the very left it has to be 0
            pygame.draw.rect(screen, gameColors["black"], pygame.Rect(0, topLeftCornerY, topBezelWidth, topBezelHeight))



            #pygame.draw.rect(screen, gameColors["white"], pygame.Rect(unscaleX(0), unscaleY(0), unscaleX))

        if developerMode == True:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos() #dont ask me why but for this function it doesn't need event.mouse to be inside the brackets, you'll get an error if you try
                    print(str(pos[0]) + ", " + str(pos[1]))
                    print(f"Scaled: {scaleX(pos[0])}, {scaleY(pos[1])}")
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.name(event.key)
                    if developerMode == True:
                        if key == "n":
                            npcPrototype = True
                        if key == "s":
                            shapeTest = True
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

        pygame.display.update()


pygame.quit()
sys.exit()