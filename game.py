import pygame
import numpy

# Settings #

Resolution = [1280,720]
Initial_Player_Position = [400,300]
Player_Speed = 7
Player_Bullet_Speed = 20
Player_Bullet_Cooldown = 15 # ticks

Enemy_Health = 10
Enemy_Bullet_Speed = 4
Enemy_Bullet_Time = 5 * 60
Enemy_Bullet_Frequency = 200

Hit_Radius = 35

# Settings #

class Entity:
    def __init__(self, health, speed, X, Y):
        self.health = health
        self.speed = speed
        self.X = X
        self.Y = Y
    def get_health(self):
        return self.health
    def get_speed(self):
        return self.speed
    def set_X(self,x):
        self.X = x
        if self.X < 0:
            self.X = 0
        if self.X > Resolution[0]:
            self.X = Resolution[0]
    def set_Y(self,y):
        self.Y = y
        if self.Y < 0:
            self.Y = 0
        if self.Y > Resolution[1]:
            self.Y = Resolution[1]
    
class Player(Entity):
    score = 0
    can_shoot = True
    bullet_cooldown = Player_Bullet_Cooldown
    def __init__(self, health, speed, X, Y):
        super().__init__(health, speed, X, Y)
    def draw(self):
        pygame.draw.rect(screen, [255,255,255], [self.X-15,self.Y-25,10,10])
        pygame.draw.rect(screen, [200,0,0], [self.X-20,self.Y-25,35,4])
        pygame.draw.rect(screen, [255,255,255], [self.X-10,self.Y-20,13,10])
        pygame.draw.rect(screen, [255,255,255], [self.X-5,self.Y-15,15,10])
        pygame.draw.rect(screen, [200,0,0], [self.X-15,self.Y-2,55,4])
        pygame.draw.rect(screen, [255,255,255], [self.X-5,self.Y+5,15,10])
        pygame.draw.rect(screen, [0,0,200], [self.X,self.Y-10,20,20])
        pygame.draw.rect(screen, [255,255,255], [self.X-10,self.Y-5,40,10])
        pygame.draw.rect(screen, [255,255,255], [self.X-10,self.Y+10,13,10])
        pygame.draw.rect(screen, [255,255,255], [self.X-15,self.Y+15,10,10])
        pygame.draw.rect(screen, [200,0,0], [self.X-20,self.Y+21,35,4])

class Enemy(Entity):
    bullet_frequency = Enemy_Bullet_Frequency
    def __init__(self, health, speed, X, Y, target_X, target_Y, model):
        super().__init__(health, speed, X, Y)
        self.target_X = target_X
        self.target_Y = target_Y

        self.model = model
    def draw(self):
        if self.model == 0:
            pygame.draw.rect(screen, [255, 50, 50], [self.X-35, self.Y-4, 10, 8])
            pygame.draw.rect(screen, [200, 0, 0], [self.X-15, self.Y-15, 30, 30])
            pygame.draw.rect(screen, [200, 0, 0], [self.X-25, self.Y-10, 50, 20])
            pygame.draw.rect(screen, [200, 0, 0], [self.X-10, self.Y-25, 20, 50])
        elif self.model == 1:
            pygame.draw.rect(screen, [255, 50, 50], [self.X-35,self.Y-2,45,4])
            pygame.draw.rect(screen, [212, 123, 116], [self.X-25,self.Y-5,30,10])
            pygame.draw.circle(screen, [50,50,200], [self.X-20,self.Y],10)
            pygame.draw.rect(screen, [212, 123, 116], [self.X-5,self.Y-15,6,30])
            pygame.draw.rect(screen, [212, 123, 116], [self.X-20,self.Y-35,30,20])
            pygame.draw.rect(screen, [212, 123, 116], [self.X-20,self.Y+15,30,20])
            pygame.draw.rect(screen, [212, 123, 116], [self.X-40,self.Y-30,40,10])
            pygame.draw.rect(screen, [212, 123, 116], [self.X-40,self.Y+20,40,10])
        else:
            pygame.draw.circle(screen, [200,200,200], [self.X,self.Y], 25)
            pygame.draw.circle(screen, [50,50,200], [self.X-20,self.Y], 5)
            pygame.draw.circle(screen, [50,50,200], [self.X-7,self.Y], 5)
            pygame.draw.circle(screen, [50,50,200], [self.X+7,self.Y], 5)
            pygame.draw.circle(screen, [50,50,200], [self.X+20,self.Y], 5)

class Bullet:
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
    def draw(self):
        pygame.draw.rect(screen, [255,0,0], [self.X,self.Y-3,20,6])

class eBullet:
    time = Enemy_Bullet_Time
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
    def draw(self):
        pygame.draw.circle(screen, [255,255,0], [self.X,self.Y], 5)

