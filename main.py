import pygame
import sys
import os
import random

# константы
FPS = 10
WIDTH = 1280
HEIGHT = 720


def load_image(name, color_key=None):  # Загрузка картинок
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


# Группы спрайтов
all_sprite = pygame.sprite.Group()
level_sprite = pygame.sprite.Group()
monster_sprite = pygame.sprite.Group()
hero_sprire = pygame.sprite.Group()


# словарь спрайтов уровней
tile_images = {'flor': pygame.transform.scale(load_image('tile_set.png').subsurface(pygame.Rect((0, 0), (64, 64))),
                                              (64, 64)),
               'void': pygame.transform.scale(load_image('tile_set.png').subsurface(pygame.Rect((64, 0), (64, 64))),
                                              (64, 64)),
               'descent': pygame.transform.scale(load_image('tile_set.png').subsurface(pygame.Rect((0, 64), (64, 64))),
                                                 (64, 64)),
               'wall': pygame.transform.scale(load_image('tile_set.png').subsurface(pygame.Rect((64, 64), (64, 64))),
                                              (64, 64))}


# словарь с спрайтами монстров
monster_image = {'lvl1': load_image('lvl1.png'), 'lvl2': load_image('lvl2.png'), 'lvl3': load_image('lvl3.png')}
hero_image = load_image('hero.png')  # Спарайт героя


def terminate():  # выход
    pygame.quit()
    sys.exit()


