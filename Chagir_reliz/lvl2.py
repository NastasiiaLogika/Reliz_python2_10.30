from pygame import *
'''Необхідні класи'''


# клас-батько для спрайтів
class GameSprite(sprite.Sprite):
    # конструктор класу
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        # кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        # кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y


    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


# клас-спадкоємець для спрайту-гравця (керується стрілками)
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

        



# клас-спадкоємець для спрайта-ворога (переміщається сам)
class Enemy(GameSprite):
    direction = "left"


    def update(self):
        if self.rect.x <= 250:
            self.direction = "right"
        if self.rect.x >= win_width - 85:
            self.direction = "left"


        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed


# клас для спрайтів-перешкод
class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        # картинка стіни - прямокутник потрібних розмірів та кольору
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        # кожен спрайт повинен зберігати властивість rect - прямокутник
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y


    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))



# Ігрова сцена:
win_width = 700
win_height = 500


window = display.set_mode((win_width, win_height))
display.set_caption("Maze")
background = transform.scale(image.load(
    "backgroundlvl2.png"), (win_width, win_height))


# Персонажі гри:
player = Player('sprite1.png', 600, win_height - 90, 5)
monster = Enemy('sprite3.png', win_width - 80, 280, 2)
final = GameSprite('treasure.png', win_width - 650, win_height - 80, 0)


#стіни
w1 = Wall(154, 205, 50, 80, 480, 600, 10) #верхня 
w2 = Wall(154, 205, 50, 50, 50, 700, 10)
w3 = Wall(154, 205, 50, 50, 50, 10, 300)
w4 = Wall(154, 205, 50, 150, 180, 10, 300) 
w5 = Wall(154, 205, 50, 150, 180, 100, 10) 
w6 = Wall(154, 205, 50, 250, 180, 10, 200)
w7 = Wall(154, 205, 50, 350, 50, 10, 300)
w8 = Wall(154, 205, 50, 350, 350, 100, 10)
w9 = Wall(154, 205, 50, 450, 200, 150, 10)
w10 = Wall(154, 205, 50, 550, 200, 10, 300)

# написи
font.init()
font = font.Font(None, 70)
win = font.render('YOU WIN!', True, (255, 215, 0))
lose = font.render('YOU LOSE!', True, (180, 0, 0))



game = True
finish = False
clock = time.Clock()
FPS = 60


# # музика
# mixer.init()
# mixer.music.load('jungles.ogg')
# mixer.music.play()


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False


    if finish != True:
        window.blit(background, (0, 0))
        player.update()
        monster.update()


        player.reset()
        monster.reset()
        final.reset()
        
        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
        w4.draw_wall()
        w5.draw_wall()
        w6.draw_wall()
        w7.draw_wall()
        w8.draw_wall()
        w9.draw_wall()
        w10.draw_wall()
        
        # Ситуація "Програш"
    if (sprite.collide_rect(player, monster) or 
        sprite.collide_rect(player, w1) or 
        sprite.collide_rect(player, w2) or 
        sprite.collide_rect(player, w3) or 
        sprite.collide_rect(player, w4) or 
        sprite.collide_rect(player, w5) or 
        sprite.collide_rect(player, w6) or 
        sprite.collide_rect(player, w7) or 
        sprite.collide_rect(player, w8) or 
        sprite.collide_rect(player, w9) or 
        sprite.collide_rect(player, w10)): 
        finish = True
        window.blit(lose, (200, 200))
        


    # Ситуація "Перемога"
    if sprite.collide_rect(player, final):
        finish = True
        window.blit(win, (200, 200))

        display.update()
        time.display(3000)
        import subprocess
        subprocess.run(["pyton", "lvl3.py"])
        game = False




    display.update()
    clock.tick(FPS)
