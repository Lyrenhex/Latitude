"""
Latitude, an infinite sidescroller / platformer game
Copyright (C) 2017  Damian Heaton <dh64784@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

This game was created in around an hour (maybe, didn't time it :<) on
Tuesday 14th February 2017. Yeah, I got bored.

CREDITS:
- Me, myself, and I: Programming, game concept, "game design", etc.
- lat (anon. abbr.): Name inspiration, 'encouragement', putting up
                     with me complaining often, etc.

"10 / 10 best game 2k17" - IGN (not really, pls no sue me)
Honestly, idk why you're even looking at this. Why not go play Overwatch?
"""

from pygame.locals import *
import pygame # it's a game, yeah
import random
import math
import time
import sys
import os

# -*- coding: utf-8 -*-

VERSION = "1.0.1"

global STAGE_LENGTH, TILE_SIZE, WINDOW_SIZE
STAGE_LENGTH = 20
TILE_SIZE = (120, 5)
WINDOW_SIZE = (900, 500)
STAGE_SIZE = (STAGE_LENGTH * TILE_SIZE[0] + TILE_SIZE[0], WINDOW_SIZE[1])

pygame.init()
display = pygame.display.set_mode(WINDOW_SIZE, HWSURFACE | DOUBLEBUF)
pygame.display.set_caption("Latitude v%s" % VERSION)

logo = pygame.image.load("logo.png")
pygame.display.set_icon(logo)

clock = pygame.time.Clock()

font = pygame.font.Font(None, 18)

def genStage ():
    stage = pygame.Surface(STAGE_SIZE).convert()
    stage.fill ((0, 0, 0))
    stageColour = (random.randint(10, 255), random.randint(10, 255),
                   random.randint(10, 255))
    tiles = [(0, STAGE_SIZE[1] / 2 + TILE_SIZE[1])]
    pygame.draw.rect(stage, stageColour, (0, STAGE_SIZE[1] / 2 + TILE_SIZE[1],
                                          TILE_SIZE[0] - 5, TILE_SIZE[1]))
    x = TILE_SIZE[0]
    for tile in range(STAGE_LENGTH - 1):
        if tile != STAGE_LENGTH - 2:
            y = random.randint(50, STAGE_SIZE[1] - TILE_SIZE[1])
            tiles.append((x, y))
            pygame.draw.rect(stage, stageColour, (x, y, TILE_SIZE[0] - 5,
                                                  TILE_SIZE[1]))
            x += TILE_SIZE[0]
        else:
            tiles.append((x, 0))
            pygame.draw.rect(stage, stageColour, (x, 0, TILE_SIZE[0],
                                                  STAGE_SIZE[1]))
            x += TILE_SIZE[0]
    return tiles, stage

def play():
    score = -1
    speed = 0.9
    while True:
        stage = genStage()
        offset = 0
        pX = (WINDOW_SIZE[0] / 2) - 5
        pY = (WINDOW_SIZE[1] / 2) - 5
        held = 0
        held2 = False
        score += 1
        speed += 0.1

        hold = True

        while hold:
            clock.tick(60)
            display.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == QUIT:
                    # user wants to close.
                    pygame.quit()
                    sys.exit()
            # get the held keys
            key = pygame.key.get_pressed()
            jumptime = 250 / speed
            if key[K_SPACE]:
                if held <= jumptime:
                    # holding space -- jump!
                    pY -= 4
                    held += 1
                held2 = True
            else:
                held2 = False
            if pY >= WINDOW_SIZE[1]:
                # game over
                print("Game over.")
                hold = False
            curTile = math.floor((offset + 5) / TILE_SIZE[0])
            if curTile == STAGE_LENGTH - 1:
                break
            display.blit(stage[1], (WINDOW_SIZE[0] / 2 - offset, 0))
            if (pY + 10 > stage[0][curTile][1] + TILE_SIZE[1]
                or pY + 10 < stage[0][curTile][1]):
                # too high or low, should descend
                pY += 2
            else:
                if not held2:
                    held = 0
            pygame.draw.rect(display, (255, 255, 255), (pX, pY, 10, 10))
            display.blit(font.render("Score: %i" % score, True, (255, 255, 255)), (5, 5))
            if held2:
                percent = held / jumptime * 100
                percent = 100 - percent
                width = WINDOW_SIZE[0] / 100 * percent
                pygame.draw.rect(display, (255, 255, 255), (0, WINDOW_SIZE[1] - 10,
                                                            width, 10))
            pygame.display.update()
            offset += 1 * speed
        else:
            break

    display.fill((0, 0, 0))
    goFont = pygame.font.SysFont("Monospace", 32)
    display.blit(goFont.render("Game Over!", True, (255, 0, 0)),
                               (WINDOW_SIZE[0] / 2 - 16 * 5,
                                WINDOW_SIZE[1] / 2 - 32))
    score = "Your Score: %i" % score
    display.blit(goFont.render(score, True, (200, 200, 200)),
                 (WINDOW_SIZE[0] / 2 - len(score) / 2 * 16,
                  WINDOW_SIZE[1] / 2 + 16))
    display.blit(goFont.render("Press space to restart", True, (100, 100, 100)),
                               (WINDOW_SIZE[0] / 2 - 16 * 11,
                                WINDOW_SIZE[1] - 32))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                # user wants to close.
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    play()

play()