def start_screen():  # Начальный экран
    intro_text = ["Добро пожаловать в подземелье",
                  "Передвижение: стрелочки",
                  'Атака: Z',
                  'Уклонение: X']
    fon = pygame.transform.scale(load_image('start screen.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 60)
    string_rendered = font.render(intro_text[0], 1, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 55
    intro_rect.x = 295
    screen.blit(string_rendered, intro_rect)
    font = pygame.font.Font(None, 40)
    text_coord = 600
    for line in intro_text[1:]:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()  # выход
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def win_screen():  # Экран по прохождению игры
    fon = pygame.transform.scale(load_image('win_screen.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 60)
    string_rendered = font.render('Поздравляю, Вы прошли игру!', 1, pygame.Color('white'))
    screen.blit(string_rendered, pygame.Rect(318, 100, 643, 42))
    string_rendered = font.render('Благодарю за прохождение игры!', 1, pygame.Color('white'))
    screen.blit(string_rendered, pygame.Rect(280, 152, 719, 42))
    pygame.mixer.music.load("data/win.mp3")
    pygame.mixer.music.play()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                terminate()  # выход
        pygame.display.flip()
        clock.tick(FPS)


def game_over_screen():  # Экран при смерти
    fon = pygame.transform.scale(load_image('game_over.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
    string_rendered = font.render('Нажмите любую кнопку для выхода.', 1, pygame.Color('white'))
    screen.blit(string_rendered, pygame.Rect(10, 685, 500, 28))
    pygame.mixer.music.load("data/game over.mp3")
    pygame.mixer.music.play()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                terminate()  # выход
        pygame.display.flip()
        clock.tick(FPS)


def render_hp(enemy, hero):  # отрисовка хп героя с врагом во время боя
    r = 256 // enemy.mx_hp
    for i in range(0, enemy.hp):
        screen.fill('green', (200 + i * r, 350, r - 1, 20))
    r = 256 // hero.mx_hp
    for i in range(0, hero.hp):
        screen.fill('green', (850 + i * r, 350, r - 1, 20))


def reward(lvl, time_group, hero):  # Повышение статуса после боя на выбор
    status = ['Status', f'Hp: {hero.mx_hp}', f'Attack: {hero.range_attack[0]}-{hero.range_attack[1]}',
              f'Healing: {hero.range_hp[0]}-{hero.range_hp[1]}']
    font = pygame.font.Font(None, 60)
    # рандомный выбор двух улучшений
    variants = {'Hp': int(lvl) * 2, 'Max healing': 1, "Max attack": 1}
    if (hero.range_attack[1] - hero.range_attack[0]) > 1:
        variants['Min attack'] = 1
    if (hero.range_hp[1] - hero.range_hp[0]) > 1:
        variants['Min healing'] = 1
    tmp = list(variants.keys())
    random.shuffle(tmp)
    variant1, variant2 = tmp[:2]
    hero.rect = pygame.Rect(300, 50, 512, 512)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()  # выход
            elif event.type == pygame.KEYDOWN and event.key == 122:  # если выбран первый вариант
                if variant1 == 'Hp':
                    hero.mx_hp += variants[variant1]
                    hero.hp = hero.mx_hp
                elif variant1 == 'Min attack':
                    hero.range_attack = (hero.range_attack[0] + 1, hero.range_attack[1])
                elif variant1 == 'Max attack':
                    hero.range_attack = (hero.range_attack[0], hero.range_attack[1] + 1)
                elif variant1 == 'Min healing':
                    hero.range_hp = (hero.range_hp[0] + 1, hero.range_hp[1])
                elif variant1 == 'Max healing':
                    hero.range_hp = (hero.range_hp[0], hero.range_hp[1] + 1)
                hero.rect = pygame.Rect(hero.pos_x * 64, hero.pos_y * 64, 64, 64)
                return
            elif event.type == pygame.KEYDOWN and event.key == 120:  # если выбран второй вариант
                if variant2 == 'Hp':
                    hero.mx_hp += variants[variant2]
                    hero.hp = hero.mx_hp
                elif variant2 == 'Min attack':
                    hero.range_attack = (hero.range_attack[0] + 1, hero.range_attack[1])
                elif variant2 == 'Max attack':
                    hero.range_attack = (hero.range_attack[0], hero.range_attack[1] + 1)
                elif variant2 == 'Min healing':
                    hero.range_hp = (hero.range_hp[0] + 1, hero.range_hp[1])
                elif variant2 == 'Max healing':
                    hero.range_hp = (hero.range_hp[0], hero.range_hp[1] + 1)
                hero.rect = pygame.Rect(hero.pos_x * 64, hero.pos_y * 64, 64, 64)
                return
        screen.fill((0, 0, 0))
        # вывод текста
        for i in range(len(status)):
            string_rendered = font.render(status[i], 1, pygame.Color('white'))
            screen.blit(string_rendered, pygame.Rect(50, 200 + 50 * i, *string_rendered.get_size()))
        string_rendered = font.render('Z: ' + variant1 + f': +{variants[variant1]}', 1, pygame.Color('white'))
        screen.blit(string_rendered, pygame.Rect(850, 250, *string_rendered.get_size()))
        string_rendered = font.render('X: ' + variant2 + f': +{variants[variant2]}', 1, pygame.Color('white'))
        screen.blit(string_rendered, pygame.Rect(850, 350, *string_rendered.get_size()))
        string_rendered = font.render('Выберите улучшение', 1, pygame.Color('white'))
        screen.blit(string_rendered, pygame.Rect(800, 150, *string_rendered.get_size()))
        # отрисовка спрайта героя
        time_group.update(512)
        time_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def battle(lvl):  # Бой
    for i in monster_sprite:  # определение врага на которого нападаем
        if pygame.sprite.collide_mask(hero, i):
            enemy = i
            break
    # создаётся группа на время боя
    time_group = pygame.sprite.Group()
    time_group.add(enemy)
    time_group.add(hero)
    enemy.rect = pygame.Rect(200, 400, 256, 256)
    hero.rect = pygame.Rect(850, 400, 256, 256)
    hero.direction = -1
    hero_attack = True
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()  # выход
            elif event.type == pygame.KEYDOWN and event.key == 122 and hero_attack:
                hero.attack(time_group, enemy)
                hero_attack = False
            elif event.type == pygame.KEYDOWN and event.key == 120 and hero_attack:
                hero.evasion(time_group, enemy)
                hero_attack = False
        screen.fill((0, 0, 0))
        time_group.update(256)
        time_group.draw(screen)
        render_hp(enemy, hero)
        if enemy.hp <= 0:  # Если враг побежден
            enemy.dead(time_group)
            enemy.kill()
            hero.hp = hero.mx_hp
            return reward(lvl, time_group, hero)
        if hero.hp <= 0:  # Если герой проигрывает
            hero.dead(time_group)
            return game_over_screen()
        if not hero_attack:  # Ход врага
            enemy.attack(time_group, hero)
            hero_attack = True
        # иначе бездействуем пока игрок не походит
        pygame.display.flip()
        clock.tick(FPS)


def load_levels():
    # Загрузка уровней
    with open('data/levels.txt') as file:
        lines = [line.strip() for line in file]
    levels = []
    level = []
    for line in lines:
        if line == '':
            levels.append(level)
            level = []
        else:
            level += [line]
    levels.append(level)
    return levels


def draw_level(number_level, hero=None):  # отрисовка уровня
    for i in range(len(levels[number_level])):
        for j in range(len(levels[number_level][i])):
            if levels[number_level][i][j] == '.':
                Tile('flor', i, j)
            elif levels[number_level][i][j] == '~':
                Tile('void', i, j)
            elif levels[number_level][i][j] == 's':
                Tile('descent', i, j)
            elif levels[number_level][i][j] == '#':
                Tile('wall', i, j)
            elif levels[number_level][i][j] == 'n':
                Tile('flor', i, j)
                if hero:
                    hero.rect = pygame.Rect(i * 64, j * 64, 64, 64)
                    hero.map_level = list(map(list, levels[number_level]))
                    hero.pos_x = i
                    hero.pos_y = j
                else:
                    hero = Hero(i, j, levels[number_level])
            elif levels[number_level][i][j].isdigit():
                Tile('flor', i, j)
                Monster(levels[number_level][i][j], i, j)
    return hero


def next_level():  # переход на следующий уровень
    global number_level, hero
    number_level += 1
    if number_level >= len(levels):
        return win_screen()
    for i in all_sprite:
        i.kill()
    hero = draw_level(number_level, hero)


class Tile(pygame.sprite.Sprite):  # класс тукстуры уровня
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(level_sprite, all_sprite)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(64 * pos_x, 64 * pos_y)


class Monster(pygame.sprite.Sprite):  # класс монстра
    def __init__(self, lvl, pos_x, pos_y):
        super().__init__(monster_sprite, all_sprite)
        self.frames_idle = []
        self.frames_attack = []
        self.frames_dead = []
        lvl = 'lvl' + lvl
        self.cut_sheet(lvl)
        self.cur_frame = 0
        self.rect = pygame.Rect(0, 0, 64, 64)
        self.image = self.frames_idle[self.cur_frame]
        self.rect = self.rect.move(64 * pos_x, 64 * pos_y)
        self.mx_hp = 10 * int(lvl[-1])
        self.hp = 10 * int(lvl[-1])
        self.range_attack = (1 + int(lvl[-1]), 3 * int(lvl[-1]))

    def cut_sheet(self, lvl):  # нарезка спрайтов
        for i in range(5 if lvl == 'lvl1' else 4):
            self.frames_idle += [monster_image[lvl].subsurface(pygame.Rect((64 * i, 0), (64, 64)))]
        for i in range(8):
            self.frames_dead += [pygame.transform.scale(monster_image[lvl].subsurface(pygame.Rect(
                (64 * i, 128 if lvl == 'lvl1' else 192), (64, 64))), (256, 256))]
        for i in range([5, 4, 6][int(lvl[-1]) - 1]):
            self.frames_attack += [pygame.transform.scale(monster_image[lvl].subsurface(pygame.Rect(
                (64 * i, 64 if lvl == 'lvl1' else 128), (64, 64))), (256, 256))]

    def update(self, n=0):  # обновление при бездействии
        self.cur_frame = (self.cur_frame + 1) % len(self.frames_idle)
        self.image = self.frames_idle[self.cur_frame]
        if n:
            self.image = pygame.transform.scale(self.image, (n, n))

    def dead(self, time_group):  # анимация смерти
        for i in range(len(self.frames_dead)):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()  # выход
            screen.fill((0, 0, 0))
            time_group.update(256)
            self.image = self.frames_dead[i]
            time_group.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)

    def attack(self, time_group, hero):  # анимация атаки
        for i in range(len(self.frames_attack)):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()  # выход
            screen.fill((0, 0, 0))
            render_hp(self, hero)
            time_group.update(256)
            self.image = self.frames_attack[i]
            time_group.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)
        hero.hp -= int((random.randint(*self.range_attack) * (2 if 1 == random.choice(range(20)) else 1)) *
                       (0.9 if hero.invulnerability else 1))
        hero.invulnerability = False


class Hero(pygame.sprite.Sprite):  # класс героя
    def __init__(self, pos_x, pos_y, map_level):
        super().__init__(hero_sprire)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.map_level = list(map(list, map_level))
        self.frames_idle = []
        self.frames_attacks = []
        self.frames_dead = []
        self.frames_evasion = []
        self.cut_sheet(hero_image)
        self.cur_frame = 0
        self.rect = pygame.Rect(0, 0, 64, 64)
        self.image = self.frames_idle[self.cur_frame]
        self.rect = self.rect.move(64 * pos_x, 64 * pos_y)
        self.direction = 1
        self.mx_hp = 20
        self.hp = 20
        self.range_hp = (1, 3)
        self.range_attack = (3, 5)
        self.invulnerability = False

    def cut_sheet(self, image):  # нарезка спрайтов
        for i in range(4):
            self.frames_idle += [image.subsurface(pygame.Rect((64 * i, 0), (64, 64)))]
        for i in range(7):
            self.frames_dead += [pygame.transform.flip(pygame.transform.scale(
                image.subsurface(pygame.Rect((64 * i, 256), (64, 64))), (256, 256)), True, False)]
        for x in range(3):
            tmp = []
            for i in range([6, 8, 6][x]):
                tmp += [pygame.transform.flip(pygame.transform.scale(image.subsurface(
                    pygame.Rect((64 * i, [704, 768, 960][x]), (64, 64))), (256, 256)), True, False)]
            self.frames_attacks.append(tmp)
        for i in range(10):
            self.frames_evasion += [pygame.transform.flip(pygame.transform.scale(
                image.subsurface(pygame.Rect((64 * i, 192), (64, 64))), (256, 256)), True, False)]

    def update(self, n=0):  # обновление при бездействии
        self.cur_frame = (self.cur_frame + 1) % len(self.frames_idle)
        self.image = self.frames_idle[self.cur_frame]
        if self.direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        if n:
            self.image = pygame.transform.scale(self.image, (n, n))

    def move(self, x, y):  # передвижение
        i = x + self.pos_x
        j = y + self.pos_y
        if self.map_level[i][j] not in '~#':
            if x != 0:
                self.direction = x
            self.rect = self.rect.move(x * 64, y * 64)
            self.pos_x += x
            self.pos_y += y
            if self.map_level[i][j] == 's':
                next_level()  # Переход на следующий уровень
            elif self.map_level[i][j].isdigit():
                battle(self.map_level[i][j])  # Запуск боя с монстром
                self.map_level[i][j] = '.'

    def dead(self, time_group):  # анимация смерти
        for i in range(len(self.frames_dead)):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()  # выход
            screen.fill((0, 0, 0))
            time_group.update(256)
            self.image = self.frames_dead[i]
            time_group.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)

    def attack(self, time_group, enemy):  # анимация атаки
        # выбор одной из анимаций атаки
        attack = random.choice(self.frames_attacks)
        for i in range(len(attack)):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()  # выход
            screen.fill((0, 0, 0))
            render_hp(enemy, self)
            time_group.update(256)
            self.image = attack[i]
            time_group.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)
        enemy.hp -= random.randint(*self.range_attack) * (2 if 1 == random.choice(range(20)) else 1)

    def evasion(self, time_group, enemy):  # анимация уворота
        if self.hp > self.mx_hp:
            self.hp = self.mx_hp
        for i in range(len(self.frames_evasion)):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()  # выход
            screen.fill((0, 0, 0))
            render_hp(enemy, self)
            time_group.update(256)
            self.image = self.frames_evasion[i]
            time_group.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)
        self.invulnerability = True
        self.hp += random.randint(*self.range_hp)


if __name__ == '__main__':  # запуск
    pygame.init()
    pygame.display.set_caption('Pygame')
    size = width, height = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    # включение музыки
    pygame.mixer.music.load("data/background.mp3")
    pygame.mixer.music.play(-1)
    start_screen()  # Заставка
    levels = load_levels()  # Загрузка карты уровней
    number_level = 0  # номер уровня
    hero = draw_level(number_level)  # Отрисовка уровня
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()  # выход
            # управление
            if event.type == pygame.KEYDOWN and event.scancode == 79:
                hero.move(1, 0)
            if event.type == pygame.KEYDOWN and event.scancode == 80:
                hero.move(-1, 0)
            if event.type == pygame.KEYDOWN and event.scancode == 81:
                hero.move(0, 1)
            if event.type == pygame.KEYDOWN and event.scancode == 82:
                hero.move(0, -1)
        screen.fill((0, 0, 0))
        # Отрисовка спрайтов
        monster_sprite.update()
        hero_sprire.update()
        level_sprite.draw(screen)
        monster_sprite.draw(screen)
        hero_sprire.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
