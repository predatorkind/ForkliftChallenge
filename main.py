import random

import pygame
import math
import time
import os

import gameObject
import dbOperations


def collideLineLine(P0, P1, Q0, Q1):
    d = (P1[0] - P0[0]) * (Q1[1] - Q0[1]) + (P1[1] - P0[1]) * (Q0[0] - Q1[0])
    if d == 0:
        return False
    t = ((Q0[0] - P0[0]) * (Q1[1] - Q0[1]) + (Q0[1] - P0[1]) * (Q0[0] - Q1[0])) / d
    u = ((Q0[0] - P0[0]) * (P1[1] - P0[1]) + (Q0[1] - P0[1]) * (P0[0] - P1[0])) / d
    return 0 <= t <= 1 and 0 <= u <= 1


def collideRectLine(p1, p2, rect):
    return (collideLineLine(p1, p2, rect[0], rect[1]) or
            collideLineLine(p1, p2, rect[1], rect[2]) or
            collideLineLine(p1, p2, rect[2], rect[3]) or
            collideLineLine(p1, p2, rect[3], rect[0]))


def collideSprites(sprite1, sprite2):
    if math.dist((sprite1.X, sprite1.Y), (sprite2.X, sprite2.Y)) > 220:
        #print("object too far")
        return False
    else:
        #print("object in range. checking..")
        return (collideRectLine(sprite1.boundingBox[0], sprite1.boundingBox[1], sprite2.boundingBox) or
                collideRectLine(sprite1.boundingBox[1], sprite1.boundingBox[2], sprite2.boundingBox) or
                collideRectLine(sprite1.boundingBox[2], sprite1.boundingBox[3], sprite2.boundingBox) or
                collideRectLine(sprite1.boundingBox[3], sprite1.boundingBox[0], sprite2.boundingBox))


def blitRotateCenter(surf, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)

    surf.blit(rotated_image, new_rect)


def rot_center(image, rect, angle):
    """rotate an image while keeping its center"""
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    # print("Angle: " + str(angle))
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

class Timer:
    def __init__(self):
        self.startTime = None
        self.timeLimit = 0

    def start(self, timeLimit):
        self.startTime = time.perf_counter()
        self.timeLimit = timeLimit

    def getTimeLeft(self):

        return int(self.startTime + self.timeLimit - time.perf_counter())

