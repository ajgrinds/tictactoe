from tictactoe import TicTacToe
from states.base_state import BaseState
import pygame
from colors import dark_colors, light_colors
from random import randint
from config import symbols, all_symbols, SCREEN_GAME_RATIO, GRID_GAP



def random_color() -> tuple:
    """Returns a tuple that contains a random rgb color"""
    return (randint(0, 255), randint(0, 255), randint(0, 255))


def random_symbol() -> str:
    """Returns a random symbol that is not already in the symbols dictionary"""
    while True:
        i = randint(0, len(all_symbols) - 1)
        if all_symbols[i] not in symbols.values():
            return all_symbols[i]


class GameState(BaseState):
    def __init__(self, game: TicTacToe = None, players: int = 2, colors: dict = dark_colors):
        super().__init__(colors=colors)
        if game is None:
            self.game = TicTacToe(players=players)
        else:
            self.game = game

        self.board_size = len(self.game.board)
        self.done = False
        self.next = None
        self.persist = {}

        self.GAME_OFFSETX = 0
        self.GAME_OFFSETY = 0
        self.GAME_SIZE = 0
        self.font = pygame.font.Font('freesansbold.ttf', self.square_size - 10)
        self.lil_font = pygame.font.Font('freesansbold.ttf', self.square_size // 3)
        self.liler_font = pygame.font.Font('freesansbold.ttf', self.square_size // 5)

        self.pressed = True

    @property
    def square_size(self):
        return self.GAME_SIZE // self.board_size

    def resize(self, height, width):
        self.GAME_SIZE = int(min(width, height) // SCREEN_GAME_RATIO)
        self.GAME_OFFSETX, self.GAME_OFFSETY = (width - self.GAME_SIZE) / 2, (height - self.GAME_SIZE) / 2
        self.font = pygame.font.Font('freesansbold.ttf', self.square_size - 10)
        self.lil_font = pygame.font.Font('freesansbold.ttf', self.square_size // 3)
        self.liler_font = pygame.font.Font('freesansbold.ttf', self.square_size // 5)
        screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.persist["dark_mode_button"].resize((min(width, height) // 15, min(width, height) // 15), (width * 0.5 - min(width, height) * 0.4, height // 25))
        self.persist["restart_button"].resize((min(width, height) // 15, min(width, height) // 15), (width * 0.5 - min(width, height) * 0.3, height // 25))
        return screen

    def start_up(self, persist, screen):
        pygame.mixer.music.set_volume(0.1)
        self.persist = persist
        screen_width, screen_height = screen.get_width(), screen.get_height()
        self.GAME_SIZE = int(min(screen_width, screen_height) // SCREEN_GAME_RATIO)
        self.GAME_OFFSETX, self.GAME_OFFSETY = (screen_width - self.GAME_SIZE) / 2, (screen_height - self.GAME_SIZE) / 2
        self.font = pygame.font.Font('freesansbold.ttf', self.square_size - 10)
        self.lil_font = pygame.font.Font('freesansbold.ttf', self.square_size // 3)
        self.liler_font = pygame.font.Font('freesansbold.ttf', self.square_size // 5)
        self.persist["dark_mode_button"].resize((min(screen_width, screen_height) // 15, min(screen_width, screen_height) // 15),
                                                (screen_width * 0.5 - min(screen_width, screen_height) * 0.4, screen_height // 25))
        self.persist["restart_button"].resize((min(screen_width, screen_height) // 15, min(screen_width, screen_height) // 15),
                                              (screen_width * 0.5 - min(screen_width, screen_height) * 0.3, screen_height // 25))

    def draw(self, screen):
        screen.fill(self.persist["colors"]["background_color"])

        # generate grid
        for i, row in enumerate(self.game.board):
            for j, spot in enumerate(row):
                pos = i * (self.square_size) + self.GAME_OFFSETX, j * \
                      (self.square_size) + self.GAME_OFFSETY
                x, y = pos
                box = pygame.Rect(
                    x, y, (self.GAME_SIZE - GRID_GAP) // self.board_size, (self.GAME_SIZE - GRID_GAP) // self.board_size)
                pygame.draw.rect(screen, self.persist["colors"]["tile_color"], box)
                if spot and spot != 0:
                    font_color = self.persist["colors"].get("{}_color".format(spot.lower()))
                    if not font_color:
                        self.persist["colors"]["{}_color".format(
                            spot.lower())] = random_color()
                        font_color = self.persist["colors"].get(
                            "{}_color".format(spot.lower()))
                    label = self.font.render(TicTacToe.get_symbol(TicTacToe.get_number(spot)),
                                        True, font_color)
                    screen.blit(label, label.get_rect(center=box.center))

        current_player = self.game.get_current_player()
        if not TicTacToe.get_symbol(current_player):
            symbols[current_player] = random_symbol()

        font_color = self.persist["colors"].get("{}_color".format(symbols[current_player].lower()))
        if not font_color:
            self.persist["colors"]["{}_color".format(symbols[current_player].lower())] = random_color()
            font_color = self.persist["colors"].get("{}_color".format(symbols[current_player].lower()))
        player_label = self.liler_font.render(f"Player: {symbols[current_player]}", True, font_color)
        screen.blit(player_label, player_label.get_rect(center=(screen.get_width() // 2, 30)))

        screen.blit(self.persist["dark_mode_button"].image,  self.persist["dark_mode_button"].rect)
        screen.blit(self.persist["restart_button"].image, self.persist["restart_button"].rect)

    def update(self, screen):
        if self.persist["restart_button"].clicked():
            self.game.restart()
            pygame.mixer.Sound("assets/sounds/click.wav").play()
        if self.persist["dark_mode_button"].clicked():
            self.persist["colors"] = light_colors if self.persist["colors"] == dark_colors else dark_colors
            pygame.mixer.Sound("assets/sounds/click.wav").play()

        if pygame.mouse.get_pressed()[0] and not self.game.winner:
            if not self.pressed:
                x, y = pygame.mouse.get_pos()
                column = (x - int(self.GAME_OFFSETX)) // self.square_size + 1
                row = (y - int(self.GAME_OFFSETY)) // self.square_size + 1
                if 0 < column <= self.board_size and 0 < row <= self.board_size:
                    current_player = self.game.get_current_player()
                    if not TicTacToe.get_symbol(current_player):
                        symbols[current_player] = random_symbol()
                    if not self.game.make_move((column, row)):
                        pygame.mixer.Sound(
                            "assets/sounds/explosion.wav").play()
                    else:
                        pygame.mixer.Sound("assets/sounds/click.wav").play()
                self.pressed = True
        else:
            self.pressed = False

        # check for a winner
        if winner := self.game.win():
            self.next = "win"
            self.done = True
            self.persist["winner"] = winner

        self.draw(screen)
