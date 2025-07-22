import pygame

class Player(pygame.sprite.Sprite):
    baseSpeed = 8
    diagSpeed = baseSpeed * 0.7071
    dashCooldown = 0

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill("blue")
        self.rect = self.image.get_rect(topleft=(x, y))
        self.moveSpeed = self.baseSpeed
        self.dashing = False
        self.dash_trails = pygame.sprite.Group()
        self.dash_duration = 250  # ms
        self.dash_speed = 32
        self.dash_start_time = 0
        self.dash_direction = pygame.Vector2(0, 0)
        self.hurtTime = 100
        self.parryTime = 0
    def dash(self, direction):
        self.dashing = True
        self.dash_start_time = pygame.time.get_ticks()
        self.last_trail_time = 0
        self.dashCooldown = self.dash_start_time + 500
        if direction == "up":
            self.dash_direction = pygame.Vector2(0, -1)
        elif direction == "down":
            self.dash_direction = pygame.Vector2(0, 1)
        elif direction == "left":
            self.dash_direction = pygame.Vector2(-1, 0)
        elif direction == "right":
            self.dash_direction = pygame.Vector2(1, 0)
        elif direction == "up-left":
            self.dash_direction = pygame.Vector2(-1, -1).normalize()
        elif direction == "up-right":
            self.dash_direction = pygame.Vector2(1, -1).normalize()
        elif direction == "down-left":
            self.dash_direction = pygame.Vector2(-1, 1).normalize()
        elif direction == "down-right":
            self.dash_direction = pygame.Vector2(1, 1).normalize()
    def update(self):
        # handling wall collision in case i need to undo
        self.startingposX = self.rect.x
        self.startingposY = self.rect.y
        keys = pygame.key.get_pressed()
        mods = pygame.key.get_mods()
        # Dash logic
        if self.dashing:
            now = pygame.time.get_ticks()
            if now - self.dash_start_time > self.dash_duration:
                self.dashing = False
                self.dash_direction = pygame.Vector2(0, 0)
            else:
                self.rect.x += self.dash_direction.x * self.dash_speed
                self.rect.y += self.dash_direction.y * self.dash_speed
                if now - self.last_trail_time > 25:  # create the trail block
                    trail = DashTrail(self.rect.x + 5, self.rect.y + 5)
                    self.dash_trails.add(trail)
                    self.last_trail_time = now
                for trail in self.dash_trails:
                    trail.update()
                return  # no moving during dash
        for trail in self.dash_trails:
            trail.update()
        # move
        vertPressed = keys[pygame.K_UP] or keys[pygame.K_DOWN]
        horizPressed = keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]
        if vertPressed and horizPressed:
            self.moveSpeed = self.diagSpeed
        else:
            self.moveSpeed = self.baseSpeed
        if mods & pygame.KMOD_SHIFT and self.dashCooldown < pygame.time.get_ticks():
            if keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
                if keys[pygame.K_LEFT]:
                    self.dash("up-left")
                elif keys[pygame.K_RIGHT]:
                    self.dash("up-right")
                else:
                    self.dash("up")
            elif keys[pygame.K_DOWN] and not keys[pygame.K_UP]:
                if keys[pygame.K_LEFT]:
                    self.dash("down-left")
                elif keys[pygame.K_RIGHT]:
                    self.dash("down-right")
                else:
                    self.dash("down")
            elif keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
                self.dash("left")
            elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
                self.dash("right")
        if keys[pygame.K_UP]:
            self.rect.y -= self.moveSpeed
        elif keys[pygame.K_DOWN]:
            self.rect.y += self.moveSpeed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.moveSpeed
        elif keys[pygame.K_RIGHT]:
            self.rect.x += self.moveSpeed
        if pygame.time.get_ticks() - self.hurtTime < 100:
            self.image.fill("red")
        elif self.parryTime > 0:
            self.image.fill("yellow")
            self.parryTime -= 1
        else:
            self.image.fill("blue")
    def damage(self):
        self.hurtTime = pygame.time.get_ticks()
    def parry(self):
        self.parryTime = 15
    def undoMove(self):
        self.rect.x = self.startingposX
        self.rect.y = self.startingposY
        self.dashing = False
        self.dash_direction = pygame.Vector2(0, 0)

class skeleSpawner(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50,50))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.skeletonCollides = 0

class DashTrail(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill("white")
        self.rect = self.image.get_rect(topleft=(x, y))
        self.lifetime = 250
        self.creation_time = pygame.time.get_ticks()
    def update(self):
        if pygame.time.get_ticks() - self.creation_time > self.lifetime:
            self.kill()
        elif pygame.time.get_ticks() - self.creation_time > self.lifetime * 0.75:
            self.image.set_alpha(64)
        elif pygame.time.get_ticks() - self.creation_time > self.lifetime * 0.5:
            self.image.set_alpha(128)
        elif pygame.time.get_ticks() - self.creation_time > self.lifetime * 0.25:
            self.image.set_alpha(192)

class Skeleton(pygame.sprite.Sprite):
    def __init__(self, x, y, textures):
        super().__init__()
        self.textures = textures
        self.image = self.textures["skelClosed"]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.openTime = 0
        self.lastShot = 0
    def shoot(self,target,texture):
        self.openTime = pygame.time.get_ticks()
        self.image = self.textures["skelOpen"]
        direction = pygame.Vector2(target.rect.x - self.rect.x, target.rect.y - self.rect.y).normalize()
        projectile = GreenBall(self.rect.centerx, self.rect.centery, direction, texture)
        return projectile
    def update(self):
        if pygame.time.get_ticks() - self.openTime > 100:
            self.image = self.textures["skelClosed"]
            self.openTime = 0

class GreenBall(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, texture):
        super().__init__()
        self.image = pygame.image.load("assets/GreenBlast.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction
        self.speed = 10
        self.striker = 0
        self.madeTime = pygame.time.get_ticks()
    def update(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
        if pygame.time.get_ticks() - self.madeTime > 2000:
            self.kill()

class WallTile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill("brown")
        self.rect = self.image.get_rect(topleft=(x, y))