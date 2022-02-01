import pygame
from tictactoe import TicTacToe
from colors import dark_colors, light_colors

pygame.init()


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
    SCREEN_HEIGHT = 1000
    SCREEN_WIDTH = 1000
    GAME_WIDTH = SCREEN_WIDTH // 2
    GAME_HEIGHT = SCREEN_WIDTH // 2
    GRID_GAP = 30
    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    game = TicTacToe(players=2)
    square_size = GAME_WIDTH // len(game.board)
    game_offsetx, game_offsety = (
        SCREEN_WIDTH - GAME_WIDTH) / 2, (SCREEN_HEIGHT - GAME_HEIGHT) / 2
    font = pygame.font.Font('freesansbold.ttf',  square_size - 10)
    lil_font = pygame.font.Font('freesansbold.ttf', square_size // 3)
    dark_mode = True
    dark_mode_img = pygame.transform.scale(pygame.image.load(
        "darkmode.png"), (square_size // 2, square_size // 2))
    dark_mode_button = Button((square_size * 3, 0), dark_mode_img)
    restart_img = pygame.transform.scale(pygame.image.load(
        "restart.png"), (square_size // 10, square_size // 10))
    restart_button = Button(
        (square_size * 1.05, square_size * 0.15), restart_img)

    game = TicTacToe(players=2)

    shutdown = False
    while not shutdown:
        if restart_button.clicked():
            game.restart()
        if dark_mode_button.clicked():
            dark_mode = not dark_mode
        if dark_mode:
            colors = dark_colors
        else:
            colors = light_colors
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                shutdown = True
            elif event.type == pygame.MOUSEBUTTONDOWN and not game.winner:
                x, y = pygame.mouse.get_pos()
                column = (x - int(game_offsetx)) // (GAME_WIDTH // 3) + 1
                row = (y - int(game_offsety)) // (GAME_HEIGHT // 3) + 1
                if 0 < column <= 3 and 0 < row <= 3:
                    game.make_move((column, row))
            elif event.type == pygame.VIDEORESIZE:
                SCREEN_HEIGHT = event.h
                SCREEN_WIDTH = event.w
                GAME_WIDTH = SCREEN_WIDTH // 2
                GAME_HEIGHT = SCREEN_WIDTH // 2
                game_offsetx, game_offsety = (
                    SCREEN_WIDTH - GAME_WIDTH) / 2, (SCREEN_HEIGHT - GAME_HEIGHT) / 2
                screen = pygame.display.set_mode(
                    (event.w, event.h), pygame.RESIZABLE)

        screen.fill(colors["sidebar_color"])
        pygame.draw.rect(screen, colors["background_color"], pygame.Rect(
            0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

        x_label = font.render(TicTacToe.get_symbol(1), True, colors["x_color"])
        o_label = font.render(TicTacToe.get_symbol(2), True, colors["o_color"])
        screen.blit(dark_mode_button.image, dark_mode_button.rect)

        for i, row in enumerate(game.board):
            for j, spot in enumerate(row):
                pos = i * (GAME_WIDTH // len(game.board)) + game_offsetx, j * \
                    (GAME_HEIGHT // len(game.board)) + game_offsety
                x, y = pos
                pygame.draw.rect(screen, (23, 23, 23), pygame.Rect(
                    x, y, (GAME_WIDTH - GRID_GAP) // len(game.board), (GAME_HEIGHT - GRID_GAP) // len(game.board)))
                if spot == TicTacToe.get_symbol(1):
                    screen.blit(x_label, pos)
                if spot == TicTacToe.get_symbol(2):
                    screen.blit(o_label, pos)

        if winner := game.win():
            screen.fill(colors["background_color"])
            winner_label = font.render(
                TicTacToe.get_symbol(winner), True, colors["x_color"])
            winner_label_rect = winner_label.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(winner_label, winner_label_rect)
            text = lil_font.render("won the game!", True, colors["o_color"])
            text_rect = text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
            screen.blit(text, text_rect)

        screen.blit(dark_mode_button.image, dark_mode_button.rect)
        screen.blit(restart_button.image, restart_button.rect)

        pygame.display.flip()


if __name__ == '__main__':
    main()
