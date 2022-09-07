import mido
import pygame as pg
import pygame
import numpy as np

col_about_to_die = (200, 200, 225)
col_alive = (255, 255, 215)
col_background = (10, 10, 40)
col_grid = (30, 30, 60)


def update_with_midi(surface, cur, sz, midiNote, midiVel):
    nxt = np.zeros((cur.shape[0], cur.shape[1]))
    nxt[midiNote][midiVel] = 1
    nxt[midiNote + 1][midiVel] = 1
    nxt[midiNote - 1][midiVel] = 1
    nxt[midiNote][midiVel + 1] = 1
    nxt[midiNote][midiVel - 1] = 1

    for r, c in np.ndindex(cur.shape):
        num_alive = np.sum(cur[r - 1:r + 2, c - 1:c + 2]) - cur[r, c]

        if cur[r, c] == 1 and num_alive < 2 or num_alive > 3:
            col = col_about_to_die
        elif (cur[r, c] == 1 and 2 <= num_alive <= 3) or (cur[r, c] == 0 and num_alive == 3):
            nxt[r, c] = 1
            col = col_alive

        col = col if cur[r, c] == 1 else col_background
        pygame.draw.rect(surface, col, (c * sz, r * sz, sz - 1, sz - 1))

    return nxt


def update(surface, cur, sz):
    nxt = np.zeros((cur.shape[0], cur.shape[1]))

    for r, c in np.ndindex(cur.shape):
        num_alive = np.sum(cur[r - 1:r + 2, c - 1:c + 2]) - cur[r, c]

        if cur[r, c] == 1 and num_alive < 2 or num_alive > 3:
            col = col_about_to_die
        elif (cur[r, c] == 1 and 2 <= num_alive <= 3) or (cur[r, c] == 0 and num_alive == 3):
            nxt[r, c] = 1
            col = col_alive

        col = col if cur[r, c] == 1 else col_background
        pygame.draw.rect(surface, col, (c * sz, r * sz, sz - 1, sz - 1))

    return nxt


def init(dimx, dimy):
    cells = np.zeros((dimy, dimx))
    # pattern = np.zeros((dimy, dimx))
    # pos = (3,3)
    # cells[pos[0]:pos[0]+pattern.shape[0], pos[1]:pos[1]+pattern.shape[1]] = pattern
    return cells


def main(dimx, dimy, cellsize):
    pygame.init()
    surface = pygame.display.set_mode((dimx * cellsize, dimy * cellsize))
    pygame.display.set_caption("John Conway's Game of Life")

    cells = init(dimx, dimy)

    with mido.open_input(names[0]) as inport:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            for msg in inport:
                note = msg.note
                velocity = msg.velocity
                surface.fill(col_grid)
                cells = update_with_midi(surface, cells, cellsize, note, velocity)
                pygame.display.update()
    surface.fill(col_grid)
    cells = update(surface, cells, cellsize)
    pygame.display.update()


names = mido.get_input_names()
print(names)
out_port = mido.open_output()

main(129, 86, 8)
