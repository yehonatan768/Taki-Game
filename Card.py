
class Card(object):
    def __init__(self, value, color, image=None, serial_number=None):
        self.color = color
        self.value = value
        self.image = image
        self.serial_number = serial_number

    def get_value(self):
        return self.value

    def get_serial_number(self):
        return self.serial_number

    def get_image(self):
        return self.image

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color

    def show(self):
        return f'{self.value}_{self.color}'