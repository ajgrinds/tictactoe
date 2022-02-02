import pygame
from states.base_state import BaseState
from colors import dark_colors
from config import SCREEN_GAME_RATIO


class WinState(BaseState):
    def __init__(self):
        super().__init__(dark_colors)
        self.persist = {}
        self.done = False
        self.next = None
        self.GAME_SIZE = 0
        self.font = 0
        self.lil_font = 0
        self.liler_font = 0
        self.played = False

    @property
    def square_size(self):
        return self.GAME_SIZE // 3

    def resize(self, height, width):
        self.GAME_SIZE = int(min(width, height) // SCREEN_GAME_RATIO)
        self.font = pygame.font.Font('freesansbold.ttf', self.square_size - 10)
        self.lil_font = pygame.font.Font('freesansbold.ttf', self.square_size // 3)
        self.liler_font = pygame.font.Font('freesansbold.ttf', self.square_size // 5)
        screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.persist["dark_mode_button"].resize((min(width, height) // 15, min(width, height) // 15), (width * 0.5 - min(width, height) * 0.4, height // 25))
        self.persist["restart_button"].resize((min(width, height) // 15, min(width, height) // 15), (width * 0.5 - min(width, height) * 0.3, height // 25))
        return screen

    def start_up(self, persist, screen):
        pygame.mixer.music.set_volume(0.5)
        self.persist = persist
        screen_width, screen_height = screen.get_width(), screen.get_height()
        self.GAME_SIZE = int(min(screen_width, screen_height) // SCREEN_GAME_RATIO)
        self.font = pygame.font.Font('freesansbold.ttf', self.square_size - 10)
        self.lil_font = pygame.font.Font('freesansbold.ttf', self.square_size // 3)
        self.liler_font = pygame.font.Font('freesansbold.ttf', self.square_size // 5)

    def draw(self, screen):
        screen.fill(self.persist["colors"]["background_color"])
        winner_label = self.font.render(self.persist["winner"], True,
                                        self.persist["colors"]["{}_color".format(self.persist["winner"].lower())])
        winner_label_rect = winner_label.get_rect(
            center=(screen.get_width() // 2, screen.get_height() // 3))
        screen.blit(winner_label, winner_label_rect)
        text = self.lil_font.render("won the game!", True, self.persist["colors"]["lines_color"])
        text_rect = text.get_rect(
            center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, text_rect)

    def update(self, screen):
        if not self.played:
            pygame.mixer.Sound("assets/sounds/win.wav").play()
            self.played = True
        self.draw(screen)
