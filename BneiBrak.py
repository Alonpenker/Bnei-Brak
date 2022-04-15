import pygame
from random import randint
import os
pygame.init()
screenWidth = 800
screenHeight = 600
display = (screenWidth, screenHeight)
win = pygame.display.set_mode(display)
pygame.display.set_caption("Bnei Brak")
bg = pygame.image.load(os.path.join('Images','street.png')).convert()
haredi = pygame.image.load(os.path.join('Images','haredi.png')).convert_alpha()
mehabel = pygame.image.load(os.path.join('Images','teR1.png')).convert_alpha()
mehabel1 = pygame.image.load(os.path.join('Images','teR2.png')).convert_alpha()
mehabel2 = pygame.image.load(os.path.join('Images','teR3.png')).convert_alpha()
walkRight = [pygame.image.load(os.path.join('Images','haR1.png')).convert_alpha(),pygame.image.load(os.path.join('Images','haR2.png')).convert_alpha(),pygame.image.load(os.path.join('Images','haR1.png')).convert_alpha(),pygame.image.load(os.path.join('Images','haR3.png')).convert_alpha()]
walkLeft = [pygame.image.load(os.path.join('Images','haL1.png')).convert_alpha(),pygame.image.load(os.path.join('Images','haL2.png')).convert_alpha(),pygame.image.load(os.path.join('Images','haL1.png')).convert_alpha(),pygame.image.load(os.path.join('Images','haL3.png')).convert_alpha()]
drivingCar = [pygame.image.load(os.path.join('Images','car1.png')).convert_alpha(),pygame.image.load(os.path.join('Images','car2.png')).convert_alpha(),pygame.image.load(os.path.join('Images','car3.png')).convert_alpha(),pygame.image.load(os.path.join('Images','car4.png')).convert_alpha()]
button = [pygame.image.load(os.path.join('Images','button1.png')).convert_alpha(),pygame.image.load(os.path.join('Images','button2.png')).convert_alpha()]
rock1 = pygame.image.load(os.path.join('Images','rock1.png')).convert_alpha()
rock2 = pygame.image.load(os.path.join('Images','rock2.png')).convert_alpha()
rock3 = pygame.image.load(os.path.join('Images','rock3.png')).convert_alpha()
rocket1 = pygame.image.load(os.path.join('Images','rocket1.png')).convert_alpha()
alert = pygame.image.load(os.path.join('Images','alert.png')).convert_alpha()
title = pygame.image.load(os.path.join('Images','title.png')).convert_alpha()
pygame.display.set_icon(haredi)
myFont = pygame.font.SysFont("Comic Sans MS",30)
otherFont = pygame.font.SysFont("Comic Sans MS", 18)
anotherFont = pygame.font.SysFont ('calibri', 30)
timer=0 #miliseconds
time=1 #seconds
lastTime = 0
bestTime = 0
initialX = 50
initialY = 440
class Player():
    def __init__(self,x,y,width,height,vel):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.vel = vel
        self.isJumping=False
        self.jumpCount=10
        self.right = False
        self.left = False
        self.walkCount = 0
    def draw(self,win):
        if self.walkCount+1>=12:
            self.walkCount =0
        if self.right:
            win.blit(walkRight[self.walkCount//3],(self.x,self.y))
            if self.isJumping==False:
              self.walkCount += 1
            else:
              self.walkCount = 9
        elif self.left:
            win.blit(walkLeft[self.walkCount//3],(self.x,self.y))
            if self.isJumping==False:
              self.walkCount += 1
            else:
              self.walkCount = 9
        else:
            win.blit(haredi,(self.x,self.y))
class Terrorist():
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.throw = False
        self.throwCount = 0
    def draw(self,win):
        if self.throw:
            if self.throwCount==1:
              win.blit(mehabel1,(self.x,self.y))
            if self.throwCount==2:
              win.blit(mehabel2,(self.x,self.y))
        else:
            win.blit(mehabel,(self.x,self.y))
class Rock():
    def __init__(self,x,y,width,height,type,vel,maxVel):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.type = type
        self.vel = vel
        self.maxVel = maxVel
    def draw(self,win):
        if self.type==1:
            self.width = 21
            self.height = 13
            win.blit(rock1, (self.x, self.y))
        if self.type==2:
            self.width = 28
            self.height = 30
            win.blit(rock2, (self.x, self.y))
        if self.type==3:
            self.width = 28
            self.height = 13
            win.blit(rock3, (self.x, self.y))
class Rocket():
    def __init__(self,x,y,width,height,vel,maxVel):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.vel = vel
        self.maxVel = maxVel
    def draw(self,win):
        win.blit(rocket1, (self.x, self.y))
        #pygame.draw.rect(win,(0,255,0),(self.x,self.y,self.width,self.height))
class Car():
    def __init__(self,x,y,width,height,vel,maxVel):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.vel = vel
        self.maxVel = maxVel
        self.countDown = 500
        self.drive = False
        self.driveCount = 0
    def draw(self,win):
        if self.driveCount+1>=8:
            self.driveCount = 0
        win.blit(drivingCar[self.driveCount//2],(self.x,self.y))
        self.driveCount += 1
ha = Player(initialX,initialY,30,82,5)
te = Terrorist(screenWidth-30,initialY+82-71,30,71)
rock = Rock(screenWidth,randint(37,45)*10,5,5,3,1,24)
rocket = Rocket(randint(5,250),-1*randint(75,125),30,75,1,20)
car = Car(-100,initialY+82-73,100,73,3,9)
g=1 #gravitational acceleration
alarm = False
alarmCountDown = randint(300,500)
gotEliminated = False
openingScreen = True
transitionScreen = False
gameScreen = False
run = True
def blit_alpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)
    target.blit(temp, location)
def hit():
    ha.x = initialX
    ha.y = initialY
    global rock,rocket,car,neg,lastTime,bestTime,time,timer,gotEliminated,alarm, alarmCountDown
    rock.x = screenWidth
    rock.y = randint(37, 45) * 10
    rock.vel = 1
    rocket.vel = 1
    rock.type = randint(1,3)
    rocket.y = -1*randint(rocket.height,rocket.height+50)
    rocket.x = randint(5, 250)
    car.x = -car.width
    car.countDown = 500
    car.vel = 3
    alarm = False
    alarmCountDown = randint(300,500)
    ha.jumpCount = 10
    ha.isJumping = False
    neg = 1
    if time>bestTime:
        bestTime=time
    lastTime = time
    time = 1
    timer = 0
    gotEliminated = True
while run:
    if openingScreen:
        win.blit(bg, (0, 0))
        pygame.time.delay(30)
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (300 + 200 > mouse[0] > 300) and (500 + 75 > mouse[1] > 500):
                    transitionScreen = True
                    openingScreen = False
        if (300 + 200 > mouse[0] > 300) and (500 + 75 > mouse[1] > 500):
            win.blit(button[1],(300,500))
        else:
            win.blit(button[0], (300, 500))
        win.blit(title,(175,100))
        #pygame.draw.rect(win,(255,0,255),(150,100,450,150))
    if transitionScreen:
        win.fill((0,0,0))
        blit_alpha(win, bg, (0, 0), 100-int(timer*(100/2.1)))
        pygame.time.delay(30)
        timer+=0.03
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        mouse = pygame.mouse.get_pos()
        if ((timer-2.1)/3.3)<=1 and timer>=2.1:
            story = anotherFont.render("שדחמ עבצנ ,2021 יאמ ,קרב ינב", 1, (int(255*((timer-2.1)/3.3)),int(255*((timer-2.1)/3.3)),int(255*((timer-2.1)/3.3))))
            win.blit(story, (220, 250))
        elif timer>=5.4:
            story = anotherFont.render("שדחמ עבצנ ,2021 יאמ ,קרב ינב", 1,(255, 255, 255))
            win.blit(story, (220, 250))
        if timer>=6:
            gameScreen = True
            transitionScreen = False
            timer=0
    if gameScreen:
        win.blit(bg, (0, 0))
        pygame.time.delay(30)  # milliseconds
        timer += 30
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and ha.x > ha.vel:
            ha.x -= ha.vel
            ha.right = False
            ha.left = True
        elif keys[pygame.K_RIGHT] and ha.x < (screenWidth - ha.width - ha.vel):
            ha.x += ha.vel
            ha.right = True
            ha.left = False
        else:
            ha.right = False
            ha.left = False
            ha.walkCount = 0
        if keys[pygame.K_DOWN]:
            if rock.x >= ha.x and rock.x <= (ha.x + ha.width):
                if rock.y > (ha.y + ha.height):
                    hit()
            ha.jumpCount = 10
            ha.isJumping = False
            ha.y = initialY
        if not (ha.isJumping):
            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                ha.isJumping = True
                #ha.walkCount = 0
        else:
            if ha.jumpCount >= -10:
                neg = 1
                if ha.jumpCount < 0:
                    neg = -1
                ha.y -= int(((1 / g) * ha.jumpCount ** 2) * 0.5 * neg)
                ha.jumpCount -= 1
            else:
                ha.isJumping = False
                ha.jumpCount = 10
        if rock.x < 0:
            rock.x = screenWidth
            rock.y = randint(37, 45) * 10
            rock.type = randint(1, 3)
            if rock.vel < rock.maxVel:
                rock.vel += 1
        if car.x >= screenWidth:
            car.x = -car.width
            car.countDown = 500
            if car.vel < car.maxVel:
                car.vel += 2
        if alarmCountDown >= 0:
            alarmCountDown -= 1
        else:
            if alarm == False:
                alarm = True
                alarmCountDown = randint(300, 500)
            elif alarm == True and rocket.y + rocket.height >= initialY + ha.height:
                alarm = False
                alarmCountDown = randint(300, 500)
        if rock.x >= ha.x and rock.x <= (ha.x + ha.width) and rock.y >= ha.y and rock.y <= (ha.y + ha.height):  # פסילה מכדור
            hit()
        if rocket.x >= ha.x and rocket.x <= (ha.x + ha.width) and rocket.y >= ha.y and rocket.y <= (ha.y + ha.height):  # פסילה מרקטה
            hit()
        if car.x <= ha.x and (car.x + car.width) >= ha.x and car.y >= ha.y and car.y <= (ha.y + ha.height):  # פסילה מאוטו
            hit()
        if rocket.y + rocket.height >= initialY + ha.height and alarmCountDown > 0:
            rocket.y = -1 * randint(rocket.height, rocket.height + 50)
            rocket.x = randint(5, 400)
            if rocket.vel <= rocket.maxVel:
                rocket.vel += 2
        if rock.x == screenWidth or rock.x < 40:
            te.throw = True
            te.throwCount = 1
        elif rock.x < screenWidth and rock.x > screenWidth - 100:
            te.throw = True
            te.throwCount = 2
        else:
            te.throw = False
            te.throwCount = 0
        if rock.vel >= rock.maxVel - 8 and rock.x == screenWidth:
            if randint(1, 20) == 20:
                rock.x -= rock.vel
        else:
            rock.x -= rock.vel
        if timer < 1000:
            score = myFont.render("Time alive: 0", 1, (0, 0, 0))
            win.blit(score, (20, 40))
        if timer >= 1000:
            if timer % 30 == 0:
                time += 0.03
            score = myFont.render(("Time alive: %3.2f" % time), 1, (0, 0, 0))
            win.blit(score, (20, 40))
        if gotEliminated == True:
            score = otherFont.render(("Last time: %3.2f seconds" % lastTime), 1, (0, 0, 0))
            win.blit(score, (20, 80))
            best = otherFont.render(("Best time: %3.2f seconds" % bestTime), 1, (0, 0, 0))
            win.blit(best, (20, 100))
        ha.draw(win)
        te.draw(win)
        rock.draw(win)
        if alarm == True:
            rocket.y += rocket.vel
            win.blit(alert, (600, 50))
            rocket.draw(win)
        if car.countDown > 0:
            car.countDown -= 1
        else:
            car.x = car.x + car.vel
            car.draw(win)
    pygame.display.update()
pygame.quit()
#TODO: explosion