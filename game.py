import pygame
import object

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
# texture loading
skeletonTextures = {
    "skelClosed": pygame.image.load("assets/SkeleClosed.png").convert_alpha(),
    "skelOpen": pygame.image.load("assets/SkeleOpen.png").convert_alpha(),
}
#object initialization
player = object.Player(100, 100)
testSkeleton = object.Skeleton(200, 200,skeletonTextures)
projectiles = pygame.sprite.Group()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    player.update()
    testSkeleton.update()
    if pygame.time.get_ticks() - testSkeleton.lastShot > 1500:
        projectiles.add(testSkeleton.shoot(player,pygame.image.load("assets/GreenBlast.png").convert_alpha()))
        testSkeleton.lastShot = pygame.time.get_ticks()
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("gray")

    # RENDER YOUR GAME HERE
    for trail in player.dash_trails:
        screen.blit(trail.image, trail.rect)
    screen.blit(testSkeleton.image, testSkeleton.rect)
    for projectile in projectiles:
        projectile.update()
        screen.blit(projectile.image, projectile.rect)
    screen.blit(player.image, player.rect)
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()