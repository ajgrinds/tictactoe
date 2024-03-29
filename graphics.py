import pygame
from states.game_state import GameState
from states.win_state import WinState
from states.title_state import TitleState
from colors import dark_colors
from config import all_symbols
import random

pygame.init()
pygame.mixer.init()
print()
print()

pygame_icon = pygame.image.load('assets/images/tictac.png')
pygame.display.set_icon(pygame_icon)
pygame.display.set_caption("Tic Tac Toe")


class Button(pygame.sprite.Sprite):
    def __init__(self, coords, image, scale=None):
        super().__init__()
        self.img = image
        if scale is not None:
            self.image = pygame.transform.scale(self.img, scale)
        else:
            self.image = image
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
    names = ["moose", "energy", "boss", "lounge"]
    random.shuffle(names)
    pygame.mixer.music.load(f"assets/sounds/{names[0]}.wav")
    for name in names:
        pygame.mixer.music.queue(f"assets/sounds/{name}.wav")

    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.1)

    print("Sorry, I havent made this part digital yet...\nAlso volume warning.")
    while not (num_players := input("How many players would you like?\n>>> ").strip()).isdigit():
        num_players = int(num_players)
        if 0 > num_players or num_players > len(all_symbols):
            print("I thought of everything... can't fool me")
        else:
            print("Come on now, already trying to break it. Try again.")
    print("Okay, look for the pygame window. Im not sure why it doesnt auto bring it to the front.")

    # game config variables
    height = 1000
    width = 1000
    # pygame ui variables
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

    dark_mode_img = pygame.image.load("assets/images/darkicon.png")
    dark_mode_button = Button((width * 0.5 - min(width, height) * 0.4, height // 25), dark_mode_img, (min(width, height) // 15, min(width, height) // 15))
    restart_img = pygame.image.load("assets/images/restart.png")
    restart_button = Button((width * 0.5 - min(width, height) * 0.3, height // 25), restart_img, (min(width, height) // 15, min(width, height) // 15))
    persist = {
        "restart_button": restart_button,
        "dark_mode_button": dark_mode_button,
        "dark_mode": True,
        "colors": dark_colors
    }

    states = {
        "title": TitleState(),
        "win": WinState(),
        "game": GameState(players=int(num_players))
    }

    current_state = states["title"]
    SHUTDOWN = False
    current_state.start_up(persist=persist, screen=screen)

    # event catcher loop
    while not SHUTDOWN:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                SHUTDOWN = True
            elif event.type == pygame.VIDEORESIZE:
                screen = current_state.resize(event.h, event.w)

        current_state.update(screen=screen)
        if current_state.done:
            current_state.cleanup()
            current_state = states[current_state.next]
            current_state.start_up(persist, screen)

        pygame.display.flip()

    current_state.cleanup()


if __name__ == '__main__':
    main()
