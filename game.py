import pygame
import levels
import object
import random

score = 0

skeletonCollides = 0

# pygame setup
pygame.init()
pygame.font.init()
font = pygame.font.SysFont("Comic Sans MS", 30)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
# texture loading
skeletonTextures = {
    "skelClosed": pygame.image.load("assets/SkeleClosed.png").convert_alpha(),
    "skelOpen": pygame.image.load("assets/SkeleOpen.png").convert_alpha(),
}
#setup score display
scoreText = font.render(f"Score: {score}", True, "black")
scoreDisplay = pygame.Surface((200, 50),pygame.SRCALPHA)
scoreDisplay.fill((0, 0, 0, 0))
scoreDisplay.blit(scoreText, (0, 0))
def update_score():
    scoreText = font.render(f"Score: {score}", True, "black")
    scoreDisplay.fill((0, 0, 0, 0))
    scoreDisplay.blit(scoreText, (0, 0))

#object initialization
player = object.Player(100, 100)
enemies = pygame.sprite.Group()
walls, spawners = levels.genLevel(levels.introLayout)
projectiles = pygame.sprite.Group()

def create_skeleton():
    skeleton = object.Skeleton(600, 300, skeletonTextures)
    enemies.add(skeleton)
    return skeleton

def cameraFollow(player):
    cameraX = player.rect.centerx - screen.get_width() // 2
    cameraY = player.rect.centery - screen.get_height() // 2
    return cameraX, cameraY

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.parry()
            if event.key == pygame.K_d:
                create_skeleton()
    if 0 > score:
        running = False
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
                score -= 1
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
                    score += 1
    wallHits = pygame.sprite.spritecollide(player, walls, False)
    if wallHits:
        player.undoMove()
    wallBlasts = pygame.sprite.groupcollide(walls, projectiles, False, True)

    # random spawn logic
    for spawner in spawners:
        if random.randint(0, 6000) < 12:
            for skeleton in enemies:
                if skeleton.rect.colliderect(spawner.rect):
                    skeletonCollides += 1
            if skeletonCollides == 0:
                newSkeleton = object.Skeleton(spawner.rect.x, spawner.rect.y, skeletonTextures)
                enemies.add(newSkeleton)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("gray")

    # RENDER YOUR GAME HERE
    cameraX, cameraY = cameraFollow(player)
    for trail in player.dash_trails:
        screen.blit(trail.image, (trail.rect.x - cameraX, trail.rect.y - cameraY))
    for skeleton in enemies:
        screen.blit(skeleton.image, (skeleton.rect.x - cameraX, skeleton.rect.y - cameraY))
    for projectile in projectiles:
        projectile.update()
        screen.blit(projectile.image, (projectile.rect.x - cameraX, projectile.rect.y - cameraY))
    for wall in walls:
        screen.blit(wall.image, (wall.rect.x - cameraX, wall.rect.y - cameraY))
    screen.blit(player.image, (player.rect.x - cameraX, player.rect.y - cameraY))
    update_score()
    screen.blit(scoreDisplay, (10, 10))
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()