class Flt(pygame.sprite.Sprite):

    def __init__(self):
        super(Flt, self).__init__()
        self.X = 600
        self.Y = 450
        self.tempX = 0
        self.tempY = 0
        self.surf = pygame.image.load(os.path.dirname(__file__) +'\\flt.png').convert_alpha()
        self.orgSurf = pygame.image.load(os.path.dirname(__file__) +'\\flt.png').convert_alpha()
        #self.orgSurf.get_rect().centerx -= self.orgSurf.get_rect().width/2
        #self.orgSurf.get_rect().centery -= self.orgSurf.get_rect().height/2
        self.rect = self.surf.get_rect()
        self.orgRect = self.orgSurf.get_rect()

        self.p1 = pygame.math.Vector2(self.X - self.orgRect.width/2, self.Y - self.orgRect.height/2)
        self.p2 = pygame.math.Vector2(self.X + self.orgRect.width/2, self.Y - self.orgRect.height/2)
        self.p3 = pygame.math.Vector2(self.X - self.orgRect.width/2, self.Y + self.orgRect.height/2)
        self.p4 = pygame.math.Vector2(self.X + self.orgRect.width/2, self.Y + self.orgRect.height/2)

        # self.p1 = pygame.math.Vector2(self.op1.x, self.op1.y)
        # self.p2 = pygame.math.Vector2(self.op2.x, self.op2.y)
        # self.p3 = pygame.math.Vector2(self.op3.x, self.op3.y)
        # self.p4 = pygame.math.Vector2(self.op4.x, self.op4.y)

        self.boundingBox = [self.p1, self.p2, self.p3, self.p4]
        self.speed = 0
        self.maxSpeed = 0.6
        self.rotSpeed = 0.01
        self.acceleration = 0.001
        self.angle = 0
        # from - 100 to +100
        self.steeringAngle = 0
        self.steeringAcceleration = 0.2

        # fltImg = pygame.image.load('flt.png')
        # self.surf.blit(fltImg, (0, 0))

    def rotate(self):
        self.surf = pygame.transform.rotate(self.orgSurf, self.angle)
        self.rect = self.surf.get_rect(center=self.orgSurf.get_rect(center=(self.X, self.Y)).center)

    def movePlayer(self, keys):
        if keys[pygame.K_RIGHT]:
            self.steeringAngle = self.steeringAngle - self.steeringAcceleration
            if self.steeringAngle < -100:
                self.steeringAngle = - 100

        if keys[pygame.K_LEFT]:
            self.steeringAngle = self.steeringAngle + self.steeringAcceleration
            if self.steeringAngle > 100:
                self.steeringAngle = 100

        if self.steeringAngle < 0.2 and self.steeringAngle > -0.2:
            self.steeringAngle = 0
            # player.angle = (player.angle - player.rotSpeed)%360

        # print ( player.steeringAngle)

        if keys[pygame.K_SPACE]:
            # if player.speed < 0:
            self.speed = self.speed / 1.05
            if self.speed < 0.001:
                self.speed = 0
        else:
            if keys[pygame.K_UP]:
                self.speed = self.speed + self.acceleration
                if self.speed > self.maxSpeed:
                    self.speed = self.maxSpeed
            if keys[pygame.K_DOWN]:
                if self.speed < 0:
                    self.speed = self.speed - self.acceleration
                else:
                    self.speed = self.speed - self.acceleration * 2
                # if player.speed < 0:
                # player.speed = 0

        if keys[pygame.K_p]:
            print("_______________________________")
            print("Player cords: " + str(self.X) + " / " + str(self.Y))
            print("Temp: " + str(self.tempX) + " / " + str(self.tempY))
            print("p1: " + str(self.p1.x) + " / " + str(self.p1.y))

        modifier = self.steeringAngle
        modRotSpeed = self.rotSpeed * (modifier / 1) * (self.speed / self.maxSpeed)
        if self.steeringAngle < 0.00001 and self.steeringAngle > -0.00001:
            modifier = 0.00001

        modSpeed = abs(self.speed * (1 / modifier))

        # player.angle = (player.angle + player.rotSpeed) % 360
        self.angle = (self.angle + modRotSpeed) % 360

        self.tempX = self.X - (math.cos(math.radians(self.angle)) * self.speed)
        self.tempY = self.Y + (math.sin(math.radians(self.angle)) * self.speed)
        # tempX = player.X - (math.cos(math.radians(player.angle)) * modSpeed)
        # tempY = player.Y + (math.sin(math.radians(player.angle)) * modSpeed)

        if (self.tempX > 0 and self.tempX < width) and (self.tempY > 0 and self.tempY < height):
            self.X = self.tempX
            self.Y = self.tempY
            #self.rect.move_ip(self.tempX + 5, self.tempY + 5)

        else:
            if self.speed >0:
                self.speed = -0.1
            else:
                self.speed = 0.1



        self.surf, self.rect = rot_center(self.orgSurf, self.orgSurf.get_rect(), self.angle)

        self.rect.center = (self.tempX, self.tempY)
        #self.orgSurf.get_rect().center = (self.tempX, self.tempY)

        self.p1.x = self.tempX - self.orgRect.width/2
        self.p1.y = self.tempY - self.orgRect.height/2
        self.p2.x = self.tempX + self.orgRect.width/2
        self.p2.y = self.tempY - self.orgRect.height/2
        self.p3.x = self.tempX + self.orgRect.width/2
        self.p3.y = self.tempY + self.orgRect.height/2
        self.p4.x = self.tempX - self.orgRect.width/2
        self.p4.y = self.tempY + self.orgRect.height/2

        self.p1 = rotate_point(self.tempX, self.tempY, self.angle, self.p1)
        self.p2 = rotate_point(self.tempX, self.tempY, self.angle, self.p2)
        self.p3 = rotate_point(self.tempX, self.tempY, self.angle, self.p3)
        self.p4 = rotate_point(self.tempX, self.tempY, self.angle, self.p4)


