import random

import pygame as pg
import constants


class Board:
    def __init__(self, window):
        self.size = 9
        self.board = [
            [0, 4, 0, 0, 0, 0, 6, 8, 5],
            [6, 0, 2, 0, 9, 8, 0, 0, 0],
            [0, 5, 0, 7, 6, 4, 0, 1, 0],
            [0, 9, 0, 0, 0, 7, 0, 6, 8],
            [0, 6, 7, 9, 0, 5, 0, 4, 2],
            [5, 2, 4, 6, 0, 3, 0, 0, 7],
            [0, 0, 0, 0, 0, 9, 0, 0, 0],
            [4, 0, 0, 0, 7, 1, 0, 0, 6],
            [9, 8, 0, 0, 5, 0, 4, 0, 0]
        ]
        self.original_fields = self.get_original_indices()
        self.window = window
        window_part = 0.3
        self.info_rect = pg.Rect(0, 0, constants.window_width, window_part * constants.window_height)
        self.game_rect = pg.Rect(0, self.info_rect.height,
                                 constants.window_width, constants.window_height - self.info_rect.height)
        # gap between small parts of board
        self.gap = 10
        self.board_size = 600
        board_x = self.game_rect.width / 2 - self.board_size / 2
        board_y = self.game_rect.height / 2 - self.board_size / 2
        self.board_rect = pg.Rect(board_x + self.game_rect.x,
                                  board_y + self.game_rect.y,
                                  self.board_size, self.board_size)
        self.board_fields = self.create_rectangles_for_fields()

    def show(self):
        pg.draw.rect(self.window, (255, 255, 255), self.info_rect)
        pg.draw.rect(self.window, (255, 0, 255), self.game_rect)
        pg.draw.rect(self.window, (0, 255, 255), self.board_rect)

        font = pg.font.Font(None, 50)
        font_color = (0, 0, 0)

        for row_counter, row_fields in enumerate(self.board_fields):
            for column_counter, field in enumerate(row_fields):
                if (row_counter, column_counter) in self.original_fields:
                    color = (128, 128, 128)
                else:
                    color = (192, 222, 60)
                pg.draw.rect(self.window, color, field)
                text = str(self.board[row_counter][column_counter])
                if text == "0":
                    text = " "
                text = font.render(text, True, font_color)

                text_width = text.get_width()
                text_height = text.get_height()
                text_x = field.width / 2 - text_width / 2 + field.x
                text_y = field.height / 2 - text_height / 2 + field.y

                self.window.blit(text, (text_x, text_y, text_width, text_height))
        pg.display.update()

    def show_in_console(self):
        for row in range(self.size):
            if row % 3 == 0 and row != 0:
                row_text = ""
                # every number 3 dashes -> 3 * 9 = 27
                # plus 6 => 33
                for _ in range(33):
                    row_text += "-"
                print(row_text)
            row_text = ""
            for column in range(self.size):
                if column % 3 == 0 and column != 0:
                    row_text += " | "
                number = self.board[row][column]
                if number:
                    row_text += " " + str(number) + " "
                else:
                    row_text += "   "
            print(row_text)

    def get_original_indices(self):
        indices = []
        for row in range(self.size):
            for column in range(self.size):
                if self.board[row][column] != 0:
                    indices.append((row, column))
        return indices

    def create_rectangles_for_fields(self):
        board_fields = []
        gap_y = 0
        field_size = (self.board_size - 2 * self.gap) / 9
        for row in range(self.size):
            gap_x = 0
            # gap is added every third row
            if row % 3 == 0 and row != 0:
                gap_y += self.gap
            row_fields = []
            for column in range(self.size):
                # gap is added every third column
                if column % 3 == 0 and column != 0:
                    gap_x += self.gap
                row_fields.append(pg.Rect(column * field_size + gap_x + self.board_rect.x,
                                          row * field_size + gap_y + self.board_rect.y,
                                          field_size, field_size))
            board_fields.append(row_fields)
        return board_fields
