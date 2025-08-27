import glob
from enum import Enum

import pygame
import tqdm
from colors import TEXT_COLOR
from configs import FONT
from rich import print


class Suit(Enum):
    CLUBS = "clubs"
    SPADES = "spades"
    HEARTS = "hearts"
    DIAMONDS = "diamonds"


class Card:
    def __init__(self, file_path: str, pygame_image_of_card: pygame.Surface):
        self.file_path: str = file_path
        self.raw_name: str = file_path.split("/")[-1]

        # GAME ATTRIBUTES
        self.suit: Suit = self.determine_suit()
        self.rank: str = self.determine_rank()
        self.value: int = self.determine_value()
        self.short_hand: str = f"{self.rank}.{str(self.suit)[0]}"

        # PYGAME ATTRIBUTES
        self.image: pygame.Surface = pygame_image_of_card
        self.rect: pygame.Rect = self.image.get_rect()
        self.original_size: pygame.Rect = self.rect
        self.image_w, self.image_h = self.image.get_size()
        self.backside_up: bool = False
        self.dragging: bool = False
        self.in_grid: bool = False
        self.display_image: pygame.Surface = self.resize_image(200)
        self.big_image: pygame.Surface = self.resize_image(self.original_size[1] / 2)
        self.small_image: pygame.Surface = self.resize_image(
            self.original_size[1] * 0.06
        )
        self.display_short_hand: pygame.Surface = FONT.render(
            self.short_hand, True, TEXT_COLOR
        )

    def determine_suit(self):
        if "clubs" in self.raw_name:
            return Suit.CLUBS
        elif "spades" in self.raw_name:
            return Suit.SPADES
        elif "hearts" in self.raw_name:
            return Suit.HEARTS
        elif "diamonds" in self.raw_name:
            return Suit.DIAMONDS

    def determine_rank(self):
        if "joker" in self.raw_name:
            return "W"
        elif "ace" in self.raw_name:
            return "A"
        elif "king" in self.raw_name:
            return "K"
        elif "queen" in self.raw_name:
            return "Q"
        elif "jack" in self.raw_name:
            return "J"
        return self.raw_name.split("_")[0]

    def determine_value(self):
        if self.rank == "W":
            return 20
        elif self.rank in ["J", "Q", "K"]:
            return 10
        elif self.rank == "A":
            return 1
        else:
            return int(self.rank)

    def resize_image(self, new_height_dimension: int) -> pygame.Surface:
        ratio = new_height_dimension / self.image_h
        return pygame.transform.smoothscale(
            self.image, (self.image_w * ratio, self.image_h * ratio)
        )

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def __repr__(self):
        return self.__str__()


def read_in_card_images():
    cards = [
        Card(image_file, pygame.image.load(image_file))
        for image_file in tqdm.tqdm(glob.glob("card_resources/PNG/*.png"))
    ]
    print(len(cards))
    return cards