class Floor(pygame.sprite.Sprite):
    def __init__(self):
        self.surf = pygame.image.load(os.path.dirname(__file__) +'\\floor.jpg')


class Cone(gameObject.GameObject):
    def __init__(self):
        super(Cone, self).__init__(os.path.dirname(__file__) +'\\cone.png')



class Pallet(gameObject.GameObject):
    def __init__(self):
        super(Pallet, self).__init__(os.path.dirname(__file__) +'\\pallet2.png')
        
class Boss(gameObject.GameObject):
    def __init__(self):
        super(Boss, self).__init__(os.path.dirname(__file__) +'\\boss.png')

class BloodSpill(gameObject.GameObject):
    def __init__(self):
        super(BloodSpill, self).__init__(os.path.dirname(__file__) +'\\blood.png')
        
class DamagedCone(gameObject.GameObject):
    def __init__(self):
        super(DamagedCone, self).__init__(os.path.dirname(__file__) +'\\coneDmg.png')




def spawnPallets(count):
    if count>10:
        count = 10
    palletList = pygame.sprite.Group()
    while len(palletList) < count:
        pallet = Pallet()

        x = random.randint(20, width - 20)
        y = random.randint(20, height - 20)

        if x > 450 and x < 750 and y > 350 and y < 450:
            print("discarding object")
        else:
            pallet.X = x
            pallet.Y = y
            pallet.position()
            palletList.add(pallet)

    return palletList


def spawnCones(count):
    if count>20:
        count = 20
    cones = pygame.sprite.Group()
    while len(cones) < count:
        cone = Cone()
        x = random.randint(20, width - 20)
        y = random.randint(20, height - 20)

        if x > 450 and x < 750 and y > 350 and y < 450:
            print("discarding object")
        else:
            cone.X = x
            cone.Y = y
            cone.position()
            cones.add(cone)

    return cones

def spawnBosses(count):
    bosses = pygame.sprite.Group()
    while len(bosses) < count:
        boss = Boss()
        x = random.randint(20, width - 20)
        y = random.randint(20, height - 20)

        if x > 400 and x < 800 and y > 300 and y < 600:
            print("discarding object")
        else:
            boss.X = x
            boss.Y = y
            boss.position()
            bosses.add(boss)

    return bosses



def renderText(text, x, y, center, color, font, surface):
    if font.get_height() > 50:
        increment = 50
    else:
        increment = 30
    y -= increment

    for line in text:
        element = font.render(line, True, color)
        rect = element.get_rect()
        if center:
            rect.center = (x,y)
        else:
            rect = (x,y)
        surface.blit(element, rect)
        y += increment

path = os.path.expanduser("~")
path1 = os.path.join(path, "Autostore Operations Database")
print(path1)
os.chdir(os.path.dirname(path1))
pygame.init()

width = 1200
height = 900
textCol = (70, 80, 60)
currentScore = 0

screen = pygame.display.set_mode([width, height])
pygame.display.set_caption('Challenge 2')



fontBig = pygame.font.SysFont(None, 62)
fontMedium = pygame.font.SysFont(None, 42)
fontSmall = pygame.font.SysFont(None, 30)


# textTitle = fontTitle.render("Challange 2", True, textCol)
# textTitleRect = textTitle.get_rect()
# textTitleRect.center = (width/2,height/2)
#
# fontSubTitle = pygame.font.SysFont(None, 42)
# textSubTitle = fontSubTitle.render("Press Spacebar to Start.", True, textCol)
# textSubTitleRect = textSubTitle.get_rect()
# textSubTitleRect.center = (width/2, height/2 +60)
#
# fontScore = pygame.font.SysFont(None, 42)
# textScore = fontScore.render("SCORE: " + str(currentScore), True, textCol)
# textScoreRect = textScore.get_rect()
# textScoreRect = (40, 40)

