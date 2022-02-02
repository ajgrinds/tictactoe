import pygame
from states.base_state import BaseState
from colors import dark_colors
from config import SCREEN_GAME_RATIO


class Button(pygame.sprite.Sprite):
    def __init__(self, id, text):
        super().__init__()
        self.id = id
        self.text = text
        self.rect = pygame.Rect(0, 0, 0, 0)

    def clicked(self):
        return self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]

    def draw(self, screen, colors, font, coords):
        text = font.render(self.text, False, colors["x_color"])
        surface = pygame.Surface(text.get_rect().size, pygame.SRCALPHA).convert_alpha()
        surface.fill(colors["sidebar_color"])
        surface.blit(text, (0, 0))
        self.rect = text.get_rect(center=coords)
        pygame.draw.rect(surface, colors["lines_color"], (0, 0, self.rect.width - 2, self.rect.height - 2), 2)
        screen.blit(surface, self.rect)


class TitleState(BaseState):
    def __init__(self):
        super().__init__(dark_colors)
        self.startButton = Button("start", " start ")
        self.persist = {}
        self.done = False
        self.next = None
        self.font = 0
        self.liler_font = 0

    def resize(self, height, width):
        self.GAME_SIZE = int(min(width, height) // SCREEN_GAME_RATIO)
        self.font = pygame.font.Font('freesansbold.ttf', self.GAME_SIZE // 5)
        self.liler_font = pygame.font.Font('freesansbold.ttf', self.GAME_SIZE // 7)
        screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        return screen

    def start_up(self, persist, screen):
        self.persist = persist
        screen_width, screen_height = screen.get_width(), screen.get_height()
        self.GAME_SIZE = int(min(screen_width, screen_height) // SCREEN_GAME_RATIO)
        self.font = pygame.font.Font('freesansbold.ttf', self.GAME_SIZE // 5)
        self.liler_font = pygame.font.Font('freesansbold.ttf', self.GAME_SIZE // 7)

    def draw(self, screen):
        screen.fill(self.persist["colors"]["background_color"])
        title_label = self.font.render("Tic-Tac-Toe", True, self.persist["colors"]["lines_color"])
        title_label_rect = title_label.get_rect(
            center=(screen.get_width() // 2, screen.get_height() // 4))
        screen.blit(title_label, title_label_rect)
        self.startButton.draw(screen, self.persist["colors"], self.liler_font, (screen.get_width() // 2, screen.get_height() // 2))

    def update(self, screen):
        if self.startButton.clicked():
            self.done = True
            self.next = "game"
            pygame.mixer.Sound("assets/sounds/click.wav").play()
        self.draw(screen)
