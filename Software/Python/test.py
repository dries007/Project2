#!/bin/env python

import os
import time
# noinspection PyUnresolvedReferences
import pygame

os.putenv('SDL_FBDEV', '/dev/fb1')

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

print("Mark")
pygame.display.init()
pygame.font.init()
pygame.mouse.set_visible(False)

FONT_XL = pygame.font.SysFont('notomono', 50)

SIZE = (pygame.display.Info().current_w, pygame.display.Info().current_h)
SCREEN = pygame.display.set_mode(SIZE, pygame.FULLSCREEN)
SCREEN.fill(BLACK)

text = FONT_XL.render("Booting...", False, WHITE)
x = (SCREEN.get_width() - text.get_width()) / 2
y = SCREEN.get_height()/ 2 - text.get_height()

SCREEN.blit(text, (x, y))
pygame.display.update()

time.sleep(300)

