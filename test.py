import pygame
import math


class Flt (pygame.sprite.Sprite):

    def __init__(self):
        super(Flt, self).__init__()
        self.X = 600
        self.Y = 450
        self.surf = pygame.image.load('flt.png').convert_alpha()
        self.orgSurf = pygame.image.load('flt.png').convert_alpha()
        self.rect = self.surf.get_rect()
        self.boundingBox = pygame.Rect(600,450, self.orgSurf.get_width(), self.orgSurf.get_height())
        self.speed = 0
        self.maxSpeed = 0.4
        self.rotSpeed = 0.01
        self.acceleration = 0.0005
        self.angle = 0
        # from - 100 to +100
        self.steeringAngle = 0
        self.steeringAcceleration = 0.2

    def update(self, pressed_keys):
        if pressed_keys[pygame.K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[pygame.K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(5, 0)


pygame.init()

width = 1200
height = 900

screen = pygame.display.set_mode([width, height])

running = True

player = Flt()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()

    player.update(pressed_keys)


    screen.fill((240, 240, 240))
    screen.blit(player.surf, player.rect)
    pygame.display.flip()