import pygame as pg

import constants


class MainMenu:
    def __init__(self, WIN, advanced_menu_set=[]):
        self.WIN = WIN

        self.menu_text = ["Sudoku", "Play", "Solve", "Quit"]

        self.no_of_rectangles = len(self.menu_text)

        # deafult menu settings
        self.logo_height = 80
        self.rect_height = 60
        self.fract_WIDTH = (2 / 3)
        self.button_gap = 30

        self.decode_advanced_menu_set(advanced_menu_set)

        self.rectangles = self.rectangles_for_menu()

    def draw(self, highlighted=[]):
        self.WIN.fill(constants.COLORS['black'])
        buttons_font = pg.font.Font(None, 32)
        caption = pg.font.Font(None, 50)
        for i in range(len(self.rectangles)):

            if i in highlighted:
                pg.draw.rect(self.WIN, constants.COLORS['light_blue'], self.rectangles[i])
            elif i != 0:
                pg.draw.rect(self.WIN, constants.COLORS['white'], self.rectangles[i])

            if i == 0:
                font = caption
                color = constants.COLORS['yellow']
            else:
                font = buttons_font
                color = constants.COLORS['black']

            txt_surface = font.render(self.menu_text[i], True, color)

            txt_x = self.rectangles[i].width / 2 - txt_surface.get_width() / 2 + self.rectangles[i].x
            txt_y = self.rectangles[i].height / 2 - txt_surface.get_height() / 2 + self.rectangles[i].y

            self.WIN.blit(txt_surface, (txt_x, txt_y, txt_surface.get_width(), txt_surface.get_height()))
        pg.display.update()

    # fract_width argument is the fraction of app window screen
    # no_of_rect contains rect with logo
    def rectangles_for_menu(self):
        rectangles = []

        # height of all buttons + gaps between them
        total_buttons_height = (self.no_of_rectangles - 1) * self.rect_height + \
                               (self.no_of_rectangles - 2) * self.button_gap

        unused_height = constants.window_height - total_buttons_height - self.logo_height
        logo_gap = unused_height / 3

        # total height is sum of buttons height (no_of_rectangles -1 ; cause of logo) and gaps between them
        rectangles_height = total_buttons_height + self.logo_height + logo_gap
        button_width = constants.window_width * self.fract_WIDTH
        header_width = 0.9 * constants.window_width
        header_height = self.rect_height + 20
        y = constants.window_height / 2 - rectangles_height / 2
        for i in range(self.no_of_rectangles):
            # it is not the logo rect
            if i != 0:
                height = self.rect_height
                width = button_width
                gap = self.button_gap
            # logo rect
            else:
                height = header_height
                width = header_width
                gap = logo_gap

            # centering
            x = constants.window_width / 2 - width / 2

            rectangles.append(pg.Rect(x, y + gap / 3, width, height))

            y = height + gap + y

        return rectangles

    def decode_advanced_menu_set(self, advanced_menu_set):

        if len(advanced_menu_set) >= 1:
            self.logo_height = advanced_menu_set[0]
        if len(advanced_menu_set) >= 2:
            self.rect_height = advanced_menu_set[1]
        if len(advanced_menu_set) >= 3:
            self.fract_WIDTH = advanced_menu_set[2]
        if len(advanced_menu_set) >= 4:
            self.button_gap = advanced_menu_set[3]


