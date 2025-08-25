import random
import sys

import pygame
from configs import BLACK, IMAGE_TYPE, SCREEN_HEIGHT, SCREEN_WIDTH


class GameObject:
    def __init__(self, image, starting_height, starting_width, speed):
        self.speed = speed
        self.direction = 1
        self.image = image
        self.pos = image.get_rect().move(starting_width, starting_height)

    def move(self):
        self.pos = self.pos.move(self.speed * self.direction, 0)
        if self.pos.right > SCREEN_WIDTH:
            self.direction = -1
        elif self.pos.left < 0:
            self.direction = 1


def load_in_sudoku_digits(suit: str, starting_width: int) -> list:
    objects = []
    for index, x in enumerate(random.sample(range(9), 9)):
        if x == 0:
            card_obj = pygame.image.load(
                f"card_resources/{IMAGE_TYPE}/ace_of_{suit}.{IMAGE_TYPE.lower()}"
            ).convert()
        else:
            card_obj = pygame.image.load(
                f"card_resources/{IMAGE_TYPE}/{x + 1}_of_{suit}.{IMAGE_TYPE.lower()}"
            ).convert()
        # speed / 3 so they move in groups of 3
        o = GameObject(card_obj, index * 45, starting_width, index)
        objects.append(o)
    return objects


def loading_screen():
    screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
    clock = pygame.time.Clock()

    # Create a sample surface to blit
    background = pygame.Surface((SCREEN_HEIGHT, SCREEN_WIDTH))
    background.fill(BLACK)
    screen.blit(background, (0, 0))
    spades = load_in_sudoku_digits("spades", 0)
    hearts = load_in_sudoku_digits("hearts", 250)
    clubs = load_in_sudoku_digits("clubs", 500)
    objects = {
        "spades": spades,
        "hearts": hearts,
        "clubs": clubs,
    }
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        # load objects into background at their current position
        # this happens in the while True so it is a smoother animation
        # and there are no visual lines while moving
        for suit, cards in objects.items():
            for card in cards:
                screen.blit(background, card.pos, card.pos)
        # now move them
        for suit, cards in objects.items():
            for card in cards:
                card.move()
                screen.blit(card.image, card.pos)
        pygame.display.update()
        clock.tick(120)


if __name__ == "__main__":
    loading_screen()
