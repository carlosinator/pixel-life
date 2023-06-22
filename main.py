import pygame
import numpy as np
import sys
import time

SCREEN_SIZE_X = 512
SCREEN_SIZE_Y = 512
SIM_PIX_SIZE = 8
UPDATE_TIME = 0.2 # seconds

num_sim_pix_x = SCREEN_SIZE_X // SIM_PIX_SIZE
num_sim_pix_y = SCREEN_SIZE_Y // SIM_PIX_SIZE


pygame.init()
screen = pygame.display.set_mode((512, 512)) 
pygame.display.set_caption("The Secret Life of Pixels")


running = True
while running:
    screen.fill((0,0,0))
    time.sleep(UPDATE_TIME)

    # Draw your simulation entities here
    for x in range(num_sim_pix_x):
        for y in range(num_sim_pix_y):
            # Calculate the position of the simulated pixel on the screen
            screen_x = x * SIM_PIX_SIZE
            screen_y = y * SIM_PIX_SIZE

            pixel_color = tuple((np.random.uniform(size=3)*127).astype(int))

            # Draw the simulated pixel on the screen
            pygame.draw.rect(screen, pixel_color, (screen_x, screen_y, SIM_PIX_SIZE, SIM_PIX_SIZE))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
sys.exit()