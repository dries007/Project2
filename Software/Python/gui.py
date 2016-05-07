#!/usr/bin/env python

import os
import pygame
import time
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.display.init()
pygame.mouse.set_visible(False)
pygame.font.init()
size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
print("Framebuffer size: %d x %d" % (size[0], size[1]))
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
screen.fill(BLACK)
pygame.display.update()

font = pygame.font.Font(None, 50)
text_surface = font.render('SmartClock (%s)' % "0.1", True, WHITE)
screen.blit(text_surface, (0, 0))

pygame.display.update()

time.sleep(10)
