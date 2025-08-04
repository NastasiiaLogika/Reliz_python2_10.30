from pygame import *
from random import *
from time import time as timer

# Зображення
img_back = "background.png"
img_hero = "rocket.png"
img_enemy = "enemy.png"
img_bullet = "bullet.png"
img_heart = "heart.png"  # нове зображення для сердець

# Клас спрайту
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, x, y, width, height, speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Гравець
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

# Вороги
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1

# Кулі
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

# СЕРЦЯ-БОНУСИ
class Heart(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.kill()

# Вікно
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("SHOOTER")
background = transform.scale(image.load(img_back), (win_width, win_height))

# Змінні гри
run = True
clock = time.Clock()
FPS = 60
finish = False

life = 3
lost = 0
max_lost = 3
rel_time = False
num_fire = 0
goal = 10
score = 0

# Шрифти
font.init()
font2 = font.Font(None, 36)

# Створення об'єктів
ship = Player(img_hero, 25, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(5):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

bullets = sprite.Group()
hearts = sprite.Group()  # група для сердець

# Основний цикл
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 10 and not rel_time:
                    num_fire += 1
                    ship.fire()
                if num_fire >= 5 and not rel_time:
                    last_time = timer()
                    rel_time = True

    if not finish:
        window.blit(background, (0, 0))

        # Тексти
        score_text = font2.render("Рахунок: " + str(score), 1, (255, 255, 255))
        window.blit(score_text, (10, 20))

        lost_text = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(lost_text, (10, 50))

        life_text = font2.render("Життя: " + str(life), 1, (255, 255, 255))
        window.blit(life_text, (10, 80))

        # Оновлення об'єктів
        ship.update()
        ship.reset()

        monsters.update()
        monsters.draw(window)

        bullets.update()
        bullets.draw(window)

        hearts.update()
        hearts.draw(window)

        # Перезарядка
        if rel_time:
            now_time = timer()
            if now_time - last_time < 3:
                reload_text = font2.render("Триває перезарядка...", 1, (150, 0, 0))
                window.blit(reload_text, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        # Створення сердець (випадково)
        if randint(1, 200) == 1:
            heart = Heart(img_heart, randint(80, win_width - 80), -40, 40, 40, 2)
            hearts.add(heart)

        # Колізії
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            new_monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(new_monster)

        if sprite.spritecollide(ship, monsters, True):
            life -= 1

        if sprite.spritecollide(ship, hearts, True):
            if life < 3:
                life += 1

        # Перевірка виграшу/програшу
        if life == 0 or lost >= max_lost:
            finish = True
            lose_text = font2.render("Ви програли!", 1, (255, 0, 0))
            window.blit(lose_text, (250, 250))

        if score >= goal:
            finish = True
            win_text = font2.render("Ви виграли!", 1, (0, 255, 0))
            window.blit(win_text, (250, 250))

        display.update()
    clock.tick(FPS)












    level = 1
level_text = font2.render("Рівень: " + str(level), 1, (255, 255, 255))



def next_level():
    global level, goal, lost, life, finish, monsters
    level += 1
    goal += 10
    lost = 0
    life = 3
    finish = False
    monsters.empty()
    for i in range(5 + level):
        new_monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(2, 4 + level))
        monsters.add(new_monster)



level_text = font2.render("Рівень: " + str(level), 1, (255, 255, 255))
window.blit(level_text, (10, 110))



if score >= goal:
    finish = True
    win_text = font2.render("Ви виграли!", 1, (0, 255, 0))
    window.blit(win_text, (250, 250))



if score >= goal:
    win_text = font2.render("Рівень пройдено!", 1, (0, 255, 0))
    window.blit(win_text, (250, 250))
    display.update()
    time.delay(2000)
    next_level()