pygame.font.init()
font = pygame.font.Font(None, 24)

time = 0
pygame.init()
screen = pygame.display.set_mode(Resolution)
pygame.display.set_caption("Space Shooter PyGame")

player = Player(100, Player_Speed, Initial_Player_Position[0], Initial_Player_Position[1])
bullets = []
enemys = []
ebullets = []

clock = pygame.time.Clock()
running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    screen.fill([30,30,30])

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.set_Y(player.Y - player.speed)
    if keys[pygame.K_s]:
        player.set_Y(player.Y + player.speed)
    if keys[pygame.K_d]:
        player.set_X(player.X + player.speed)
    if keys[pygame.K_a]:
        player.set_X(player.X - player.speed)
    if keys[pygame.K_SPACE]:
        if player.can_shoot:
            bullets.append(Bullet(player.X,player.Y))
            player.can_shoot = False

    if time == 0 or time == 120:
        enemys.append(Enemy(Enemy_Health,
                            numpy.random.randint(1,5),
                            Resolution[0],
                            numpy.random.randint(10,Resolution[1]-10),
                            numpy.random.randint(Resolution[0]/2,Resolution[0]-10),
                            numpy.random.randint(10,Resolution[1]-10),
                            numpy.random.randint(0,3))
        )

    for i in bullets[:]:
        i.X += Player_Bullet_Speed
        i.draw()
        if i.X > Resolution[0]:
            bullets.remove(i)

    for i in enemys[:]:
        i.draw()
        i.X -= i.speed * (i.X-i.target_X) / numpy.sqrt((i.X-i.target_X)*(i.X-i.target_X)+(i.Y-i.target_Y)*(i.Y-i.target_Y))
        i.Y -= i.speed * (i.Y-i.target_Y) / numpy.sqrt((i.X-i.target_X)*(i.X-i.target_X)+(i.Y-i.target_Y)*(i.Y-i.target_Y))
        if abs(i.X - i.target_X) < 10:
            i.target_X = numpy.random.randint(Resolution[0]/2,Resolution[0]-10)
        if abs(i.Y - i.target_Y) < 10:
            i.target_Y = numpy.random.randint(10,Resolution[1]-5)
        if (player.X-i.X)*(player.X-i.X)+(player.Y-i.Y)*(player.Y-i.Y) <= Hit_Radius * Hit_Radius:
            enemys.remove(i)
            player.health -= 40
        if i.bullet_frequency == 0:
            ebullets.append(eBullet(i.X,i.Y))
            i.bullet_frequency = Enemy_Bullet_Frequency
        i.bullet_frequency -= 1

    for i in bullets[:]:
        for j in enemys[:]:
            if (i.X-j.X)*(i.X-j.X)+(i.Y-j.Y)*(i.Y-j.Y) <= Hit_Radius * Hit_Radius:
                bullets.remove(i)
                enemys.remove(j)
                player.score += 5
    
    for i in ebullets[:]:
        if i.X < 0 or i.Y < 0 or i.X > Resolution[0] or i.Y > Resolution[1] or i.time == 0:
            ebullets.remove(i)
        i.X += Enemy_Bullet_Speed * (player.X-i.X) / numpy.sqrt((player.X-i.X)*(player.X-i.X)+(player.Y-i.Y)*(player.Y-i.Y))
        i.Y += Enemy_Bullet_Speed * (player.Y-i.Y) / numpy.sqrt((player.X-i.X)*(player.X-i.X)+(player.Y-i.Y)*(player.Y-i.Y))
        i.draw()
        i.time -= 1
        if (player.X-i.X)*(player.X-i.X)+(player.Y-i.Y)*(player.Y-i.Y) <= Hit_Radius * Hit_Radius:
            ebullets.remove(i)
            player.health -= 15

    if player.health <= 0:
        running = False

    if player.can_shoot == False:
        player.bullet_cooldown -= 1
        if player.bullet_cooldown < 0:
            player.bullet_cooldown = Player_Bullet_Cooldown
            player.can_shoot = True

    player.draw()
    stats = font.render(
        f"Score: {player.score}        Number of Enemies: {len(enemys)}",
        True,[255,255,255]
    )
    health_stats = font.render(
        f"Health  {player.health}%",
        True,[255,255,255]
    )
    pygame.draw.rect(screen, [100, 100, 100], [120,7,200,20])
    pygame.draw.rect(screen, [49, 232, 55], [120,7,player.health*2,20])
    screen.blit(stats,[10,Resolution[1]-30])
    screen.blit(health_stats,[10,10])
    pygame.display.flip()

    time += 1
    if time > 240:
        time = 0
    clock.tick(60)

pygame.quit()