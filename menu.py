import pygame as pg


class Menu:
    def __init__(self, rectangle, window):
        self.rectangle = rectangle
        self.window = window
        self.messages = {
            "valid": "Congratulations. You completed this puzzle",
            "invalid": "You made a mistake somewhere. Try to find it",
            "in progress": "Good luck"
        }
        self.key_to_message = "in progress"

    def set_key(self, key):
        self.key_to_message = key

    def show(self):
        pg.draw.rect(self.window, (230, 255, 255), self.rectangle)
        font = pg.font.Font(None, 50)
        font_color = (0, 0, 0)
        text = font.render(self.messages.get(self.key_to_message), True, font_color)
        self.window.blit(text, self.rectangle)
