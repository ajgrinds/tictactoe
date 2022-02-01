import pygame
from tictactoe import TicTacToe
from colors import dark_colors, light_colors

pygame.init()


class Button:
    def __init__(self, coords, image, scale=None):
        super().__init__()
        self.img = image
        self.image = pygame.transform.scale(self.img, scale)
        self.rect = self.image.get_rect()
        self.rect.center = coords
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

    def resize(self, scale, coords):
        self.image = pygame.transform.scale(self.img, scale)
        self.rect.center = coords


def main():
    SCREEN_HEIGHT = 1000
    SCREEN_WIDTH = 1000
    GAME_SIZE = int(min(SCREEN_WIDTH, SCREEN_HEIGHT) / 1.2)
    GRID_GAP = 30
    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    game = TicTacToe(players=2)
    game_offsetx, game_offsety = (
        SCREEN_WIDTH - GAME_SIZE) / 2, (SCREEN_HEIGHT - GAME_SIZE) / 2
    font = pygame.font.Font('freesansbold.ttf', GAME_SIZE // len(game.board) - 10)
    lil_font = pygame.font.Font('freesansbold.ttf', GAME_SIZE // len(game.board) // 3)
    liler_font = pygame.font.Font('freesansbold.ttf', GAME_SIZE // len(game.board) // 5)
    dark_mode = True
    dark_mode_img = pygame.image.load("images/darkmode.png")
    dark_mode_button = Button((game_offsetx + GAME_SIZE // len(game.board) * 0.7, 30), dark_mode_img, (GAME_SIZE // len(game.board) // 8, GAME_SIZE // len(game.board) // 8))
    restart_img = pygame.image.load("images/restart.png")
    restart_button = Button(
        (game_offsetx + GAME_SIZE // len(game.board) * 0.5, 30), restart_img, (GAME_SIZE // len(game.board) // 10, GAME_SIZE // len(game.board) // 10))

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
                column = (x - int(game_offsetx)) // (GAME_SIZE // 3) + 1
                row = (y - int(game_offsety)) // (GAME_SIZE // 3) + 1
                if 0 < column <= 3 and 0 < row <= 3:
                    game.make_move((column, row))
            elif event.type == pygame.VIDEORESIZE:
                SCREEN_HEIGHT = event.h
                SCREEN_WIDTH = event.w
                GAME_SIZE = int(min(SCREEN_WIDTH, SCREEN_HEIGHT) // 1.2)
                game_offsetx, game_offsety = (
                    SCREEN_WIDTH - GAME_SIZE) / 2, (SCREEN_HEIGHT - GAME_SIZE) / 2
                screen = pygame.display.set_mode(
                    (event.w, event.h), pygame.RESIZABLE)
                font = pygame.font.Font('freesansbold.ttf', GAME_SIZE // len(game.board) - 10)
                lil_font = pygame.font.Font('freesansbold.ttf', GAME_SIZE // len(game.board) // 3)
                liler_font = pygame.font.Font('freesansbold.ttf', GAME_SIZE // len(game.board) // 5)
                dark_mode_button.resize((GAME_SIZE // len(game.board) // 8, GAME_SIZE // len(game.board) // 8), (game_offsetx + GAME_SIZE // len(game.board) * 0.7, 30))
                restart_button.resize((GAME_SIZE // len(game.board) // 10, GAME_SIZE // len(game.board) // 10), (game_offsetx + GAME_SIZE // len(game.board) * 0.5, 30))

        screen.fill(colors["sidebar_color"])
        pygame.draw.rect(screen, colors["background_color"], pygame.Rect(
            0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        player_label = liler_font.render(f"Player: {TicTacToe.get_symbol(game.turn % game.players + 1)}", True, colors[game.turn % game.players + 1])
        screen.blit(player_label, player_label.get_rect(center=(SCREEN_WIDTH // 2, 30)))

        x_label = font.render(TicTacToe.get_symbol(1), True, colors[1])
        o_label = font.render(TicTacToe.get_symbol(2), True, colors[2])

        for i, row in enumerate(game.board):
            for j, spot in enumerate(row):
                pos = i * (GAME_SIZE // len(game.board)) + game_offsetx, j * \
                    (GAME_SIZE // len(game.board)) + game_offsety
                x, y = pos
                box = pygame.Rect(x, y, (GAME_SIZE - GRID_GAP) // len(game.board), (GAME_SIZE - GRID_GAP) // len(game.board))
                pygame.draw.rect(screen, colors["tile_color"], box)
                if spot == TicTacToe.get_symbol(1):
                    screen.blit(x_label, x_label.get_rect(center=(box.centerx, box.centery + GRID_GAP // 2)))
                if spot == TicTacToe.get_symbol(2):
                    screen.blit(o_label, o_label.get_rect(center=(box.centerx, box.centery + GRID_GAP // 2)))

        if winner := game.win():
            screen.fill(colors["background_color"])
            winner_label = font.render(
                TicTacToe.get_symbol(winner), True, colors[2 / (game.turn % game.players + 1)])
            winner_label_rect = winner_label.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
            screen.blit(winner_label, winner_label_rect)
            text = lil_font.render("won the game!", True, colors[game.turn % game.players + 1])
            text_rect = text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)

        screen.blit(dark_mode_button.image, dark_mode_button.rect)
        screen.blit(restart_button.image, restart_button.rect)

        pygame.display.flip()


if __name__ == '__main__':
    main()
