import random
import sys

import matplotlib.pyplot as plt
import pygame
from card import read_in_card_images
from configs import (
    BLACK,
    BLUE,
    GREEN,
    RED,
    WHITE,
    get_dimensions,
    get_dimensions_from_height,
)
from rich import print


def debugging_function(dimensions):
    """
    throw everything in here you want to run just for debugging
    """
    boxes_center_points = dimensions["play_area_centers"]
    plt.scatter(
        x=[i[0] for i in boxes_center_points], y=[j[1] for j in boxes_center_points]
    )
    plt.show()
    card = pygame.image.load("card_resources/PNG/ace_of_spades.png")
    w_, h_ = card.get_size()
    print(card.get_size())
    ratio_small = dimensions["image_size"] / h_
    ratio_big = 0.5
    print(ratio_small, ratio_big)
    small_card = pygame.transform.scale(card, (w_ * ratio_small, h_ * ratio_small))
    print(small_card.get_size())


def setup_screens(dims: dict[str, int]) -> tuple[pygame.Surface, pygame.Surface]:
    screen = pygame.display.set_mode(
        (dims["screen_width"], dims["screen_height"]), pygame.RESIZABLE
    )
    pygame.display.set_caption("Cardoku")
    screen.fill(BLACK)
    play_area = pygame.Surface((dims["play_area"], dims["play_area"]))
    play_area.fill(BLUE)
    build_grid(play_area, dims["play_area"], dims["main_line_width"])
    boxes = setup_subscreens(dims["inner_grid"], dims["inner_line_width"])
    return screen, play_area, boxes


def setup_subscreens(
    inner_grid_size: int,
    line_size: int,
) -> tuple[pygame.Surface, pygame.Surface]:
    """
    Returns 9 subgrids to be used for each box"""
    boxes = []
    for _ in range(9):
        surface = pygame.Surface((inner_grid_size, inner_grid_size))
        surface.fill(GREEN)
        build_grid(surface, inner_grid_size, line_size)
        boxes.append(surface)
    return boxes


def build_grid(
    play_area_screen: pygame.Surface,
    side_length: int,
    line_width: int,
) -> None:
    # vertical lines
    for x in range(1, 3):
        pygame.draw.line(
            play_area_screen,
            WHITE,
            (x * (side_length / 3), 0),
            (x * (side_length / 3), side_length),
            line_width,
        )

    # horizontal lines
    for y in range(1, 3):
        pygame.draw.line(
            play_area_screen,
            WHITE,
            (0, y * (side_length / 3)),
            (side_length, y * (side_length / 3)),
            line_width,
        )


def draw_board(screen, play_area, boxes, dimensions):
    # MAIN PLAY AREA
    screen.blit(
        play_area,
        (
            (dimensions["screen_width"] - dimensions["play_area"]) / 2,
            (dimensions["screen_height"] - dimensions["play_area"]) / 4,
        ),
    )
    # INDIVIDUAL BOXES
    for box, centers in zip(boxes, dimensions["play_area_centers"]):
        play_area.blit(
            box,
            (
                centers[0],
                centers[1],
            ),
        )


def main():
    pygame.init()
    cards = read_in_card_images()
    DEFAULT_HEIGHT = 1100
    DIMENSIONS = get_dimensions_from_height(DEFAULT_HEIGHT)
    print("====== DEFAULT DIMENSIONS ======")
    print(DIMENSIONS)
    print("==============================")
    screen, play_area, boxes = setup_screens(DIMENSIONS)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Cardoku")

    # debugging_function(DIMENSIONS)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # WINDOW RESIZED
            if event.type == pygame.VIDEORESIZE:
                DIMENSIONS = get_dimensions(screen)
                screen, play_area, boxes = setup_screens(DIMENSIONS)
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     pass
            # elif event.type == pygame.MOUSEBUTTONUP:
            #     if event.button == 1:
            #         rectangle_draging = False

            # elif event.type == pygame.MOUSEMOTION:
            #     for card in cards:
            #         if rectangle_draging:
            #             card.pos = event.pos

        # draw the main board
        draw_board(screen, play_area, boxes, DIMENSIONS)
        play_area.blit(
            cards[0].resize_image(DIMENSIONS["image_size"]),
            (
                DIMENSIONS["play_area_centers"][0][0] + DIMENSIONS["image_size"] / 4,
                DIMENSIONS["play_area_centers"][0][1] + DIMENSIONS["image_size"] / 8,
            ),
        )
        circle = pygame.draw.circle(
            play_area,
            RED,
            (
                DIMENSIONS["play_area_centers"][0][0],
                DIMENSIONS["play_area_centers"][0][1],
            ),
            10,
        )
        screen.blit(
            cards[13].resize_image(200),
            (
                DIMENSIONS["screen_center"][0] - 73,
                DIMENSIONS["play_area"] + 150,
            ),
        )
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
