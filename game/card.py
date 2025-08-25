import glob
from enum import Enum

import pygame
import tqdm
from rich import print


class Suit(Enum):
    CLUBS = "clubs"
    SPADES = "spades"
    HEARTS = "hearts"
    DIAMONDS = "diamonds"


class Card:
    def __init__(self, file_path: str, pygame_image_of_card: pygame.Surface):
        self.raw_name = file_path.split("/")[-1]
        self.image = pygame_image_of_card
        self.image_w, self.image_h = self.image.get_size()
        self.suit: Suit = self.determine_suit()
        self.rank: str = self.determine_rank()
        self.value: int = self.determine_value()
        self.dragging: bool = False
        self.in_grid: bool = False
        self.big_image: pygame.Surface = pygame.transform.scale(
            self.image, (self.image_w / 2, self.image_h / 2)
        )
        self.small_image: pygame.Surface = pygame.transform.scale(
            self.image, (self.image_w * 0.06, self.image_h * 0.06)
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

    def resize_image(self, new_height_dimension: int):
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
