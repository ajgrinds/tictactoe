import pygame
from tictactoe import TicTacToe
from colors import dark_colors, light_colors

pygame.init()
SCREEN_HEIGHT = 400
SCREEN_WIDTH = 500
SQUARE_SIZE = min(SCREEN_WIDTH, SCREEN_HEIGHT)


class Button:
    def __init__(self, coords, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = coords
        self.surface = pygame.Surface(self.rect.size, pygame.SRCALPHA).convert_alpha()
        self.surface.blit(self.image, (0, 0))
        pygame.draw.rect(self.surface, (255, 255, 255), (0, 0, self.rect.width - 2, self.rect.height - 2), 2)
        self.click = False

    def clicked(self):
        if self.click and self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return False
        self.click = self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]
        return self.click


def main():
    font = pygame.font.Font('freesansbold.ttf', 4 * SQUARE_SIZE // 10)
    lil_font = pygame.font.Font('freesansbold.ttf', SQUARE_SIZE // 10)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    dark_mode = True
    dark_mode_img = pygame.transform.scale(pygame.image.load("darkmode.png"), (SQUARE_SIZE // 10, SQUARE_SIZE // 10))
    dark_mode_button = Button((SQUARE_SIZE * 1.05, 0), dark_mode_img)

    lines = [
        pygame.Rect(SQUARE_SIZE // 3 - SQUARE_SIZE // 100, SQUARE_SIZE // 50, SQUARE_SIZE // 50,
                    SQUARE_SIZE - SQUARE_SIZE // 50),
        pygame.Rect(2 * SQUARE_SIZE // 3 - SQUARE_SIZE // 100, SQUARE_SIZE // 50, SQUARE_SIZE // 50,
                    SQUARE_SIZE - SQUARE_SIZE // 50),
        pygame.Rect(SQUARE_SIZE // 50, SQUARE_SIZE // 3 - SQUARE_SIZE // 100, SQUARE_SIZE - SQUARE_SIZE // 50,
                    SQUARE_SIZE // 50),
        pygame.Rect(SQUARE_SIZE // 50, 2 * SQUARE_SIZE // 3 - SQUARE_SIZE // 100, SQUARE_SIZE - SQUARE_SIZE // 50,
                    SQUARE_SIZE // 50)
    ]

    game = TicTacToe(players=2)

    shutdown = False
    while not shutdown:
        if dark_mode_button.clicked():
            dark_mode = not dark_mode
        if dark_mode:
            colors = dark_colors
        else:
            colors = light_colors
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                shutdown = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                row = column = False
                if x <= SQUARE_SIZE // 3:
                    column = 1
                elif SQUARE_SIZE // 3 < x <= 2 * SQUARE_SIZE // 3:
                    column = 2
                elif 2 * SQUARE_SIZE // 3 < x <= SQUARE_SIZE:
                    column = 3

                if y <= SQUARE_SIZE // 3:
                    row = 1
                elif SQUARE_SIZE // 3 < y <= 2 * SQUARE_SIZE // 3:
                    row = 2
                elif 2 * SQUARE_SIZE // 3 < y <= SQUARE_SIZE:
                    row = 3

                if column and row:
                    game.make_move((column, row))

        screen.fill(colors["sidebar_color"])
        pygame.draw.rect(screen, colors["background_color"], pygame.Rect(0, 0, SQUARE_SIZE, SQUARE_SIZE))

        screen.blit(dark_mode_button.image, dark_mode_button.rect)

        x_label = font.render(TicTacToe.get_symbol(1), True, colors["x_color"])
        o_label = font.render(TicTacToe.get_symbol(2), True, colors["o_color"])
        for i, row in enumerate(game.board):
            for j, spot in enumerate(row):
                if spot == TicTacToe.get_symbol(1):
                    screen.blit(x_label, (i * (SQUARE_SIZE // 3), j * (SQUARE_SIZE // 3)))
                if spot == TicTacToe.get_symbol(2):
                    screen.blit(o_label, (i * (SQUARE_SIZE // 3), j * (SQUARE_SIZE // 3)))

        for line in lines:
            pygame.draw.rect(screen, colors["lines_color"], line)

        if winner := game.win():
            screen.fill(colors["background_color"])
            winner_label = font.render(TicTacToe.get_symbol(winner), True, colors["x_color"])
            winner_label_rect = winner_label.get_rect(center=(SQUARE_SIZE // 2, SQUARE_SIZE // 3))
            screen.blit(winner_label, winner_label_rect)
            text = lil_font.render("won the game!", True, colors["o_color"])
            text_rect = text.get_rect(center=(SQUARE_SIZE // 2, SQUARE_SIZE // 2))
            screen.blit(text, text_rect)

        pygame.display.flip()


if __name__ == '__main__':
    main()
