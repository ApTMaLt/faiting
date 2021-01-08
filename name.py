import pygame
import os
import sys
all_sprites = pygame.sprite.Group()
all_spritess = pygame.sprite.Group()
clock = pygame.time.Clock()
pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
x1, y1, x2, y2 = 0, 100, 400, 100
fps = 30
col = (0, 0, 0)
animCount1 = 0
animCount2 = 0
animCount = 0
otkat = 0


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
    return ninjarun, ninjastay, ninjahm, ninjahh, ninjasit, ninjasithandmedium


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

    def otris(self, reverse):
        global animCount
        if animCount + 1 >= 30:
            animCount = 0
        if animCount % 5 == 0:
            if reverse:
                self.cur_frame = (self.cur_frame - 1) % len(self.frames)
            else:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        animCount += 1
        return self.frames[self.cur_frame]


class Player2(pygame.sprite.Sprite):
    imagestay = load_image('stay.png')

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = Player2.imagestay
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.ninjarun, self.ninjastay, self.ninjahm, self.ninjahh, self.ninjasit, self.ninjasithandmedium = razvorot(True)

    def A_I(self):
        global runA_I, handmediumA_I, otkat
        if otkat == 0:
            if 40 >= self.rect.x - player1.rect.x > 0:
                handmediumA_I = True
                otkat = 30
                runA_I = False
        else:
            otkat -= 1
        if player1.rect.x + 30 < self.rect.x:
            runA_I = True
        else:
            runA_I = False

    def run(self):
        self.image = self.ninjarun.otris(True)
        self.rect = self.rect.move(-5, 0)

    def handmedium(self):
        global animCount2, handmediumA_I
        if animCount2 >= 10:
            handmediumA_I = False
            animCount2 = 0
        self.image = self.ninjahm.otris(False)
        animCount2 += 1

    def update(self):
        global col, animCount2
        if pygame.sprite.collide_mask(self, player1):
            col = (255, 255, 255)
        else:
            col = (0, 0, 0)
        if runA_I:
             self.run()
        elif handmediumA_I:
            self.handmedium()
        else:
            animCount2 = 0
            self.image = self.ninjastay.otris(False)
        self.mask = pygame.mask.from_surface(self.image)


class G_Player(pygame.sprite.Sprite):
    imagestay = load_image('stay.png')

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = G_Player.imagestay
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.ninjarun, self.ninjastay, self.ninjahm, self.ninjahh, self.ninjasit, self.ninjasithandmedium = razvorot(False)

    def run(self, reverse):
        self.image = self.ninjarun.otris(reverse)
        if reverse:
            self.rect = self.rect.move(-5, 0)
        else:
            self.rect = self.rect.move(5, 0)

    def handmedium(self):
        global animCount1, handmedium1
        if animCount1 >= 10:
            handmedium1 = False
            animCount1 = 0
        self.image = self.ninjahm.otris(False)
        animCount1 += 1

    def handmhigh(self):
        global animCount1, handmhigh1
        if animCount1 >= 10:
            handmhigh1 = False
            animCount1 = 0
        self.image = self.ninjahh.otris(False)
        animCount1 += 1

    def sithandmedium(self):
        global animCount1, handmedium1
        if animCount1 >= 10:
            handmedium1 = False
            animCount1 = 0
        self.image = self.ninjasithandmedium.otris(False)
        animCount1 += 1

    def sit(self):
        self.image = self.ninjasit.otris(False)

    def update(self):
        global col, animCount1
        if pygame.sprite.collide_mask(self, player2):
            col = (255, 255, 255)
        else:
            col = (0, 0, 0)
        if run1 and self.rect.x + 40 < player2.rect.x:
            self.run(False)
        elif run2 and self.rect.x - 40 < player2.rect.x:
            self.run(True)
        elif sit:
            if handmedium1:
                self.sithandmedium()
            else:
                self.sit()
        elif handmedium1:
            self.handmedium()
        elif handmhigh1:
            self.handmhigh()
        else:
            animCount1 = 0
            self.image = self.ninjastay.otris(False)
        self.mask = pygame.mask.from_surface(self.image)


if __name__ == '__main__':
    run1, run2, handmhigh1, handmedium1, runA_I, sit, handmediumA_I = False, False, False, False, False, False, False
    running = True
    player1 = G_Player((x1, y1))
    player2 = Player2((x2, y2))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    run2 = True
                if event.key == pygame.K_RIGHT:
                    run1 = True
                if event.key == pygame.K_UP:
                    pass
                if event.key == pygame.K_DOWN:
                    sit = True
                if event.key == pygame.K_KP1:
                    handmedium1 = True
                    handmhigh1 = False
                if event.key == pygame.K_KP3:
                    handmhigh1 = True
                    handmedium1 = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    run2 = False
                    animCount1 = 0
                    handmedium1 = False
                    handmhigh1 = False
                if event.key == pygame.K_RIGHT:
                    run1 = False
                    animCount1 = 0
                    handmedium1 = False
                    handmhigh1 = False
                if event.key == pygame.K_UP:
                    pass
                if event.key == pygame.K_DOWN:
                    animCount1 = 0
                    sit = False
                    handmhigh1 = False
        player2.A_I()
        all_sprites.update()
        screen.fill(col)
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
