import pygame
import sys
import random
import time

pygame.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RPG Битва")

FONT = pygame.font.SysFont(None, 32)
SMALL_FONT = pygame.font.SysFont(None, 24)
BIG_FONT = pygame.font.SysFont(None, 64)

BLUE = (135, 206, 250)
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
ORANGE = (255, 165, 0)
RED = (200, 0, 0)

money = 100
difficulty = "easy"
enemy_hp = 150
enemy_damage = 20

state = "menu"
round_num = 1
last_attack_time = time.time()

# Змінні для атаки й анімації
attacker = None
defender = None
attack_phase = 0  # 0 - ні атаки, 1 - рух до противника, 2 - рух назад
attack_cooldown = 1.5



class Character:
    def __init__(self, name, image_path, x, y):
        self.name = name
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (90, 90))
        self.x = x
        self.y = y
        self.base_x = x
        self.base_y = y
        self.hp = 150
        self.base_hp = 150
        self.damage = 20
        self.level = 0

        self.target_pos = None
        self.is_moving = False
        self.move_speed = 12  # швидкість руху (пікселів за кадр)

    def upgrade(self):
        global money
        if money >= 50:
            self.base_hp += 15
            self.damage += 2
            self.hp = self.base_hp
            self.level += 1
            money -= 50

    def is_alive(self):
        return self.hp > 0

    def attack(self, target):
        target.hp -= self.damage

    def draw(self):
        screen.blit(self.image, (self.x, self.y))
        text = FONT.render(f"{self.name} ({int(self.hp)})", True, BLACK)
        screen.blit(text, (self.x, self.y + 90))

    def is_clicked(self, pos):
        return pygame.Rect(self.x, self.y, 60, 60).collidepoint(pos)

    def start_move(self, target_x, target_y):
        self.target_pos = (target_x, target_y)
        self.is_moving = True

    def update_position(self):
        if not self.is_moving or self.target_pos is None:
            return True  # рух неактивний - вважаємо рух завершеним

        dx = self.target_pos[0] - self.x
        dy = self.target_pos[1] - self.y
        dist = (dx ** 2 + dy ** 2) ** 0.5

        if dist < self.move_speed:
            # Досягли точки призначення
            self.x, self.y = self.target_pos
            self.is_moving = False
            self.target_pos = None
            return True
        else:
            # Рухаємося у напрямку цілі
            self.x += self.move_speed * dx / dist
            self.y += self.move_speed * dy / dist
            return False

    def return_to_base(self):
        self.start_move(self.base_x, self.base_y)


class Button:
    def __init__(self, text, x, y, w, h, action):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.action = action

    def draw(self):
        pygame.draw.rect(screen, BROWN, self.rect)
        txt = FONT.render(self.text, True, BLACK)
        screen.blit(txt, (self.rect.x + 10, self.rect.y + 10))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

buttons = [
    Button("Вибрати персонажів", 400, 200, 260, 50, "select"),
    Button("Прокачати персонажів", 400, 300, 260, 50, "upgrade"),
    Button("Вибрати складність", 400, 400, 260, 50, "difficulty")
]

available_heroes = [
    Character("Людина", "human.png", 100, 110),
    Character("Воїн", "warrior.png", 250, 110),
    Character("Лікар", "medic.png", 400, 110),
    Character("Маг", "mage.png", 550, 110),
    Character("Боксер", "boxer.png", 700, 110)
]

selected_heroes = []

enemies = [
    Character("Павук", "spider.png", 200, 260),
    Character("Гоблін", "goblin.png", 300, 260),
    Character("Робот", "robot.png", 400, 260)
]

def draw_money():
    txt = FONT.render(f"💰 {money}", True, BLACK)
    screen.blit(txt, (WIDTH - 120, 20))

def get_difficulty_color(diff):
    return {
        "easy": GREEN,
        "normal": ORANGE,
        "hard": RED
    }.get(diff, BLACK)

def main_menu():
    screen.fill(BLUE)
    for b in buttons:
        b.draw()

    diff_color = get_difficulty_color(difficulty)
    diff_text = FONT.render(f"Складність: {difficulty}", True, diff_color)
    screen.blit(diff_text, (430, 460))

    draw_money()
    pygame.display.flip()

def draw_select_screen():
    screen.fill(BLUE)
    txt = BIG_FONT.render("Вибери 3 героїв", True, BLACK)
    screen.blit(txt, (300, 30))

    for hero in available_heroes:
        hero.draw()

    for h in selected_heroes:
        pygame.draw.rect(screen, GREEN, (h.x, h.y - 10, 60, 5))

    back = FONT.render("Натисни B щоб повернутись", True, BLACK)
    screen.blit(back, (300, 600))
    pygame.display.flip()

def draw_upgrade_screen():
    screen.fill(BLUE)
    txt = BIG_FONT.render("Клікни на героя, щоб прокачати", True, BLACK)
    screen.blit(txt, (250, 30))
    for hero in selected_heroes:
        hero.draw()
        lvl_text = FONT.render(f"Lvl: {hero.level}", True, BLACK)
        screen.blit(lvl_text, (hero.x, hero.y - 20))

    back = FONT.render("Натисни B щоб повернутись", True, BLACK)
    screen.blit(back, (300, 600))
    draw_money()
    pygame.display.flip()

