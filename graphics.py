import pygame
from tictactoe import TicTacToe

pygame.init()
SCREEN_HEIGHT = 1000
SCREEN_WIDTH = 1000


def main():
    font = pygame.font.Font('freesansbold.ttf', 4 * SCREEN_HEIGHT // 10)
    lil_font = pygame.font.Font('freesansbold.ttf', SCREEN_HEIGHT // 10)
    x_label = font.render(TicTacToe.get_symbol(1), True, (0, 0, 0))
    o_label = font.render(TicTacToe.get_symbol(2), True, (0, 0, 0))
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    game = TicTacToe(players=2)

    shutdown = False
    while not shutdown:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                shutdown = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if x <= SCREEN_WIDTH // 3:
                    column = 1
                elif SCREEN_WIDTH // 3 < x <= 2 * SCREEN_WIDTH // 3:
                    column = 2
                else:
                    column = 3

                if y <= SCREEN_HEIGHT // 3:
                    row = 1
                elif SCREEN_HEIGHT // 3 < y <= 2 * SCREEN_HEIGHT // 3:
                    row = 2
                else:
                    row = 3

                game.make_move((column, row))

        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(SCREEN_WIDTH // 3 - 10, 0, 20, SCREEN_HEIGHT))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(2 * SCREEN_WIDTH // 3 - 10, 0, 20, SCREEN_HEIGHT))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, SCREEN_HEIGHT // 3 - 10, SCREEN_WIDTH, 20))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 2 * SCREEN_HEIGHT // 3 - 10, SCREEN_WIDTH, 20))

        for i, row in enumerate(game.board):
            for j, spot in enumerate(row):
                if spot == TicTacToe.get_symbol(1):
                    screen.blit(x_label, (i * (SCREEN_WIDTH // 3), j * (SCREEN_HEIGHT // 3)))
                if spot == TicTacToe.get_symbol(2):
                    screen.blit(o_label, (i * (SCREEN_WIDTH // 3), j * (SCREEN_HEIGHT // 3)))

        if winner := game.win():
            screen.fill((255, 255, 255))
            winner_label = font.render(TicTacToe.get_symbol(winner), True, (0, 0, 0))
            winner_label_rect = winner_label.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
            screen.blit(winner_label, winner_label_rect)
            text = lil_font.render("won the game!", True, (0, 0, 0))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)

        pygame.display.flip()


if __name__ == '__main__':
    main()
