import sys
import threading
from board import Board
import pygame as pg
import constants


# represents all actions made in game
class Game:
    def __init__(self):
        self.window = pg.display.set_mode((constants.window_width, constants.window_height))
        self.clock = pg.time.Clock()

        pg.display.set_caption("Sudoku")

        pg.init()

        self.game_board = Board(self.window)
        self.fields = self.game_board.get_board_fields()
        self.fps = 60

    def start(self):
        active_field = None
        modifiable_field = None

        run = True
        click = False
        while run:
            self.game_board.show(active_field, modifiable_field)
            pos = pg.mouse.get_pos()
            if click:
                # user clicked beside board, stop focus
                if not self.game_board.get_board_rect().collidepoint(pos):
                    active_field = None
                    modifiable_field = None
                # user clicked on one of fields
                else:
                    for fields_row in self.fields:
                        for field in fields_row:
                            rect = field.get_rect()
                            if rect.collidepoint(pos):
                                active_field = field
                                if field.get_is_original():
                                    modifiable_field = None
                                else:
                                    modifiable_field = field
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
                        if event.key == pg.K_UP:
                            active_field = self.game_board.find_field_beside(active_field, "up")
                        if event.key == pg.K_DOWN:
                            active_field = self.game_board.find_field_beside(active_field, "down")
                        if event.key == pg.K_LEFT:
                            active_field = self.game_board.find_field_beside(active_field, "left")
                        if event.key == pg.K_RIGHT:
                            active_field = self.game_board.find_field_beside(active_field, "right")

                        # active field is now changed or remain the same
                        if active_field.get_is_original():
                            modifiable_field = None
                        else:
                            modifiable_field = active_field

                        if modifiable_field:
                            if event.key == pg.K_BACKSPACE:
                                # value 0 is invisible on board
                                modifiable_field.set_value(0)
                            if event.unicode.isdigit():
                                value = int(event.unicode)
                                print(value)
                                modifiable_field.set_value(value)

                            # after move
                            if self.game_board.is_board_full():
                                menu = self.game_board.get_menu()
                                if self.game_board.check_and_set_correct():
                                    menu.set_key("valid")
                                else:
                                    menu.set_key("invalid")

                if event.type == pg.MOUSEBUTTONDOWN:
                    click = True

            self.clock.tick(self.fps)

    def brute_force(self):
        # fields that have to be solved
        fields_to_solve = []
        for fields_row in self.fields:
            for field in fields_row:
                if not field.get_is_original():
                    fields_to_solve.append(field)

        correct = None
        index = 0
        solved = False
        while not solved:
            # check if all fields already filled up
            if index == len(fields_to_solve):
                if self.game_board.check_and_set_correct():
                    solved = True
                    print("solved")
                    continue
            # puzzle is unsolvable
            elif index == -1:
                print("unsolvable")
                break

            field = fields_to_solve[index]
            # initiating field for changes, set incremented value
            value = field.get_value()
            field.set_value(value + 1)

            for value in range(field.get_value(), 10):
                field.set_value(value)
                # if correct go to next field
                correct = self.game_board.check_and_set_correct()
                if correct:
                    index += 1
                    break
                # incorrect do nothing
            # if there is no solution
            if not correct:
                # erase changes
                field.set_value(0)
                index -= 1

    def solve(self):
        run = True

        brute = threading.Thread(target=self.brute_force, args=())
        brute.start()

        while run:
            self.game_board.show()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        run = False
