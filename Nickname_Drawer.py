from Const_params import WHITE
import pygame

class Nickname_Drawer:
    def __init__(self, font_name, location, surface_size, max_text_size, text=''):
        self.color = WHITE
        self.text = text
        self.location = location
        self.surface_size = surface_size
        self.max_text_size = max_text_size
        self.text_size = max_text_size
        self.font_name = font_name
        self.txt_surface = pygame.font.SysFont(self.font_name, self.text_size).render(self.text, True, self.color)
        self.update_surface()

    def get_Text(self):
        return self.text

    def set_Text(self, text):
        self.text = text
        self.update_surface()

    def setFont(self, font_name):
        self.font_name = font_name

    def draw(self, screen):
        screen.blit(self.txt_surface, self.location)

    def update_surface(self):
        self.text_size = self.max_text_size
        while True:
            font = pygame.font.SysFont(self.font_name, self.text_size)

            self.txt_surface = font.render(self.text, True, self.color)

            if 0 < self.txt_surface.get_rect()[2] - self.txt_surface.get_rect()[0] < self.surface_size[0] and 0 < \
                    self.txt_surface.get_rect()[3] - self.txt_surface.get_rect()[1] < \
                    self.surface_size[1]:
                break
            else:
                self.text_size -= 1