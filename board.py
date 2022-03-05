import random

import pygame as pg
import constants


class Board:
    def __init__(self, window):
        self.size = 9
        self.block_size = 3
        
        self.board_values = []

        # initialize board from file
        # method sets board_values
        self.read_board_values_from_file("boards/board1.txt")

        self.board_correct = True
        # checks validity of board and sets board_correct parameters
        self.check_and_set_correct()

        # pygame window
        self.window = window
        # fraction of window intended for logo etc
        window_part = 0.3
        # rect containing logo etc
        self.info_rect = pg.Rect(0, 0, constants.window_width, window_part * constants.window_height)
        self.game_rect = pg.Rect(0, self.info_rect.height,
                                 constants.window_width, constants.window_height - self.info_rect.height)
        # gap between small parts of board
        self.gap = 8
        self.board_size = 600
        board_x = self.game_rect.width / 2 - self.board_size / 2
        board_y = self.game_rect.height / 2 - self.board_size / 2
        self.board_rect = pg.Rect(board_x + self.game_rect.x,
                                  board_y + self.game_rect.y,
                                  self.board_size, self.board_size)
        self.board_fields = self.create_rectangles_for_fields()

        # stores the indices of starting fields
        self.original_fields = self.create_original_fields()

    def show(self, active_field, modifiable_field):
        pg.draw.rect(self.window, (255, 255, 255), self.info_rect)
        pg.draw.rect(self.window, (255, 0, 255), self.game_rect)
        pg.draw.rect(self.window, (0, 255, 255), self.board_rect)

        font = pg.font.Font(None, 50)
        font_color = (0, 0, 0)

        for row_counter, row_fields in enumerate(self.board_fields):
            for column_counter, field in enumerate(row_fields):
                if field in self.original_fields:
                    color = (128, 128, 128)
                elif modifiable_field == field:
                    color = (135, 206, 250)
                else:
                    color = (192, 222, 60)
                pg.draw.rect(self.window, color, field)
                text = str(self.board_values[row_counter][column_counter])
                if text == "0":
                    text = " "
                text = font.render(text, True, font_color)

                text_width = text.get_width()
                text_height = text.get_height()
                text_x = field.width / 2 - text_width / 2 + field.x
                text_y = field.height / 2 - text_height / 2 + field.y

                if active_field == field:
                    pg.draw.rect(self.window, (100, 100, 100), field, 3)

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
                number = self.board_values[row][column]
                if number:
                    row_text += " " + str(number) + " "
                else:
                    row_text += "   "
            print(row_text)

    def create_original_fields(self):
        fields = []
        for row in range(self.size):
            for column in range(self.size):
                if self.board_values[row][column] != 0:
                    fields.append(self.board_fields[row][column])
        return fields

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

    def get_board_fields(self):
        return self.board_fields

    def get_original_fields(self):
        return self.original_fields

    def get_board_rect(self):
        return self.board_rect

    def find_field_value(self, field):
        for row in range(self.size):
            for column in range(self.size):
                if field == self.board_fields[row][column]:
                    return self.board_values[row][column]

    def insert_field_value(self, field, value):
        for row in range(self.size):
            for column in range(self.size):
                if field == self.board_fields[row][column]:
                    self.board_values[row][column] = value
                    return

    def read_board_values_from_file(self, file_path):
        self.board_values = []
        file = open(file_path, "r")
        for row in range(self.size):
            one_row = []
            values_string = file.readline()
            for column in range(self.size):
                one_row.append(int(values_string[column]))
            self.board_values.append(one_row)

    # checks if values on board are correct and sets board_correct
    def check_and_set_correct(self):
        correctness = self.rule1() and self.rule2() and self.rule3()
        self.board_correct = correctness
        return correctness

    # Rule 1 - Each row must contain the numbers from 1 to 9, without repetitions
    def rule1(self):
        for row in range(self.size):
            row_values = []
            for column in range(self.size):
                value = self.board_values[row][column]
                # making sure that 0 values won't get to row_values
                if not value:
                    continue
                # repetition of value
                if value in row_values:
                    return False
                row_values.append(value)
        return True

    # Rule 2 - Each column must contain the numbers from 1 to 9, without repetitions
    def rule2(self):
        for column in range(self.size):
            column_values = []
            for row in range(self.size):
                value = self.board_values[row][column]
                # making sure that 0 values won't get to row_values
                if not value:
                    continue
                # repetition of value
                if value in column_values:
                    return False
                column_values.append(value)
        return True

    # Rule 3 - The digits can only occur once per block (nonet)
    def rule3(self):
        # int(self.size / self.block_size) gives the number of blocks (nonets)
        no_of_blocks = int(self.size / self.block_size)
        # will be checking every block and every field in block
        for block_row in range(no_of_blocks):
            for block_column in range(no_of_blocks):
                block_values = []
                for row in range(self.block_size):
                    for column in range(self.block_size):
                        row_index = block_row * self.block_size + row
                        column_index = block_column * self.block_size + column

                        value = self.board_values[row_index][column_index]
                        # value == 0
                        if not value:
                            continue
                        if value in block_values:
                            return False
                        block_values.append(value)
        return True

    def get_board_correct(self):
        return self.board_correct

    def is_board_full(self):
        for row in range(self.size):
            if 0 in self.board_values[row]:
                return False
        return True

    def get_field_coordinates(self, field):
        for row in range(self.size):
            for column in range(self.size):
                if field == self.board_fields[row][column]:
                    return row, column
        return None

    def find_field_beside(self, field, direction):
        if direction in constants.DIRECTIONS:
            row, column = self.get_field_coordinates(field)
            if direction == "up":
                # if it is not the upper border
                if row != 0:
                    field = self.board_fields[row-1][column]
            if direction == "down":
                # if it is not the lower border
                if row != self.size-1:
                    field = self.board_fields[row+1][column]
            if direction == "left":
                # if it is not the left border
                if column != 0:
                    field = self.board_fields[row][column-1]
            if direction == "right":
                # if it is not the right border
                if column != self.size-1:
                    field = self.board_fields[row][column+1]
            return field

        else:
            print("direction have to be a value from constants.DIRECTION")
            return 1


