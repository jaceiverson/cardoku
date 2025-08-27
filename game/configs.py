from enum import Enum

import pygame

pygame.init()
IMAGE_TYPE = "PNG"

FONT = pygame.font.SysFont("Arial", 30, True)


class CardView(Enum):
    FULL = "full"
    CONDENSED = "condensed"
    NUMERIC = "numeric"
    DYNAMIC = "dynamic"


def find_grid_centers(grid_size: int) -> list[tuple[int, int]]:
    """
    Given a grid, find the 9 center points for the sudoku subgrids.
    """
    return sum(
        [
            [
                (
                    (col * (grid_size / 3)) + grid_size / 2,
                    (row * (grid_size / 3)) + grid_size / 2,
                )
                for col in range(-1, 2, 1)
            ]
            for row in range(-1, 2, 1)
        ],
        [],
    )


def get_dimensions(surface: pygame.Surface) -> dict[str, int]:
    true_height = surface.get_height()
    return get_dimensions_from_height(true_height)


def determine_box_number(dimensions: dict, pos_w: int, pos_h: int) -> int:
    pass


def get_dimensions_from_height(screen_height: int) -> dict[str, int]:
    # 80% of height
    screen_width = screen_height * 0.8
    # 60% of the height
    play_area_size = screen_height * 0.6
    # now get the center points for the play_area
    play_area_centers = find_grid_centers(play_area_size)
    # save the play_area starting points
    play_area_starting_points = (
        (int(screen_width) - int(play_area_size)) / 2,
        (int(screen_height) - int(play_area_size)) / 4,
    )
    # 30% of the play area to account for lines and padding
    inner_grid_size = play_area_size * 0.3
    # center points of the inner grid
    inner_grid_centers = find_grid_centers(inner_grid_size)
    # 3\0% of the inner grid side
    cell_size = inner_grid_size * 0.3
    # 1% of the play area height
    main_line_width = play_area_size * 0.01
    # 1% of the inner grid side of the play area
    inner_line_width = inner_grid_size * 0.01

    return {
        "screen_height": int(screen_height),
        "screen_width": int(screen_width),
        "screen_center": (int(screen_width // 2), int(screen_height // 2)),
        "play_area": int(play_area_size),
        "play_area_starting_point": play_area_starting_points,
        "play_area_top_left_corners": [
            (int(x) - int(inner_grid_size / 2), int(y) - int(inner_grid_size / 2))
            for x, y in play_area_centers
        ],
        "play_area_centers": [(int(x), int(y)) for x, y in play_area_centers],
        "main_line_width": int(main_line_width),
        "inner_grid": int(inner_grid_size),
        "inner_line_width": int(inner_line_width),
        "cell_size": int(cell_size),
        "image_size": int(cell_size * 0.9),
        "cell_centers": [
            (int(x) - int(inner_grid_size / 2), int(y) - int(inner_grid_size / 2))
            for x, y in inner_grid_centers
        ],
        "box_center": (
            int(screen_width / 3),
            int(play_area_size) + play_area_starting_points[1] + 150,
        ),
        "visible_card_center": (
            int(screen_width) - 100,
            int(play_area_size) + play_area_starting_points[1] + 400,
        ),
        "deck_center": (
            int(screen_width / 3) + 100,
            int(play_area_size) + play_area_starting_points[1] + 400,
        ),
    }


def get_cells(play_area_dimension: int) -> dict:
    cell_size = play_area_dimension * 0.3 * 0.3
    return {
        "cell_size": cell_size,
        "cells": [
            {"rect": (x * cell_size, y * cell_size, cell_size, cell_size)}
            for x in range(3)
            for y in range(3)
        ],
    }
