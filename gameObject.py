import pygame
import random
import math


def rot_center(image, rect, angle):
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image, rot_rect


def rotate_point(cx, cy, angle, p):
    s = math.sin(math.radians(-angle))
    c = math.cos(math.radians(-angle))
    p.x -= cx
    p.y -= cy
    xnew = p.x * c - p.y * s
    ynew = p.x * s + p.y * c
    p.x = xnew + cx
    p.y = ynew + cy
    return p


class GameObject(pygame.sprite.Sprite):
    def __init__(self, imageFile):
        super(GameObject, self).__init__()
        self.surf = pygame.image.load(imageFile)
        self.orgSurf = pygame.image.load(imageFile)
        self.rect = self.surf.get_rect()
        self.orgRect = self.orgSurf.get_rect()
        self.angle = random.randint(0, 360)
        self.X = 0
        self.Y = 0
        self.p1 = pygame.math.Vector2(0, 0)
        self.p2 = pygame.math.Vector2(0, 0)
        self.p3 = pygame.math.Vector2(0, 0)
        self.p4 = pygame.math.Vector2(0, 0)
        self.boundingBox = [self.p1, self.p2, self.p3, self.p4]

    def position(self):
        self.surf, self.rect = rot_center(self.orgSurf, self.orgSurf.get_rect(), self.angle)

        self.rect.center = (self.X, self.Y)
        self.p1.x = self.X - self.orgRect.width/2
        self.p1.y = self.Y - self.orgRect.height/2
        self.p2.x = self.X + self.orgRect.width/2
        self.p2.y = self.Y - self.orgRect.height/2
        self.p3.x = self.X + self.orgRect.width/2
        self.p3.y = self.Y + self.orgRect.height/2
        self.p4.x = self.X - self.orgRect.width/2
        self.p4.y = self.Y + self.orgRect.height/2

        self.p1 = rotate_point(self.X, self.Y, self.angle, self.p1)
        self.p2 = rotate_point(self.X, self.Y, self.angle, self.p2)
        self.p3 = rotate_point(self.X, self.Y, self.angle, self.p3)
        self.p4 = rotate_point(self.X, self.Y, self.angle, self.p4)