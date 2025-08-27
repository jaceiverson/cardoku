import random
import sys

import matplotlib.pyplot as plt
import pygame
from card import read_in_card_images
from colors import (
    BACKGROUND_COLOR,
    BOX_COLOR,
    CELL_COLOR,
    LINE_COLOR,
    PLAY_AREA_COLOR,
    TEXT_COLOR,
)
from configs import FONT, get_dimensions, get_dimensions_from_height
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


def draw_cells(
    dimensions: dict,
    play_area: pygame.Surface,
    font: pygame.font.Font,
    include_numbers: bool = False,
):
    counter = 1
    for box_w, box_h in dimensions["play_area_centers"]:
        for cw, ch in dimensions["cell_centers"]:
            indv_cell = pygame.Rect(
                box_w + cw, box_h + ch, dimensions["cell_size"], dimensions["cell_size"]
            )
            indv_cell.center = (box_w + cw, box_h + ch)
            pygame.draw.rect(
                play_area,
                PLAY_AREA_COLOR,
                indv_cell,
            )
            if include_numbers:
                number = FONT.render(str(counter), True, TEXT_COLOR)
                num_center = number.get_rect(center=(box_w + cw, box_h + ch))
                play_area.blit(number, num_center)
                counter += 1


def setup_screens(
    dims: dict[str, int], resizeable: bool = False
) -> tuple[pygame.Surface, pygame.Surface]:
    if resizeable:
        screen = pygame.display.set_mode(
            (dims["screen_width"], dims["screen_height"]), pygame.RESIZABLE
        )
    else:
        screen = pygame.display.set_mode((dims["screen_width"], dims["screen_height"]))
    pygame.display.set_caption("Cardoku")
    screen.fill(BACKGROUND_COLOR)
    play_area = pygame.Surface((dims["play_area"], dims["play_area"]))
    play_area.fill(BOX_COLOR)
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
        surface.fill(BOX_COLOR)
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
            BACKGROUND_COLOR,
            (x * (side_length / 3), 0),
            (x * (side_length / 3), side_length),
            line_width,
        )

    # horizontal lines
    for y in range(1, 3):
        pygame.draw.line(
            play_area_screen,
            BACKGROUND_COLOR,
            (0, y * (side_length / 3)),
            (side_length, y * (side_length / 3)),
            line_width,
        )


def draw_board(screen, play_area, boxes, dimensions, font):
    # MAIN PLAY AREA
    screen.blit(
        play_area,
        (
            dimensions["play_area_starting_point"][0],
            dimensions["play_area_starting_point"][1],
        ),
    )
    # INDIVIDUAL BOXES
    for box, centers in zip(boxes, dimensions["play_area_top_left_corners"]):
        play_area.blit(
            box,
            (
                centers[0],
                centers[1],
            ),
        )
    # INDIVIDUAL CELLS
    draw_cells(dimensions, play_area, font, False)


def draw_board_from_image(
    screen: pygame.Surface, play_area_image: pygame.image, dimensions: dict
):
    screen.blit(
        play_area_image,
        (
            dimensions["play_area_starting_point"][0],
            dimensions["play_area_starting_point"][1],
        ),
    )


def main():
    pygame.init()
    DEFAULT_HEIGHT = 1100
    DIMENSIONS = get_dimensions_from_height(DEFAULT_HEIGHT)
    play_area_image = pygame.image.load("game_resources/play_area_2.png")
    print("====== DEFAULT DIMENSIONS ======")
    print(DIMENSIONS)
    print("==============================")
    screen, play_area, boxes = setup_screens(DIMENSIONS)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Cardoku")
    # draw the main board
    # draw_board(screen, play_area, boxes, DIMENSIONS, font)
    # debugging_function(DIMENSIONS)

    cards = read_in_card_images()
    for i, card in enumerate(cards):
        if i == len(cards) - 1:
            card.rect.center = (
                DIMENSIONS["visible_card_center"][0],
                DIMENSIONS["visible_card_center"][1],
            )
        else:
            card.rect.center = (
                DIMENSIONS["deck_center"][0],
                DIMENSIONS["deck_center"][1],
            )
    deck = cards.copy()
    print(deck[0])
    print(deck[-1])
    dragged_card = None
    while True:
        for event in pygame.event.get():
            screen.fill(BACKGROUND_COLOR)
            draw_board_from_image(screen, play_area_image, DIMENSIONS)
            if event.type == pygame.QUIT:
                sys.exit()
            # WINDOW RESIZED - NOT SUPPORTED AT THIS TIME
            # elif event.type == pygame.VIDEORESIZE:
            #     DIMENSIONS = get_dimensions(screen)
            #     screen, play_area, boxes = setup_screens(DIMENSIONS)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(event)
                # left click
                if event.button == 1:
                    for card_idx, card in enumerate(cards):
                        if card.rect.collidepoint(event.pos):
                            dragged_card = card
                            dragged_card_idx = card_idx
                            print(f"{card=} {card.dragging=} {dragged_card=}")
                            # dragged_card.dragging = True
                            # test_card.display_image = test_card.big_image
                            offset_x = event.pos[0] - dragged_card.rect.x
                            offset_y = event.pos[1] - dragged_card.rect.y
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if dragged_card:
                        print(event)
                        current_center = dragged_card.rect.center
                        print(f"{dragged_card.rect.center=}")
                        dragged_card.display_image = dragged_card.resize_image(
                            DIMENSIONS["image_size"]
                        )
                        print(f"{dragged_card.rect.center=}")
                        # TODO: why is this not centering? It is locking into the current top left position
                        # TODO: maybe convert this to the image shorthand?
                        # dragged_card.display_image = dragged_card.display_short_hand
                        dragged_card.rect.center = current_center

                        print(f"{dragged_card.rect.center=}")
                        # dragged_card.rect = card_rect
                        cards[dragged_card_idx] = dragged_card
                        cards[dragged_card_idx].dragging = False
                        cards[dragged_card_idx].rect = dragged_card.rect
                        dragged_card = None
                        dragged_card_idx = None

            elif event.type == pygame.MOUSEMOTION:
                if dragged_card:
                    print(event)
                    dragged_card.rect.x = event.pos[0] - offset_x
                    dragged_card.rect.y = event.pos[1] - offset_y

        # DECK BOX TO PULL FROM
        the_box = pygame.Surface((DIMENSIONS["inner_grid"], DIMENSIONS["inner_grid"]))
        the_box.fill(BOX_COLOR)
        box_rect = the_box.get_rect()
        box_rect.center = (DIMENSIONS["box_center"][0], DIMENSIONS["box_center"][1])
        screen.blit(the_box, box_rect)

        for card in deck:
            screen.blit(
                card.display_image,
                card.rect,
            )

        # pygame.image.save(play_area, "play_area_3.png")
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
