# represents one field from board
class Field:
    def __init__(self, value, is_original):
        self.value = value
        self.rect = None
        self.is_original = is_original

    def set_rect(self, rect):
        self.rect = rect

    def get_rect(self):
        return self.rect

    def get_is_original(self):
        return self.is_original

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value