def setup_positions():
    hero_x = 50
    hero_start_y = 155
    hero_spacing_y = 110
    for idx, h in enumerate(selected_heroes):
        h.x = hero_x
        h.y = hero_start_y + idx * hero_spacing_y
        h.base_x = h.x
        h.base_y = h.y
        h.is_moving = False
        h.target_pos = None

    enemy_x = WIDTH - 110
    enemy_start_y = 150
    enemy_spacing_y = 110
    for idx, e in enumerate(enemies):
        e.x = enemy_x
        e.y = enemy_start_y + idx * enemy_spacing_y
        e.base_x = e.x
        e.base_y = e.y
        e.is_moving = False
        e.target_pos = None

turn = "enemy"  # або "hero" залежно від того, хто починає

def battle():
    global round_num, last_attack_time
    global attacker, defender, attack_phase, turn  # <--- додаємо turn сюди

    screen.fill(BLUE)

    round_text = FONT.render(f"Раунд {round_num}/15", True, BLACK)
    screen.blit(round_text, (450, 30))

    draw_money()

    # Малюємо героїв
    for h in selected_heroes:
        if h.is_alive():
            if h.is_moving:
                finished = h.update_position()
                if finished and attack_phase == 2 and h == attacker:
                    attacker = None
                    defender = None
                    attack_phase = 0

            text = SMALL_FONT.render(f"{h.name} ({int(h.hp)})", True, BLACK)
            screen.blit(text, (h.x, h.y - 20))
            screen.blit(h.image, (h.x, h.y))

    # Малюємо ворогів
    for e in enemies:
        if e.is_alive():
            if e.is_moving:
                finished = e.update_position()
                if finished and attack_phase == 2 and e == attacker:
                    attacker = None
                    defender = None
                    attack_phase = 0

            text = SMALL_FONT.render(f"{e.name} ({int(e.hp)})", True, BLACK)
            screen.blit(text, (e.x, e.y - 20))
            screen.blit(e.image, (e.x, e.y))

    # Логіка атаки
    current_time = time.time()
    ##############################################
    global turn
    if attack_phase == 0 and current_time - last_attack_time > attack_cooldown:
        alive_heroes = [h for h in selected_heroes if h.is_alive()]
        alive_enemies = [e for e in enemies if e.is_alive()]
        if alive_heroes and alive_enemies:
            if turn == "hero": 
                attacker = random.choice(alive_heroes)
                defender = random.choice(alive_enemies)
                attacker.start_move(defender.x - 50, defender.y)
            else:  # enemy
                attacker = random.choice(alive_enemies)
                defender = random.choice(alive_heroes)
                attacker.start_move(defender.x + 50, defender.y)
            attack_phase = 1

    elif attack_phase == 1:
        # Рух до противника
        if attacker.update_position():  # повертає True, якщо досягли цілі
            # Наносимо шкоду
            defender.hp -= attacker.damage
            if defender.hp < 0:
                defender.hp = 0
            # Починаємо рух назад
            attacker.return_to_base()
            attack_phase = 2

    elif attack_phase == 2:
        # Рух назад
        if attacker.update_position():  # повернулися на базу
            attack_phase = 0
            last_attack_time = time.time()
            attacker = None
            defender = None
            # Перемикаємо чергу
            turn = "hero" if turn == "enemy" else "enemy"
            
        # Якщо противник вмер, перевіряємо кінець бою
        alive_heroes = [h for h in selected_heroes if h.is_alive()]
        alive_enemies = [e for e in enemies if e.is_alive()]
        if not alive_heroes or not alive_enemies:
            round_num += 1
            if round_num > 15:
                print("Бій завершено!")
                pygame.quit()
                sys.exit()
            else:
                # Починаємо новий раунд, оновлюємо життя ворогів та героїв, позиції
                setup_positions()
                for h in selected_heroes:
                    h.hp = h.base_hp
                for e in enemies:
                    e.hp = enemy_hp
                last_attack_time = time.time()
                attack_phase = 0
                attacker = None
                defender = None
    ###############################################################
    pygame.display.flip()


def handle_menu_click(pos):
    global state, difficulty, enemy_hp, enemy_damage, round_num, attack_phase, attacker, defender
    for b in buttons:
        if b.is_clicked(pos):
            if b.action == "select":
                state = "select"
            elif b.action == "upgrade":
                state = "upgrade"
            elif b.action == "difficulty":
                if difficulty == "easy":
                    difficulty = "normal"
                    enemy_hp = 250
                    enemy_damage = 30
                elif difficulty == "normal":
                    difficulty = "hard"
                    enemy_hp = 300
                    enemy_damage = 45
                else:
                    difficulty = "easy"
                    enemy_hp = 150
                    enemy_damage = 20
                for e in enemies:
                    e.hp = enemy_hp
                    e.damage = enemy_damage
                print(f"Складність: {difficulty}")

clock = pygame.time.Clock()

while True:
    if state == "menu":
        main_menu()
    elif state == "battle":
        battle()
    elif state == "select":
        draw_select_screen()
    elif state == "upgrade":
        draw_upgrade_screen()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if state == "menu":
                handle_menu_click(event.pos)
            elif state == "select":
                for hero in available_heroes:
                    if hero.is_clicked(event.pos) and hero not in selected_heroes:
                        if len(selected_heroes) < 3:
                            selected_heroes.append(hero)
            elif state == "upgrade":
                for hero in selected_heroes:
                    if hero.is_clicked(event.pos):
                        hero.upgrade()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and state == "menu":
                if selected_heroes:
                    setup_positions()
                    round_num = 1
                    attack_phase = 0
                    attacker = None
                    defender = None
                    state = "battle"
            elif event.key == pygame.K_b and state in ["select", "upgrade"]:
                state = "menu"

    clock.tick(60)
