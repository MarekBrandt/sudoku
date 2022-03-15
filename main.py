import sys

import constants
from game import Game
import pygame as pg
import time

from main_menu import MainMenu


def main():
    window = pg.display.set_mode((constants.window_width, constants.window_height))
    clock = pg.time.Clock()
    game = Game(window)
    menu = MainMenu(window)
    run = True
    click = False
    while run:
        menu.draw()
        pos = pg.mouse.get_pos()
        if click:
            if menu.rectangles[1].collidepoint(pos):
                game.start()
            # player vs AI
            elif menu.rectangles[2].collidepoint(pos):
                game.solve()
            # quit
            elif menu.rectangles[3].collidepoint(pos):
                pg.quit()
                sys.exit()
        click = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                click = True

        clock.tick(60)

    start = time.time()

    end = time.time()
    print(f"Program worked for {end - start} seconds")


if __name__ == "__main__":
    main()
