import sys

from board import Board
import pygame as pg
import constants


class Game:
    def __init__(self):
        self.window = pg.display.set_mode((constants.window_width, constants.window_height))
        self.clock = pg.time.Clock()

        pg.display.set_caption("Sudoku")

        pg.init()

        self.game_board = Board(self.window)
        self.rectangles = self.game_board.get_board_fields()
        self.original_fields = self.game_board.get_original_fields()
        self.fps = 60

    def start(self):
        active_field = None

        run = True
        click = False
        while run:
            self.game_board.show(active_field)
            pos = pg.mouse.get_pos()
            position_found = 0
            if click:
                # user clicked beside board, stop focus
                if not self.game_board.get_board_rect().collidepoint(pos):
                    active_field = None
                # user clicked on one of fields
                else:
                    for rect_row in self.rectangles:
                        for rect in rect_row:
                            if rect.collidepoint(pos):
                                if rect not in self.original_fields:
                                    active_field = rect
                                else:
                                    active_field = None
                                break
            click = False
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()

                    # if there is active field
                    if active_field is not None:
                        if event.key == pg.K_BACKSPACE:
                            # value 0 is invisible on board
                            self.game_board.insert_field_value(active_field, 0)
                        elif event.key == pg.K_1 or pg.K_2 or pg.K_3 or pg.K_4 or pg.K_5 or pg.K_6 \
                                or pg.K_7 or pg.K_8 or pg.K_9 or pg.K_0:
                            # for numbers pg.key.name returns for instance [4], value takes only number
                            value = pg.key.name(event.key)
                            # if numeric keypad
                            if '[' in value:
                                value = int(value[1])
                            else:
                                value = int(value)

                            self.game_board.insert_field_value(active_field, value)
                        # after changing a value
                        print(self.game_board.check_and_set_correct())

                if event.type == pg.MOUSEBUTTONDOWN:
                    click = True

            self.clock.tick(self.fps)

    # def click_handler(self):
