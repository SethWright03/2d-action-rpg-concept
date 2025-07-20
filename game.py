import pygame
import object

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
player = object.Player(100, 100)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    player.update()

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("gray")

    # RENDER YOUR GAME HERE
    for trail in player.dash_trails:
        screen.blit(trail.image, trail.rect)
    screen.blit(player.image, player.rect)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()