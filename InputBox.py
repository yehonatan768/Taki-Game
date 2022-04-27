from Const_params import WHITE, BLACK
import pygame

class InputBox:
    # Constructor ------------------------------------------------- #
    def __init__(self, x, y, w, h, font, text_size, text='', backspace_pressed=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.clicked_rect = pygame.Rect(x - 2, y - 2, w + 4, h + 4)
        self.color = WHITE
        self.text = text
        self.backspace_pressed = backspace_pressed
        self.text_size = text_size
        self.font = pygame.font.Font(font, self.text_size)
        self.txt_surface = self.font.render(self.text, True, self.color)
        self.active = False

    def getText(self):
        return self.text

    def getActive(self):
        return self.active

    # Setters ---------------------------------------------------- #
    def setFont(self, font):
        self.font = pygame.font.Font(font, self.text_size)

    def setTextSize(self, text_size):
        self.text_size = text_size

    # Functions -------------------------------------------------- #
    def handle_event_save(self, event, click, screen):
        # Prepare the text to be saved as nickname.
        if event.type == pygame.MOUSEBUTTONDOWN and click[0] == 1:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = BLACK if self.active else WHITE

        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.color = WHITE
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    screen.set_key_repeat(100, 100)
                    self.delete()

                elif len(self.text) < 16:
                    self.text += event.unicode
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE:
                    screen.set_key_repeat(500, 200)

                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, WHITE)
        else:
            self.txt_surface = self.font.render(self.text, True, WHITE)

    def delete(self):
        self.text = self.text[:-1]
        self.txt_surface = self.font.render(self.text, True, WHITE)

    def update(self):
        # Resize the box if the text is too long.
        width = max(350, self.txt_surface.get_width() + 10)
        self.rect.w = width
        self.clicked_rect.w = width + 4

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        if self.active:
            pygame.draw.rect(screen, WHITE, self.rect, 8)
            pygame.draw.rect(screen, self.color, self.clicked_rect, 4)
            self.txt_surface = self.font.render(self.text, True, WHITE)
        else:
            pygame.draw.rect(screen, self.color, self.rect, 4)
            self.txt_surface = self.font.render(self.text, True, self.color)