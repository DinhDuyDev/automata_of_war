import pygame
import game_matrix as g
from pygame.locals import *
import settings
import asyncio
import os

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT), HWSURFACE | DOUBLEBUF | RESIZABLE)
draw_dest = screen.copy()

cursor_surf = pygame.Surface((settings.cell_dimension, settings.cell_dimension))
cursor_surf.fill((255, 0, 0))
cursor_surf.set_alpha(128)

my_font = pygame.sysfont.SysFont("Arial", 10)

clock = pygame.time.Clock()
clock_fps = 60


def mouse_translate():
    x = pygame.mouse.get_pos()[0] / (screen.get_rect().width / draw_dest.get_width()) / settings.zoom
    y = pygame.mouse.get_pos()[1] / (screen.get_rect().height / draw_dest.get_height()) / settings.zoom
    return x, y

async def main():
    generation = 0
    running = True
    sim_running = False
    is_x = True

    while running:
        mx, my = mouse_translate()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_e:
                    sim_running = not sim_running
                    print(f"Game running: {sim_running}")
                elif event.key == pygame.K_x:
                    is_x = not is_x
                elif event.key == pygame.K_SPACE:
                    g.sim()
                    generation += 1
                elif event.key == pygame.K_TAB:
                    for row in g.game_matrix:
                        for cell in row:
                            cell.set_faction("None")
                            cell.set_state("UNOCCUPIED")

        #elif event.type == pygame.MOUSEBUTTONDOWN:
        if not sim_running:
            xx = int(mx / settings.cell_dimension)
            yy = int(my / settings.cell_dimension)
            state = "CAPITAL"
            if pygame.key.get_pressed()[pygame.K_RSHIFT]:
                state = "TERRAIN"
            elif pygame.key.get_pressed()[pygame.K_RETURN]:
                state = "UNOCCUPIED"

            if pygame.mouse.get_pressed()[0]:
                g.game_matrix[yy][xx].set_state(state)
                if state not in "TERRAIN UNOCCUPIED":
                    g.game_matrix[yy][xx].set_faction('X' if is_x else 'O') # setting different factions
                else:
                    g.game_matrix[yy][xx].set_faction("None")

        if sim_running:
            clock_fps = 10
            g.sim()
            # pyautogui.screenshot(f"all_screenshots/scout{generation}.png")
            if pygame.key.get_pressed()[pygame.K_s]:
                os.system(f"screencapture all_screenshots/zone_of_conflict{generation}.png")
                generation += 1
        else:
            clock_fps = 60

        draw_dest.fill((0, 0, 0))

        for y in range(settings.ver_cells):
            for x in range(settings.hor_cells):
                if g.game_matrix[y][x].get_state() != "UNOCCUPIED":
                    cel = g.game_matrix[y][x].faction
                    st = g.game_matrix[y][x].get_state()
                    col = g.state_colors[st]
                    pygame.draw.rect(draw_dest, col, (x * settings.cell_dimension, y * settings.cell_dimension,
                                                      settings.cell_dimension, settings.cell_dimension))
                    if cel == 'X':
                        pygame.draw.line(draw_dest, 'white', (x * settings.cell_dimension + settings.cell_dimension * 0.3, y * settings.cell_dimension + settings.cell_dimension * 0.3)
                                         , (x * settings.cell_dimension + settings.cell_dimension - settings.cell_dimension * 0.3, y * settings.cell_dimension + settings.cell_dimension - settings.cell_dimension * 0.3))
                        pygame.draw.line(draw_dest, 'white', (x * settings.cell_dimension + settings.cell_dimension - settings.cell_dimension * 0.2, y * settings.cell_dimension + settings.cell_dimension * 0.3)
                                         , (x * settings.cell_dimension + settings.cell_dimension * 0.3,
                                            y * settings.cell_dimension + settings.cell_dimension - settings.cell_dimension * 0.3))
                    elif cel == 'O':
                        pygame.draw.circle(draw_dest, 'white',
                                           (x * settings.cell_dimension + settings.cell_dimension / 2,
                                            y * settings.cell_dimension + settings.cell_dimension / 2), 2, 1)

                else:
                    pygame.draw.line(draw_dest, 'gray', (x * settings.cell_dimension, y * settings.cell_dimension),
                                     (x * settings.cell_dimension + settings.cell_dimension, y * settings.cell_dimension))
                    pygame.draw.line(draw_dest, 'gray', (x * settings.cell_dimension, y * settings.cell_dimension),
                                     (x * settings.cell_dimension, y * settings.cell_dimension + settings.cell_dimension))


        cursor_rect = cursor_surf.get_rect(
            topleft=(int(mx / settings.cell_dimension) * settings.cell_dimension, int(my / settings.cell_dimension) * settings.cell_dimension))
        draw_dest.blit(cursor_surf, cursor_rect)
        screen.blit(pygame.transform.scale_by(pygame.transform.scale(draw_dest, screen.get_rect().size), settings.zoom),
                    draw_dest.get_rect(center=(settings.WINDOW_WIDTH / 2, settings.WINDOW_HEIGHT / 2)))

        pygame.display.flip()
        clock.tick(clock_fps)
        await asyncio.sleep(0)

asyncio.run(main())

