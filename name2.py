import pygame as pg
import pygame
import os
import sys
import random
all_sprites = pygame.sprite.Group()
all_spritess = pygame.sprite.Group()
clock = pygame.time.Clock()
pygame.init()
size = width, height = 700, 300
screen = pygame.display.set_mode(size)
x1, y1, x2, y2 = 100, 200, 600, 200
gg = 0
activno = None
screen_rect = (0, 0, width, height)
GRAVITY = 3
stop = False
win_round1, win_round2 = 0, 0
zvyk_ydara = pg.mixer.Sound('data\ydar.mp3')
pg.mixer.music.load('data\music_bitva.mp3')
pygame.mixer.music.play(-1, 0.0)

def povorot(name, r):
    if r:
        return pygame.transform.flip(load_image(name), True, False)
    else:
        return load_image(name)


def razvorot(r):
    ninjarun = AnimatedSprite(povorot("run.png", r), 6, 1, 0, 0)
    ninjastay = AnimatedSprite(povorot("stay.png", r), 1, 1, 0, 0)
    ninjahm = AnimatedSprite(povorot("handmedium.png", r), 1, 1, 0, 0)
    ninjahh = AnimatedSprite(povorot("handhigh.png", r), 1, 1, 0, 0)
    ninjasit = AnimatedSprite(povorot("sit.png", r), 1, 1, 0, 0)
    ninjasithandmedium = AnimatedSprite(povorot("sithandmedium.png", r), 1, 1, 0, 0)
    ninjajump = AnimatedSprite(povorot("jump.png", r), 5, 1, 0, 0)
    ninjadeafened = AnimatedSprite(povorot("deafened.png", r), 1, 1, 0, 0)
    return ninjarun, ninjastay, ninjahm, ninjahh, ninjasit, ninjasithandmedium, ninjajump, ninjadeafened


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    firee = [load_image("star.png")]
    fire = []
    for scale in (10, 15):
        fire.append(pygame.transform.scale(firee[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = GRAVITY

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()

def create_particles(position):
    # количество создаваемых частиц
    particle_count = 10
    # возможные скорости
    numbers = range(-1, 10)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_spritess)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def otris(self, reverse, kadrov, animCount):
        global gg
        if animCount + 1 >= 30:
            animCount = 0
            gg = 0
        if reverse:
            gg = len(self.frames) + -1 * animCount // kadrov
        else:
            if animCount // kadrov != gg:
                gg = animCount // kadrov
        animCount += 1
        if gg > len(self.frames) - 1:
            gg = 0
        return self.frames[gg], animCount


class G_Player(pygame.sprite.Sprite):
    imagestay = load_image('stay.png')
    tipi_ydarov = {'hm': '7', 'hh': '10', 'shm': '5'}

    def __init__(self, pos, left):
        super().__init__(all_sprites)
        self.image = G_Player.imagestay
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.otkat = 0
        self.otkatjump = 0
        self.protivnik = None
        self.activno = None
        self.left = left
        self.animCount = 0
        self.posledni_deistvia = []
        self.ydar = False
        self.healts = 7
        self.run1, self.run2, self.handhigh, self.handmedium, self.runA_I, self.sitt, self.handmediumA_I, self.jump,\
        self.activnosti, self.deafened = False, False, False, False, False, False, False, False, False, False
        self.ninjarun, self.ninjastay, self.ninjahm, self.ninjahh, self.ninjasit, self.ninjasithandmedium,\
        self.ninjajump, self.ninjadeafened = razvorot(self.left)

    def start_fight(self, pos, left):
        self.left = left
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.image = G_Player.imagestay
        self.run1, self.run2, self.handhigh, self.handmedium, self.runA_I, self.sitt, self.handmediumA_I, self.jump, \
        self.activnosti, self.deafened = False, False, False, False, False, False, False, False, False, False
        self.animCount = 0
        self.ydar = False
        self.healts = 7

    def obmen(self):
        player1.ninjarun, player1.ninjastay, player1.ninjahm, player1.ninjahh, player1.ninjasit,\
        player1.ninjasithandmedium, player1.ninjajump, player1.ninjadeafened, player2.ninjarun, player2.ninjastay, player2.ninjahm,\
        player2.ninjahh, player2.ninjasit, player2.ninjasithandmedium, player2.ninjajump, player2.ninjadeafened = player2.ninjarun,\
        player2.ninjastay, player2.ninjahm, player2.ninjahh, player2.ninjasit, player2.ninjasithandmedium,\
        player2.ninjajump, player2.ninjadeafened, player1.ninjarun, player1.ninjastay, player1.ninjahm, player1.ninjahh, player1.ninjasit,\
        player1.ninjasithandmedium, player1.ninjajump, player1.ninjadeafened

    def set_protivnik(self, protivnik):
        self.protivnik = protivnik

    def A_I(self):
        if len(self.posledni_deistvia) > 4:
            self.posledni_deistvia.pop(0)
        if player2.otkat - 5 <= 0:
            if player1.rect.x + 10 < player2.rect.x:
                pass
                player2.ninja_run(True)
            elif player1.rect.x - 10 > player2.rect.x:
                player2.ninja_run(False)
            else:
                player2.ninja_stay()
        if player2.otkat == 0:
            if self.left:
                if 20 >= self.rect.x - player1.rect.x > 0 and self.posledni_deistvia.count('hh') != 3:
                    player2.player_handhigh()
                    self.posledni_deistvia.append('hh')
                elif 40 >= self.rect.x - player1.rect.x > 0 and self.posledni_deistvia.count('hm') != 3:
                    player2.player_handmedium()
                    self.posledni_deistvia.append('hm')
            else:
                if 20 >= player1.rect.x - self.rect.x > 0 and self.posledni_deistvia.count('hh') != 3:
                    player2.player_handhigh()
                    self.posledni_deistvia.append('hh')
                elif 40 >= player1.rect.x - self.rect.x > 0 and self.posledni_deistvia.count('hm') != 3:
                    player2.player_handmedium()
                    self.posledni_deistvia.append('hm')
        else:
            player2.otkat -= 1

    def ninja_deafened(self):
        self.handhigh, self.handmedium, self.jump = False, False, False
        self.image, self.animCount = self.ninjadeafened.otris(False, 30, self.animCount)
        if self.animCount == 4:
            self.rect = self.rect.move(40 * - 1 if not self.left else 40, 0)
        if self.animCount >= 6:
            self.deafened = False
            self.ninja_stay()

    def ninja_run(self, reverse):
        self.image, self.animCount = self.ninjarun.otris(reverse, 5, self.animCount)
        if reverse:
            self.rect = self.rect.move(-5, 0)
        else:
            self.rect = self.rect.move(5, 0)
        if player1.rect.x > player2.rect.x and player1.left is False and player2.left is True and not player1.jump:
            player1.left = True
            player2.left = False
            self.obmen()
        if player1.rect.x < player2.rect.x and player1.left is True and player2.left is False and not player1.jump:
            player1.left = False
            player2.left = True
            self.obmen()

    def ninja_handmedium(self):
        if self.left and self.animCount == 1:
            self.rect.x -= 35
        self.image, self.animCount = self.ninjahm.otris(False, 30, self.animCount)
        if self.animCount >= 20:
            self.handmedium = False
            self.ydar = False
            if self.left:
                self.rect.x += 35
            self.ninja_stay()
        self.chastici('hm')

    def chastici(self, tip_ydara):
        if pygame.sprite.collide_mask(self, self.protivnik) and not self.ydar:
            ydvaenie = 1
            if random.randint(0, 100) <= 10:
                create_particles((self.protivnik.rect.x + 10, self.protivnik.rect.y))
                ydvaenie = 2
            self.ydar = True
            self.protivnik.healts -= int(self.tipi_ydarov[tip_ydara]) * ydvaenie
            self.protivnik.deafened = True
            zvyk_ydara.play()
            self.protivnik.ninja_deafened()

    def ninja_handmhigh(self):
        if self.left and self.animCount == 1:
            self.rect.x -= 35
        self.image, self.animCount = self.ninjahh.otris(False, 30, self.animCount)
        if self.animCount >= 20 or self.sitt:
            self.handhigh = False
            self.ydar = False
            if self.left:
                self.rect.x += 35
            self.ninja_stay()
        self.chastici('hh')

    def ninja_sithandmedium(self):
        if self.left and self.animCount == 1:
            self.rect.x -= 35
        self.image, self.animCount = self.ninjasithandmedium.otris(False, 30, self.animCount)
        if self.animCount >= 20:
            self.handmedium = False
            self.sitt = True
            self.ydar = False
            if self.left:
                self.rect.x += 35
            self.ninja_sit()
        self.chastici('shm')

    def ninja_stay(self):
        self.animCount = 0
        self.image, self.animCount = self.ninjastay.otris(False, 30, self.animCount)
        self.animCount = 0
        self.activnosti = False

    def ninja_sit(self):
        self.activnosti = True
        self.image, self.animCount = self.ninjasit.otris(False, 30, self.animCount)
        self.activnosti = True

    def ninja_jump(self):
        if self.left:
            self.rect = self.rect.move(-10, 0)
            self.image, self.animCount = self.ninjajump.otris(True, 6, self.animCount)
        else:
            self.rect = self.rect.move(10, 0)
            self.image, self.animCount = self.ninjajump.otris(False, 6, self.animCount)
        if self.animCount // 5 in [1, 2]:
            self.rect = self.rect.move(0, -10)
        if self.animCount // 5 in [3, 4]:
            self.rect = self.rect.move(0, 10)
        if self.animCount + 1 >= 30:
            self.jump = False
            self.animCount = 0
            self.ninja_stay()
            if player1.rect.x > player2.rect.x and player1.left is False and player2.left is True:
                player1.left = True
                player2.left = False
                self.obmen()
            if player1.rect.x < player2.rect.x and player1.left is True and player2.left is False:
                player1.left = False
                player2.left = True
                self.obmen()
            self.ninja_stay()

    def player_jump(self):
        self.animCount = 0
        self.jump = True
        self.activnosti = True
        self.otkatjump = 120
        self.otkat = 50

    def player_sit(self):
        self.handhigh = False
        self.sitt = True
        self.jump = False
        self.activnosti = True
        self.otkat = 30
        self.ninja_sit()

    def player_handmedium(self):
        self.animCount = 0
        self.handmedium = True
        self.activnosti = True
        self.otkat = 60

    def player_handhigh(self):
        self.animCount = 0
        self.handhigh = True
        self.activnosti = True
        self.otkat = 80

    def player_dont_sit(self):
        self.sitt = False
        self.jump = False
        self.handhigh = False
        self.activnosti = False
        self.ninja_stay()

    def update(self):
        global col, otkat, stop
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x + 70 > 700:
            self.rect.x = 630
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and not player1.activnosti:
                player1.ninja_run(True)
            if event.key == pygame.K_RIGHT and not player1.activnosti:
                player1.ninja_run(False)
            if player1.otkat == 0:
                if event.key == pygame.K_UP and not player1.activnosti and self.otkatjump == 0:
                    player1.player_jump()
                if event.key == pygame.K_DOWN and not player1.activnosti:
                    player1.player_sit()
                if event.key == pygame.K_KP1 and player1.activnosti and self.sitt and not self.jump or event.key == pygame.K_KP1 and not self.activnosti:
                    player1.player_handmedium()
                if event.key == pygame.K_KP3 and not player1.activnosti and not self.sitt:
                    player1.player_handhigh()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and not player1.activnosti:
                player1.ninja_stay()
            if event.key == pygame.K_RIGHT and not player1.activnosti:
                player1.ninja_stay()
            if event.key == pygame.K_UP:
                pass
            if player1.otkat == 0:
                if event.key == pygame.K_DOWN:
                    player1.player_dont_sit()
        if player1.otkat > 0:
            player1.otkat -= 1
        if player1.otkatjump > 0:
            player1.otkatjump -= 1
        if self.sitt:
            if self.handmedium:
                self.ninja_sithandmedium()
            else:
                self.ninja_sit()
        elif self.deafened:
            self.ninja_deafened()
        elif player1.jump:
            player1.ninja_jump()
        elif self.handmedium:
            self.ninja_handmedium()
        elif self.handhigh:
            self.ninja_handmhigh()
        self.mask = pygame.mask.from_surface(self.image)


if __name__ == '__main__':
    running = True
    player1, player2 = G_Player((x1, y1), False), G_Player((x2, y2), True)
    player1.set_protivnik(player2)
    player2.set_protivnik(player1)
    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if player1.healts <= 0:
            stop = True
            win_round2 += 1
        if player2.healts <= 0:
            stop = True
            win_round1 += 1
        if stop and win_round1 != 2 and win_round2 != 2:
            stop = False
            player2.start_fight((x2, y2), True), player1.start_fight((x1, y1), False)
        else:
            if win_round2 == 2:
                print('lose')
                running = False
            if win_round1 == 2:
                print('won')
                running = False
        player2.A_I()
        all_sprites.update()
        screen.blit(fon, (0, 0))
        all_sprites.draw(screen)
        pygame.draw.rect(screen, 'black', (15, 47, 20, 20), 2)
        pygame.draw.rect(screen, 'black', (40, 47, 20, 20), 2)
        pygame.draw.rect(screen, 'black', (700 - 30, 47, 20, 20), 2)
        pygame.draw.rect(screen, 'black', (700 - 55, 47, 20, 20), 2)
        for i in range(win_round1):
            pygame.draw.rect(screen, 'white', (15 * (i + 1), 47, 20, 20))
        for j in range(win_round2):
            pygame.draw.rect(screen, 'white', (700 - 30 * (j + 1), 47, 20, 20))
            pygame.draw.rect(screen, 'black', (700 - 30 * (j + 1), 47, 20, 20), 2)
        pygame.draw.rect(screen, 'green', (10, 10, player1.healts * 0 if player1.healts < 0 else player1.healts * 3, 30))
        pygame.draw.rect(screen, 'black', (10, 10, 300, 30), 5)
        pygame.draw.rect(screen, 'green', (390, 10, player2.healts * 0 if player2.healts < 0 else player2.healts * 3, 30))
        pygame.draw.rect(screen, 'black', (390, 10, 300, 30), 5)
        font = pygame.font.Font(None, 50)
        text_coord = 0
        string_rendered = font.render(str(win_round1 + win_round2 + 1), 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 345
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        pygame.display.flip()
        clock.tick(30)