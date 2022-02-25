import sys

from board import Board
import pygame as pg
import constants


def main():
    window = pg.display.set_mode((constants.window_width, constants.window_height))
    clock = pg.time.Clock()

    pg.display.set_caption("Sudoku")

    pg.init()

    game_board = Board(window)

    run = True
    click = False
    while run:
        game_board.show()
        pos = pg.mouse.get_pos()
        if click:
            pass
        click = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                click = True

        clock.tick(60)


if __name__ == "__main__":
    main()
