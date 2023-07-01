import pygame
import numpy as np
import sys
import time
import world

# SET SOME PARAMS HERE
SCREEN_SIZE_X = 800
SCREEN_SIZE_Y = 800
SIM_PIX_SIZE = 4
UPDATE_TIME = 0 # seconds

num_sim_pix_x = SCREEN_SIZE_X // SIM_PIX_SIZE
num_sim_pix_y = SCREEN_SIZE_Y // SIM_PIX_SIZE

# SET OTHER PARAMS HERE
config = {
    "pix_x" : num_sim_pix_x,
    "pix_y" : num_sim_pix_y,
    "num_nutrients" : 4,                    # number of different nutrients
    "nutrient_restore" : 1e-5,              # restoration rate of nutrients on their own
    "nutrient_greed" : 2e-3,                # amount of nutrients harvested each day, proportional to used energy
    "context_size" : 0,                     # currently meaningless
    "starting_num" : 10000,                 # starting number of plants
    "sun_energy" : 0.5,                     # amount of energy each day
    "energy_cost_age" : 1e-3,               # tax on age, exponential accumulation, fraction of sun_energy
    "energy_cost_dissipation" : 5e-3,       # like a tax on accumulated energy, it limits the amount of energy a cell can store, fraction of sun_energy
    "death_chance" : 1e-6,                  # random chance of death of a plant at a time step
    "reproduction_cost" : 2.0,              # amount of energy one must expend to create a new plant cell
    "energy_sending_cost" : 0.4,            # when passing on energy, the fraction of energy lost
    "info_sending_cost" : 0.01,             # when sending information, amount of energy lost
    "genome_size" : [(10, 9), (9,9)],       # dimensions of decision genes, left most number input, right most output, neighboring nums must match [(X, Y), (Y, Z), (Z, A)]
    "genome_mutation" : [1e-2, 1e-2, 1e-2]  # mutation params: normal noise size, bitflip prob, reversal prob
}

field = world.World(config)
WHITE = np.array([255, 255, 255])


pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE_X, SCREEN_SIZE_Y)) 
pygame.display.set_caption("The Secret Life of Pixels")


running = True

update_time = []
render_time = []

while running:
    time.sleep(UPDATE_TIME)
    update_start = time.process_time()
    field.update()
    update_time.append(time.process_time() - update_start)

    render_start = time.process_time()
    screen.fill((0,0,0))

    pix_colors = np.zeros((num_sim_pix_y, num_sim_pix_x, 3))

    # print("-"*50)

    for elem in field.entities:
        y, x = elem.location
        screen_x = x * SIM_PIX_SIZE
        screen_y = y * SIM_PIX_SIZE
        # Calculate the position of the simulated pixel on the screen

        pc = elem.genome.color
        # pix_colors[y,x] += np.array([0,255,0])
        pygame.draw.rect(screen, pc, (screen_x, screen_y, SIM_PIX_SIZE, SIM_PIX_SIZE))


        # Draw the simulated pixel on the screen
    
    # for y in range(num_sim_pix_y):
    #     for x in range(num_sim_pix_x):
    #         screen_x = x * SIM_PIX_SIZE
    #         screen_y = y * SIM_PIX_SIZE

    #         energy_val = 255 * field.energies[y,x] * 4
    #         if energy_val > 255:
    #             energy_val = 255

    #         nutr_val = 255 * min(1, np.sum(field.nutrients[y,x]))
    #         pix_colors[y,x] += np.array([0, 0, nutr_val])
    #         pc = tuple(pix_colors[y,x].astype(np.int16))
    #         # if pc != (0,0,0):
    #         #     print(pc)

    #         pygame.draw.rect(screen, pc, (screen_x, screen_y, SIM_PIX_SIZE, SIM_PIX_SIZE))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    render_time.append(time.process_time() - render_start)

    if field.world_age % 100 == 0:
        print("-"*50)
        print("world age: ", field.world_age, ", num plants", len(field.entities), f", world cost {1.1 * (1 - np.exp(-field.config['energy_cost_age'] * field.world_age)):.2f}")
        print("update time: mean", np.mean(update_time), ", total", np.sum(update_time))

pygame.quit()
sys.exit()