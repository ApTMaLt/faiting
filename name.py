import pygame
import os
import sys
all_sprites = pygame.sprite.Group()
all_spritess = pygame.sprite.Group()
clock = pygame.time.Clock()
pygame.init()
size = width, height = 600, 500
screen = pygame.display.set_mode(size)
x1, y1, x2, y2 = 100, 100, 400, 100
fps = 30
col = (0, 0, 0)
animCount1 = 0
animCount2 = 0
animCount = 0
gg = 0
activno = None


def zalypa(name, r):
    if r:
        return pygame.transform.flip(load_image(name), True, False)
    else:
        return load_image(name)


def razvorot(r):
    ninjarun = AnimatedSprite(zalypa("run.png", r), 6, 1, 0, 0)
    ninjastay = AnimatedSprite(zalypa("stay.png", r), 1, 1, 0, 0)
    ninjahm = AnimatedSprite(zalypa("handmedium.png", r), 1, 1, 0, 0)
    ninjahh = AnimatedSprite(zalypa("handhigh.png", r), 1, 1, 0, 0)
    ninjasit = AnimatedSprite(zalypa("sit.png", r), 1, 1, 0, 0)
    ninjasithandmedium = AnimatedSprite(zalypa("sithandmedium.png", r), 1, 1, 0, 0)
    ninjajump = AnimatedSprite(zalypa("jump.png", r), 5, 1, 0, 0)
    return ninjarun, ninjastay, ninjahm, ninjahh, ninjasit, ninjasithandmedium, ninjajump


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

    def otris(self, reverse, kadrov):
        global animCount, gg
        if animCount + 1 >= 30:
            animCount = 0
            gg = 0
        if animCount // kadrov != gg:
            if reverse:
                gg = len(self.frames) - animCount // 5
            else:
                gg = animCount // 5
        animCount += 1
        if gg > len(self.frames) - 1:
            gg = 0
        return self.frames[gg]


class G_Player(pygame.sprite.Sprite):
    imagestay = load_image('stay.png')

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
        self.ninjarun, self.ninjastay, self.ninjahm, self.ninjahh, self.ninjasit, self.ninjasithandmedium, self.ninjajump = razvorot(left)

    def set_protivnik(self, protivnik):
        self.protivnik = protivnik

    def A_I(self):
        global runA_I, handmediumA_I, otkat
        if otkat == 0:
            if 40 >= self.rect.x - player1.rect.x > 0:
                player2.handmedium()
                otkat = 30
                player2.stay()
        else:
            otkat -= 1
        if player1.rect.x + 30 < player2.rect.x:
            player2.run(True)
        else:
            player2.stay()

    def run(self, reverse):
        self.image = self.ninjarun.otris(reverse, 5)
        if reverse:
            self.rect = self.rect.move(-5, 0)
        else:
            self.rect = self.rect.move(5, 0)

    def handmedium(self):
        global animCount1, handmedium1
        self.image = self.ninjahm.otris(False, 30)
        if animCount1 >= 20:
            handmedium1 = False
            animCount1 = 0
            player1.stay()
        animCount1 += 1

    def handmhigh(self):
        global animCount1, handmhigh1

        self.image = self.ninjahh.otris(False, 30)
        if animCount1 >= 20:
            handmhigh1 = False
            animCount1 = 0
            player1.stay()
        animCount1 += 1

    def sithandmedium(self):
        global animCount1, handmedium1
        self.image = self.ninjasithandmedium.otris(False, 30)
        if animCount1 >= 20:
            handmedium1 = False
            animCount1 = 0
            player1.sit()
        animCount1 += 1

    def stay(self):
        global animCount, activnosti
        animCount = 0
        self.image = self.ninjastay.otris(False, 30)
        animCount = 0
        activnosti = False

    def sit(self):
        self.image = self.ninjasit.otris(False, 30)

    def jump(self):
        global animCount1, jump1, activnosti
        self.image = self.ninjajump.otris(False, 6)
        self.rect = self.rect.move(10, 0)
        if animCount // 5 in [1, 2]:
            self.rect = self.rect.move(0, -10)
        if animCount // 5 in [3, 4]:
            self.rect = self.rect.move(0, 10)
        if animCount1 + 1 >= 30:
            jump1 = False
            animCount1 = 0
            player1.stay()
            activnosti = False
        animCount1 += 1

    def update(self):
        global col, animCount1, animCount, handmedium1, handmhigh1, sit, run2, run1, jump1, activnosti, otkat, otkatjump
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and not activnosti:
                player1.run(True)
            if event.key == pygame.K_RIGHT and not activnosti:
                player1.run(False)
            if player1.otkat == 0:
                if event.key == pygame.K_UP and not activnosti and player1.otkatjump == 0:
                    animCount = 0
                    jump1 = True
                    activnosti = True
                    player1.otkatjump = 120
                if event.key == pygame.K_DOWN and not activnosti:
                    player1.sit()
                    sit = True
                    jump1 = False
                    activnosti = True
                    player1.otkat = 30
                if event.key == pygame.K_KP1 and not activnosti or event.key == pygame.K_KP1 and activnosti and sit:
                    animCount = 0
                    handmedium1 = True
                    activnosti = True
                    player1.otkat = 40
                if event.key == pygame.K_KP3 and not activnosti:
                    animCount = 0
                    handmhigh1 = True
                    activnosti = True
                    player1.otkat = 50
        if player1.otkat > 0:
            player1.otkat -= 1
        if player1.otkatjump > 0:
            player1.otkatjump -= 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and not activnosti:
                player1.stay()
            if event.key == pygame.K_RIGHT and not activnosti:
                player1.stay()
            if event.key == pygame.K_UP:
                pass
            if event.key == pygame.K_DOWN:
                player1.stay()
                sit = False
                jump1 = False
        if pygame.sprite.collide_mask(self, self.protivnik):
            col = (255, 255, 255)
        else:
            col = (0, 0, 0)
        if sit:
            if handmedium1:
                player1.sithandmedium()
            else:
                player1.sit()
        elif jump1:
            player1.jump()
        elif handmedium1:
            player1.handmedium()
        elif handmhigh1:
            player1.handmhigh()
        self.mask = pygame.mask.from_surface(self.image)


if __name__ == '__main__':
    run1, run2, handmhigh1, handmedium1, runA_I, sit, handmediumA_I, jump1, activnosti = False, False, False, False, False, False, False, False, False
    running = True
    player1, player2 = G_Player((x1, y1), False), G_Player((x2, y2), True)
    player1.set_protivnik(player2)
    player2.set_protivnik(player1)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # player2.A_I()
        all_sprites.update()
        screen.fill(col)
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(30)