from pygame import mixer
import pygame

class PygameSetup:
    def __init__(self, p_X, p_Y):
        pygame.init()
        pygame.key.set_repeat(500, 200)
        pygame.display.set_caption('Taki')
        pygame.display.set_icon(pygame.image.load('pic\\Interface\\TAKI_lcon.png'))
        self.screen = pygame.display.set_mode((p_X, p_Y))
        self.clock = pygame.time.Clock()

    def getScreen(self):
        return self.screen

    @staticmethod
    def set_key_repeat(delay, interval):
        pygame.key.set_repeat(delay, interval)

    def update(self):
        pygame.display.flip()
        self.clock.tick(100)

    def update_fps(self, font):
        return font.render(str(int(self.clock.get_fps())), 1, [255, 255, 255])

    def blit(self, pic, x):
        self.screen.blit(pic, x)

    def fill(self, color):
        self.screen.fill(color)

    @staticmethod
    def loadify(image):
        return pygame.image.load(image).convert_alpha()

    def close(self):
        self.close()

    def draw_text(self, text, color, font, size, x, y):
        font1 = pygame.font.Font(font, size)
        surface = font1.render(text, True, color)
        self.screen.blit(surface, (x, y))

# Server & Client IP, PORT
IP = '127.0.0.1'
PORT = 8080


WHITE = [255, 255, 255]
BLACK = [0, 0, 0]

# parameters
screen = PygameSetup(1915, 1005)

nickname_clicked = screen.loadify('pic\\Interface\\click_nickname.png')
# win/lose screen
exit_button_win_lose_screen = screen.loadify('pic\\Interface\\exit_button_win_screen copy.png')
play_again_button_win_lose_screen = screen.loadify('pic\\Interface\\play_again_button_win_screen copy.png')
lose_screen_background = screen.loadify('pic\\Interface\\lose_screen.png')
win_screen_background = screen.loadify('pic\\Interface\\win_screen.png')

# menu buttons
menu = screen.loadify('pic\\Interface\\menu.png')
bold_start_button = screen.loadify('pic\\Interface\\start_button.png')
how_to_play_button = screen.loadify('pic\\Interface\\how_to_play_button.png')
exit_button = screen.loadify('pic\\Interface\\exit_button.png')

# rules screen buttons
rules_screen = screen.loadify('pic\\Interface\\game_rules.png')
return_button_rules = screen.loadify('pic\\Interface\\return_button_menu.png')

# game buttons
game_screen = screen.loadify('pic\\Interface\\game_screen.png')
client_turn_screen = screen.loadify('pic\\Interface\\client_turn_screen.png')
front_turn_screen = screen.loadify('pic\\Interface\\front_turn_screen.png')
left_side_turn_screen = screen.loadify('pic\\Interface\\left_side_turn_screen.png')
right_side_turn_screen = screen.loadify('pic\\Interface\\right_side_turn_screen.png')

card_bar = screen.loadify('pic\\Interface\\card_bar.png')
chat_button = screen.loadify('pic\\Interface\\chat_button.png')
return_button_game = screen.loadify('pic\\Interface\\return_button_game.png')
left_button_game = screen.loadify('pic\\Interface\\left_button_game_broad.png')
bold_left_button_game = screen.loadify('pic\\Interface\\bold_left_button_game_broad.png')
right_button_game = screen.loadify('pic\\Interface\\right_button_game_broad.png')
bold_right_button_game = screen.loadify('pic\\Interface\\bold_right_button_game_broad.png')

# music buttons
bold_music_on_main_button = screen.loadify('pic\\Interface\\bold_Music_On_Client_Interface.png')
bold_music_off_main_button = screen.loadify('pic\\Interface\\bold_Music_Off_Client_Interface.png')
music_on_main_button = screen.loadify('pic\\Interface\\Music_On_Client_Interface.png')
music_off_main_button = screen.loadify('pic\\Interface\\Music_Off_Client_Interface.png')

muted_vol = screen.loadify('pic\\Interface\\muted_music.png')
low_vol = screen.loadify('pic\\Interface\\low_volume_music.png')
med_vol = screen.loadify('pic\\Interface\\music_medium_volume.png')
high_vol = screen.loadify('pic\\Interface\\Music_high_Volume.png')

# sounds
buttons_s = mixer.Sound('music\\click.wav')
buttons_s.set_volume(5.1)

# dict cards for easy access
pic_cards = dict()

for value in ['1', 'plus_2', '3', '4', '5', '6', '7', '8', '9', 'taki', 'plus', 'stop', 'change_direction', 'change']:
    for c in ['red', 'blue', 'green', 'yellow']:
        pic_cards[value + '_' + c] = screen.loadify('pic\\Taki_Cards\\' + str(value) + '_' + str(c) + '.png')

pic_cards['taki_colorful'] = screen.loadify('pic\\Taki_Cards\\taki_colorful.png')
pic_cards['change_colorful'] = screen.loadify('pic\\Taki_Cards\\change_colorful.png')
pic_cards['choose_color'] = screen.loadify('pic\\Taki_Cards\\choose_color.png')

half_card_back = screen.loadify('pic\\Taki_Cards\\back_card.png')
card_blank = screen.loadify('pic\\Taki_Cards\\blank_card.png')
card_back = screen.loadify('pic\\Taki_Cards\\full_back_card.png')


def search(name):
    return pic_cards[name]
