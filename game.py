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
enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()

def create_skeleton():
    skeleton = object.Skeleton(600, 300, skeletonTextures)
    enemies.add(skeleton)
    return skeleton

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.parry()
            if event.key == pygame.K_d:
                create_skeleton()
    player.update()
    for skeleton in enemies:
        skeleton.update()
        if pygame.time.get_ticks() - skeleton.lastShot > 1500:
            projectiles.add(skeleton.shoot(player,pygame.image.load("assets/GreenBlast.png").convert_alpha()))
            skeleton.lastShot = pygame.time.get_ticks()
    hits = pygame.sprite.spritecollide(player,projectiles,False)
    if hits:
        for projectile in hits:
            if projectile is None:
                pass
            if player.parryTime == 0:
                player.damage()
                projectiles.remove(pygame.sprite.spritecollideany(player, projectiles))
            else:
                projectile.direction.x = projectile.direction.x * -1
                projectile.direction.y = projectile.direction.y * -1
                projectile.striker = 1
    enemyHits = pygame.sprite.groupcollide(enemies, projectiles, False, False)
    if enemyHits:
        for skeleton, projectile_hits in enemyHits.items():
            for projectile in projectile_hits:
                if projectile.striker == 1:
                    enemies.remove(skeleton)
                    projectiles.remove(projectile)
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("gray")

    # RENDER YOUR GAME HERE
    for trail in player.dash_trails:
        screen.blit(trail.image, trail.rect)
    for skeleton in enemies:
        screen.blit(skeleton.image, skeleton.rect)
    for projectile in projectiles:
        projectile.update()
        screen.blit(projectile.image, projectile.rect)
    screen.blit(player.image, player.rect)
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()