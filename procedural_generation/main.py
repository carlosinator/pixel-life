import pygame
import numpy as np
import sys
import time
import utils

import conways, langtons

SCREEN_SIZE_X = 700
SCREEN_SIZE_Y = 700
SIM_PIX_SIZE = 4
UPDATE_TIME = 0 # seconds
WHITE = np.array([255, 255, 255])

num_sim_pix_x = SCREEN_SIZE_X // SIM_PIX_SIZE
num_sim_pix_y = SCREEN_SIZE_Y // SIM_PIX_SIZE


img_arr = utils.get_array_for_conway("berry.png")
world = conways.Conways(num_sim_pix_x, num_sim_pix_y, initial_config=img_arr)

# rules = "RLLR"
# colors = [(0, 0, 0), (95, 180, 245), (13, 61, 163), (136, 84, 240)] #, (68, 14, 176)]
# ant_color = (255, 0, 0)
# world = langtons.CycleLangtons(num_sim_pix_x, num_sim_pix_y, rules=rules, colors=colors, ant_color=ant_color)


pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE_X, SCREEN_SIZE_Y)) 
pygame.display.set_caption("The Secret Life of Pixels")


running = True
screen.fill(world.colors[0])
while running:
    time.sleep(UPDATE_TIME)
    world.update()

    for elem in world.changes:
        x, y = elem
        # Calculate the position of the simulated pixel on the screen
        screen_x = x * SIM_PIX_SIZE
        screen_y = y * SIM_PIX_SIZE

        idx = world.life[y,x]
        pixel_color = world.colors[idx]
        if x == world.ant_x and y == world.ant_y:
            pixel_color = world.ant_color

        # Draw the simulated pixel on the screen
        pygame.draw.rect(screen, pixel_color, (screen_x, screen_y, SIM_PIX_SIZE, SIM_PIX_SIZE))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
sys.exit()