import pygame, sys

pygame.init()

developerMode = True

gameColors = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "white": (255, 255, 255),
    "black": (0, 0, 0)}

for k, v in gameColors.items():
   gameColors[str(k)] = v

mac = False
if sys.platform == "darwin":
    mac = True

# The above code checks if the platform is Mac, as there are a few limitations that pygame has only for mac users.

usersDisplaySize = pygame.display.Info()

pygame.display.set_caption("Wherever Whenever!")


notMacFullscreen = False

if developerMode == True:
    print(f"Your Display DimensionsL {usersDisplaySize.current_w}x{usersDisplaySize.current_h}")

if mac == True:
    screen = pygame.display.set_mode((usersDisplaySize.current_w//2, usersDisplaySize.current_h//2), pygame.RESIZABLE)
    font = pygame.font.SysFont("Arial", 36)
    macMessage = font.render("Mac users must press fullscreen!", True, gameColors["red"])
    print(macMessage.get_width())
    screen.blit(macMessage, (((usersDisplaySize.current_w//2)-macMessage.get_width())//2,((usersDisplaySize.current_h//2)-macMessage.get_height())//2))
    pygame.display.update()
    notMacFullscreen = True
        
elif mac == False:
    screen = pygame.display.set_mode((usersDisplaySize.current_w, usersDisplaySize.current_h), pygame.NOFRAME)


closeWindow = False
while closeWindow == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            closeWindow = True
        if mac == False or notMacFullscreen == False:
            if developerMode == True:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos() #dont ask me why but for this function it doesn't need event.mouse to be inside the brackets, you'll get an error if you try
                    print(str(pos[0]) + ", " + str(pos[1]))
        elif notMacFullscreen == True:
            if pygame.display.get_window_size() == (usersDisplaySize.current_w, usersDisplaySize.current_h):
                notMacFullscreen = False
                screen.fill(gameColors["black"])
                print("Screen Filled")

        pygame.display.update()


pygame.quit()
sys.exit()