import sys

import pygame

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 300, 300
LINE_COLOR_1 = (255, 255, 255)
LINE_COLOR_2 = (128, 128, 128)
LINE_COLOR_3 = (64, 64, 64)
LINE_COLOR_4 = (32, 32, 32)
BG_COLOR = (0, 0, 0)
LINE_WIDTH = 4

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe Lines")


def draw_board():
    screen.fill(BG_COLOR)
    # Vertical lines
    pygame.draw.line(
        screen, LINE_COLOR_1, (WIDTH // 3, 0), (WIDTH // 3, HEIGHT), LINE_WIDTH
    )
    pygame.draw.line(
        screen, LINE_COLOR_2, (2 * WIDTH // 3, 0), (2 * WIDTH // 3, HEIGHT), LINE_WIDTH
    )
    # Horizontal lines
    pygame.draw.line(
        screen, LINE_COLOR_3, (0, HEIGHT // 3), (WIDTH, HEIGHT // 3), LINE_WIDTH
    )
    pygame.draw.line(
        screen, LINE_COLOR_4, (0, 2 * HEIGHT // 3), (WIDTH, 2 * HEIGHT // 3), LINE_WIDTH
    )


def main():
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        draw_board()
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
