import pygame
from tictactoe import TicTacToe
from colors import dark_colors, light_colors
from random import randint
from config import symbols, all_symbols

pygame.init()
pygame.mixer.init()

pygame_icon = pygame.image.load('assets/images/tictac.png')
pygame.display.set_icon(pygame_icon)
pygame.display.set_caption("Tic Tac Toe")


def random_color() -> tuple:
    """Returns a tuple that contains a random rgb color"""
    return (randint(0, 255), randint(0, 255), randint(0, 255))


def random_symbol() -> str:
    """Returns a random symbol that is not already in the symbols dictionary"""
    while True:
        i = randint(0, len(all_symbols) - 1)
        if all_symbols[i] not in symbols.values():
            return all_symbols[i]


class Button:
    def __init__(self, coords, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = coords
        self.surface = pygame.Surface(
            self.rect.size, pygame.SRCALPHA).convert_alpha()
        self.surface.blit(self.image, (0, 0))
        pygame.draw.rect(self.surface, (255, 255, 255),
                         (0, 0, self.rect.width - 2, self.rect.height - 2), 2)
        self.click = False

    def clicked(self):
        if self.click and self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return False
        self.click = self.rect.collidepoint(
            pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]
        return self.click


def main():
    # game declaration
    game = TicTacToe(players=2)
    board_size = len(game.board)

    # game config variables
    screen_game_ratio = 1.2
    SCREEN_HEIGHT = 1000
    SCREEN_WIDTH = 1000
    GAME_WIDTH = int(SCREEN_WIDTH / screen_game_ratio)
    GAME_HEIGHT = int(SCREEN_WIDTH / screen_game_ratio)
    GRID_GAP = 40
    GAME_OFFSETX, GAME_OFFSETY = (
        SCREEN_WIDTH - GAME_WIDTH) / 2, (SCREEN_HEIGHT - GAME_HEIGHT) / 2
    DARK_MODE = True
    SHUTDOWN = False
    WON_GAME = 0

    # pygame ui variables
    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    square_size = GAME_WIDTH // board_size
    font = pygame.font.Font('freesansbold.ttf',  square_size - 10)
    lil_font = pygame.font.Font('freesansbold.ttf', square_size // 3)
    dark_mode_img = pygame.image.load("assets/images/darkicon.png")
    dark_mode_button = Button((square_size * 3, 0), dark_mode_img)
    restart_img = pygame.transform.scale(pygame.image.load(
        "assets/images/restart.png"), (square_size // 10, square_size // 10))
    restart_button = Button(
        (square_size * 1.05, square_size * 0.15), restart_img)

    # event catcher loop
    while not SHUTDOWN:
        if restart_button.clicked():
            game.restart()
        if dark_mode_button.clicked():
            DARK_MODE = not DARK_MODE
        if DARK_MODE:
            colors = dark_colors
        else:
            colors = light_colors
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                SHUTDOWN = True
            elif event.type == pygame.MOUSEBUTTONDOWN and not game.winner:
                if(WON_GAME):
                    WON_GAME = 0
                x, y = pygame.mouse.get_pos()
                column = (x - int(GAME_OFFSETX)
                          ) // (GAME_WIDTH // board_size) + 1
                row = (y - int(GAME_OFFSETY)) // (GAME_HEIGHT // board_size) + 1
                if 0 < column <= board_size and 0 < row <= board_size:
                    current_player = game.get_current_player()
                    if not TicTacToe.get_symbol(current_player):
                        symbols[current_player] = random_symbol()
                    unoccupiedSquare = game.make_move((column, row))
                    if not unoccupiedSquare:
                        pygame.mixer.Sound(
                            "assets/sounds/explosion.wav").play()
                    else:
                        pygame.mixer.Sound("assets/sounds/click.wav").play()

            elif event.type == pygame.VIDEORESIZE:
                SCREEN_HEIGHT = event.h
                SCREEN_WIDTH = event.w
                GAME_WIDTH = int(SCREEN_WIDTH / screen_game_ratio)
                GAME_HEIGHT = int(SCREEN_WIDTH / screen_game_ratio)
                GAME_OFFSETX, GAME_OFFSETY = (
                    SCREEN_WIDTH - GAME_WIDTH) / 2, (SCREEN_HEIGHT - GAME_HEIGHT) / 2
                print(GAME_WIDTH)
                screen = pygame.display.set_mode(
                    (event.w, event.h), pygame.RESIZABLE)

        # board initializer
        pygame.draw.rect(screen, colors["background_color"], pygame.Rect(
            0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.draw.rect(screen, colors["lines_color"], pygame.Rect(
            GAME_OFFSETX - (GRID_GAP // board_size), GAME_OFFSETY - (GRID_GAP // board_size), GAME_WIDTH + (GRID_GAP // board_size), GAME_HEIGHT + (GRID_GAP // board_size)))

        # generate grid
        for i, row in enumerate(game.board):
            for j, spot in enumerate(row):
                pos = i * (GAME_WIDTH // board_size) + GAME_OFFSETX, j * \
                    (GAME_HEIGHT // board_size) + GAME_OFFSETY
                x, y = pos
                box = pygame.Rect(
                    x, y, (GAME_WIDTH - GRID_GAP) // board_size, (GAME_HEIGHT - GRID_GAP) // board_size)
                pygame.draw.rect(screen, colors["tile_color"], box)
                if (spot and spot != 0):
                    font_color = colors.get("{}_color".format(spot.lower()))
                    if not font_color:
                        colors["{}_color".format(
                            spot.lower())] = random_color()
                        font_color = colors.get(
                            "{}_color".format(spot.lower()))
                    label = font.render(TicTacToe.get_symbol(TicTacToe.get_number(spot)),
                                        True, font_color)
                    screen.blit(label, label.get_rect(center=box.center))

        # check for a winner
        if winner := game.win():
            if not WON_GAME:
                WON_GAME = 1
                pygame.mixer.Sound("assets/sounds/win.mp3").play()
            screen.fill(colors["background_color"])
            winner_label = font.render(
                winner, True, colors["{}_color".format(winner.lower())])
            winner_label_rect = winner_label.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(winner_label, winner_label_rect)
            text = lil_font.render("won the game!", True, colors["o_color"])
            text_rect = text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
            screen.blit(text, text_rect)

        # add ui buttons
        screen.blit(dark_mode_button.image, dark_mode_button.rect)
        screen.blit(restart_button.image, restart_button.rect)

        pygame.display.flip()


if __name__ == '__main__':
    main()
