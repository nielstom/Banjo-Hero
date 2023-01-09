import pygame
from pygame.locals import *
import sys
import random

pygame.init()

SPAWN_EVENT = pygame.USEREVENT+1
SCORE_NOTIFICATION_EVENT = pygame.USEREVENT+2
spawn_rate = 500  # ms
pygame.time.set_timer(SPAWN_EVENT, spawn_rate)

vec = pygame.math.Vector2  # 2 for two-dimensional

HEIGHT = 450
WIDTH = 400
ACC = 0.5
FPS = 60
SCORE_MISS = 0
SCORE_HIT = 0
SCORE_ERR = 0
SCORE_STREAK = 0
PRESSED_L, PRESSED_U, PRESSED_D, PRESSED_R, PRESSED_S = False, False, False, False, False

FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Banjo Hero")


class Platform(pygame.sprite.Sprite):
    def __init__(self, x_loc, sp):
        super().__init__()
        self.surf = pygame.Surface([60, 12])
        self.x_loc = x_loc
        color_val = 255
        if x_loc == 0:
            pass
        elif x_loc == 1:
            self.surf.fill((0, color_val, 0))
        elif x_loc == 2:
            self.surf.fill((color_val, 0, 0))
        elif x_loc == 3:
            self.surf.fill((color_val, color_val, 0))
        elif x_loc == 4:
            self.surf.fill((0, 0, color_val))
        else:
            exit("Unrecognized x_loc")

        self.rect = self.surf.get_rect(center=[WIDTH*x_loc//5, HEIGHT//5])
        self.speed = sp

    def move(self):
        global SCORE_MISS, SCORE_STREAK
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom > HEIGHT:
            SCORE_MISS += 1
            SCORE_STREAK = 0
            self.kill()


def check(platform, player):
    return pygame.sprite.collide_rect(platform, player)


speed = 2  # Configure

PT1 = Platform(0, 0)
PT1.surf = pygame.Surface((WIDTH, 20))
PT1.surf.fill((255, 0, 0))
PT1.rect = PT1.surf.get_rect(center=(WIDTH / 2, HEIGHT - 10))

platform_width = 60
platform_height = 40
color_val_unpressed = 60
color_val_pressed = 120

PT_L = Platform(0, 0)
PT_L.surf = pygame.Surface((platform_width, platform_height))
PT_L.surf.fill((0, color_val_unpressed, 0))
PT_L.rect = PT_L.surf.get_rect(center=(WIDTH//5, HEIGHT-80))

PT_U = Platform(0, 0)
PT_U.surf = pygame.Surface((platform_width, platform_height))
PT_U.surf.fill((color_val_unpressed, 0, 0))
PT_U.rect = PT_U.surf.get_rect(center=(WIDTH*2//5, HEIGHT-80))

PT_D = Platform(0, 0)
PT_D.surf = pygame.Surface((platform_width, platform_height))
PT_D.surf.fill((color_val_unpressed, color_val_unpressed, 0))
PT_D.rect = PT_D.surf.get_rect(center=(WIDTH*3//5, HEIGHT-80))

PT_R = Platform(0, 0)
PT_R.surf = pygame.Surface((platform_width, platform_height))
PT_R.surf.fill((0, 0, color_val_unpressed))
PT_R.rect = PT_R.surf.get_rect(center=(WIDTH*4//5, HEIGHT-80))

all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(PT_L)
all_sprites.add(PT_U)
all_sprites.add(PT_D)
all_sprites.add(PT_R)

platforms = pygame.sprite.Group()
platforms.add(PT1)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SPAWN_EVENT:
            x_loc = random.randint(1, 4)
            pl = Platform(x_loc, speed)
            platforms.add(pl)
            all_sprites.add(pl)
        if event.type == SCORE_NOTIFICATION_EVENT:
            pass
            # TODO: some kind of notice on the bottom if hit/miss/error
            # PT1.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                PRESSED_S = True
            if event.key == pygame.K_RIGHT:
                PRESSED_L = True
                PT_L.surf.fill((0, color_val_pressed, 0))
            if event.key == pygame.K_DOWN:
                PRESSED_U = True
                PT_U.surf.fill((color_val_pressed, 0, 0))
            if event.key == pygame.K_LEFT:
                PRESSED_D = True
                PT_D.surf.fill((color_val_pressed, color_val_pressed, 0))
            if event.key == pygame.K_UP:
                PRESSED_R = True
                PT_R.surf.fill((0, 0, color_val_pressed))
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                PRESSED_L = False
                PT_L.surf.fill((0, color_val_unpressed, 0))
            if event.key == pygame.K_DOWN:
                PRESSED_U = False
                PT_U.surf.fill((color_val_unpressed, 0, 0))
            if event.key == pygame.K_LEFT:
                PRESSED_D = False
                PT_D.surf.fill((color_val_unpressed, color_val_unpressed, 0))
            if event.key == pygame.K_UP:
                PRESSED_R = False
                PT_R.surf.fill((0, 0, color_val_unpressed))

    if PRESSED_S:
        PRESSED_S = False

        if PRESSED_L:
            good_input = False
            for entity in platforms:
                if check(entity, PT_L):
                    good_input = True
                    # TODO: Set up a trigger event so entity.kill non-immediate -------
                    entity.surf.fill((0, 0, 0))
                    entity.kill()
                    # TODO: -----------------------------------------------------------
                    break
            if good_input:
                SCORE_HIT += 1
                SCORE_STREAK += 1
            else:
                SCORE_ERR += 1
                SCORE_STREAK = 0

        if PRESSED_U:
            good_input = False
            for entity in platforms:
                if check(entity, PT_U):
                    good_input = True
                    # TODO: Set up a trigger event so entity.kill non-immediate -------
                    entity.surf.fill((0, 0, 0))
                    entity.kill()
                    # TODO: -----------------------------------------------------------
                    break
            if good_input:
                SCORE_HIT += 1
                SCORE_STREAK += 1
            else:
                SCORE_ERR += 1
                SCORE_STREAK = 0

        if PRESSED_D:
            good_input = False
            for entity in platforms:
                if check(entity, PT_D):
                    good_input = True
                    # TODO: Set up a trigger event so entity.kill non-immediate -------
                    entity.surf.fill((0, 0, 0))
                    entity.kill()
                    # TODO: -----------------------------------------------------------
                    break
            if good_input:
                SCORE_HIT += 1
                SCORE_STREAK += 1
            else:
                SCORE_ERR += 1
                SCORE_STREAK = 0

        if PRESSED_R:
            good_input = False
            for entity in platforms:
                if check(entity, PT_R):
                    good_input = True
                    # TODO: Set up a trigger event so entity.kill non-immediate -------
                    entity.surf.fill((0, 0, 0))
                    entity.kill()
                    # TODO: -----------------------------------------------------------
                    break
            if good_input:
                SCORE_HIT += 1
                SCORE_STREAK += 1
            else:
                SCORE_ERR += 1
                SCORE_STREAK = 0

    displaysurface.fill((0, 0, 0))
    f = pygame.font.SysFont("Verdana", 15)
    hit_perc = 0
    if SCORE_HIT+SCORE_MISS+SCORE_ERR > 0:
        hit_perc = 100*SCORE_HIT//(SCORE_HIT+SCORE_MISS+SCORE_ERR)
    g = f.render("ACCURACY: " + str(hit_perc) + "% | STREAK: " + str(SCORE_STREAK), True, (123, 255, 0))
    displaysurface.blit(g, (WIDTH / 4, 10))

    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
        entity.move()

    pygame.display.update()
    FramePerSec.tick(FPS)
