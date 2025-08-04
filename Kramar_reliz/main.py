from pygame import*
from random import*
from time import time as timer

img_back = "background.png"
img_hero = "hero.png"
img_enemy = "enemy.png"

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, x, y, width, height, speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys [K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height-self.rect.height:
            self.rect.y+=self.speed 
        if keys[K_RIGHT] and self.rect.x < win_width -80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 30, 30, -15)
        bullets.add(bullet)
        
        
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1            

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
    

window = display.set_mode((700, 500))
display.set_caption("SHOOTER")
background = transform.scale(image.load(img_back), (700, 500))

win_width = 700
win_height = 500
run = True
clock = time.Clock()
FPS = 60
finish = False

life = 10
lost = 0
max_lost = 4
rel_time = False
num_fire = 0
goal = 30
score = 0

font.init()
font2 = font.Font(None, 36)


ship = Player(img_hero, 25, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

img_bullet = "bullet.png"
bullets = sprite.Group()

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:  
                if num_fire < 20 and  rel_time == False:
                    num_fire = num_fire + 1
                    ship.fire()
                
                if num_fire >= 20 and rel_time == False:
                    last_time = timer()
                    rel_time = True
        
    
    if not finish:
        window.blit(background, (0,0))

        text = font2.render("Рахунок: " +str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено: " +str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))


        ship.reset()
        ship.update()
        
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render("Триває перезарядка.....", 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0 
                rel_time = False

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False):
                sprite.spritecollide(ship, monsters, True)
                life = life - 1

        lose = font2.render("Ви програли!!! " , 1, (255, 255, 255))
        win = font2.render("Ви виграли!!! " , 1, (0, 255, 0))

        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
        
        if life==3:
            life_color=(0,150,0)
        if life==2:
            life_color=(150,150,0)
        if life==1:
            life_color=(150,0,0)
        text_life=font2.render("життя "+str(life),1,(0,150,0))
        window.blit(text_life,(450,10))
        display.update()
    time.delay(50)