animating = False
running = True
playing = False
gameOverFlag = False
levelCompleteFlag = False
saveScoreFlag = False


player = Flt()
floor = Floor()
pallets = None
cones = None
bosses = None
bloodSpills = None
dmgCones = None

currentLevel = 1
currentScore = 0
minimumHiscore = 0
hiScore = 0
name = ""
names = []
scores = []
(names, scores) = dbOperations.getHiscores()
if(len(scores)>4):
    minimumHiscore = int(scores[-1])

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if gameOverFlag == False and playing == False and saveScoreFlag == False:
                    playing = True
                    animating = True
                    pallets = spawnPallets(currentLevel * 1)
                    cones = spawnCones(int(currentLevel * 2.3))
                    bosses = spawnBosses(int(currentLevel * 0.4))

                    bloodSpills = pygame.sprite.Group()
                    dmgCones = pygame.sprite.Group()
                    print("bosses count: " + str(len(bosses)))
                    timer = Timer()
                    timer.start(31)
                if gameOverFlag:
                    gameOverFlag = False
                    animating = False
                    if currentScore > minimumHiscore:
                        saveScoreFlag = True
                        hiScore = currentScore
                    currentLevel = 1
                    currentScore = 0
                    player.X = 600
                    player.Y = 450
                    player.angle = 0

                if levelCompleteFlag:
                    levelCompleteFlag = False
                    playing = True
                    animating = True

                if saveScoreFlag:
                    name += " "
                    if len(name) > 12:
                        name = name[:-1]

            elif event.key == pygame.K_ESCAPE:
                playing = False
                animating = False
                levelCompleteFlag = False
                gameOverFlag = False
                saveScoreFlag = False
                currentLevel = 1
                currentScore = 0
                player.X = 600
                player.Y = 450
                player.angle = 0

            elif event.key == pygame.K_RETURN:
                name = name.strip()
                if len(name) > 1:

                    dbOperations.saveHiscore(name, hiScore)
                    name = ""
                    hiScore = 0
                    (names, scores) = dbOperations.getHiscores()
                    if len(scores) > 4:
                        minimumHiscore = int(scores[-1])
                        print("minHiScore: " + str(minimumHiscore))

                saveScoreFlag = False

            elif event.key == pygame.K_BACKSPACE:

                name = name[:-1]

            else:

                name += event.unicode
                if len(name) > 12:
                    name = name[:-1]



        #         circleX = circleX - 1
        #     elif event.key == pygame.K_RIGHT:
        #         circleX = circleX + 1
        #     elif event.key == pygame.K_UP:
        #         circleY = circleY - 1
        #     elif event.key == pygame.K_DOWN:
        #         circleY = circleY + 1

    keys = pygame.key.get_pressed()

    screen.fill((240, 240, 240))
    screen.blit(floor.surf, (0, 0))

    if animating:
        for s in bloodSpills:
            screen.blit(s.surf, s.rect)

        for dc in dmgCones:
            screen.blit(dc.surf, dc.rect)

        for p in pallets:
            screen.blit(p.surf, p.rect)

        for c in cones:
            screen.blit(c.surf, c.rect)

        for b in bosses:
            screen.blit(b.surf, b.rect)

        screen.blit(player.surf, player.rect)

    if not playing and not gameOverFlag and not levelCompleteFlag and not saveScoreFlag:
        renderText(["Challenge 2"], width/2, 300, True, textCol, fontBig, screen)
        renderText(["Press Spacebar to Start"], width/2, 400, True, textCol, fontMedium, screen)
        renderText(names, width/2 - 100, 500, True, textCol, fontSmall, screen)
        renderText(scores, width/2 + 100, 500, True, textCol, fontSmall, screen)
        renderText(["Collect all pallets. Avoid obstacles.", "Use arrow keys to steer and spacebar to brake.", "Do not forget to stop when your job is done."], width / 2, 800, True, textCol, fontSmall, screen)

    if levelCompleteFlag:
        renderText(["LEVEL " + str(currentLevel-1) + " COMPLETE!"], width/2, 300, True, textCol, fontBig, screen)
        renderText(["Current Score: " + str(currentScore)], width/2,  400, True, textCol,fontMedium, screen)

    if gameOverFlag:
        renderText(["GAME OVER!"], width/2, 300, True, textCol, fontBig, screen)
        renderText(["Your Final Score: " + str(currentScore)], width / 2, 400, True, textCol, fontMedium, screen)

    if saveScoreFlag:
        renderText(['You have got a Hi Score!'], width/2, 300, True, textCol, fontBig, screen)
        renderText(['Enter your name:'], width/2, 360, True, textCol, fontMedium, screen)
        textBox = pygame.Rect(0,0, 200, 50)
        textBox.center = (width/2, 430)
        pygame.draw.rect(screen, textCol, textBox, 2)
        renderText([name], width/2, 460, True, textCol, fontSmall, screen)


    if playing:
        player.movePlayer(keys)


        # pygame.draw.circle(screen, (200,100, 100), (player.X, player.Y), 10)
        # pygame.draw.rect(screen, (150,100,100), player.rect, 2)
        # for p in player.boundingBox:
        #     pygame.draw.circle(screen, (50, 200, 50), (p.x, p.y), 5)
        #
        # for e in pallets:
        #     for p in e.boundingBox:
        #         pygame.draw.circle(screen, (50,200, 50), (p.x, p.y), 5)
        #         pygame.draw.rect(screen, (150,100,100), e.rect, 3)
        # for e in cones:
        #     for p in e.boundingBox:
        #         pygame.draw.circle(screen, (50,200,50), (p.x, p.y), 5)
        #         pygame.draw.rect(screen, (150, 100, 100), e.rect, 3)

        # pygame.sprite.spritecollide(player, pallets, False)
        collisionList = pygame.sprite.spritecollide(player, bosses, False, collided=collideSprites)

        for b in collisionList:
            print("collided with boss: " + str(b.rect))
            ##todo replace with blood
            blood = BloodSpill()
            blood.X = b.X
            blood.Y = b.Y
            blood.position()
            bloodSpills.add(blood)
            b.kill()
            currentScore -= 100
            gameOverFlag = True
            playing = False

        collisionList = pygame.sprite.spritecollide(player, pallets, False, collided=collideSprites)

        for e in collisionList:
            print("collided with pallet: " + str(e.rect))
            e.kill()
            currentScore += 5
            print("Pallets count: " + str(len(pallets)))

        collisionList = pygame.sprite.spritecollide(player, cones, False, collided=collideSprites)

        for e in collisionList:
            print("collided with cone: " + str(e.rect))
            dmgCon = DamagedCone()
            dmgCon.X = e.X
            dmgCon.Y = e.Y
            dmgCon.position()
            dmgCones.add(dmgCon)
            e.kill()
            currentScore -= 1
            print("Cones count: " + str(len(cones)))

        if len(pallets) == 0 and player.speed == 0:
            levelCompleteFlag = True
            currentLevel = currentLevel + 1
            currentScore += timer.getTimeLeft()
            playing = False
            player.X = 600
            player.Y = 450
            player.angle = 0

        renderText(["SCORE: " + str(currentScore)], 40, 40, False, textCol, fontMedium, screen)
        renderText(["TIME: " + str(timer.getTimeLeft())], 240, 40, False, textCol, fontMedium, screen)

        if timer.getTimeLeft() == 0:
            gameOverFlag= True
            playing = False


    pygame.display.flip()

pygame.quit()
