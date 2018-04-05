import os
import pygame
from level import Level
from field import Field, TEXT_BLOCK_COEF
from constants import *

TEST_PATH = os.getcwd() + '/levels/level2'
FONT_PATH = os.getcwd() + '/fonts/qarmic.ttf'


def process_click(x, y):
    pass


def repaint_screen(screen, field, level):
    n = field.n
    screen.fill(GRAY)
    pygame.draw.rect(screen, WHITE, [MARGIN, MARGIN,
                                     repaint_screen.block_len - 2 * MARGIN,
                                     repaint_screen.block_len - 2 * MARGIN])
    for i in range(n):
        additional = MARGIN if i % 5 == 0 else 0
        horizontal_rec = pygame.Rect(MARGIN, repaint_screen.block_len + CELL_SIDE * i - MARGIN + additional,
                                     repaint_screen.block_len - 2 * MARGIN, CELL_SIDE - MARGIN - additional)
        horizontal_text = repaint_screen.font.render(' '.join(list(map(str, level.rows[i]))), True, (0, 0, 0))
        horizontal_text_rect = horizontal_text.get_rect(center=(horizontal_rec.center[0], horizontal_rec.center[1]))
        pygame.draw.rect(screen, WHITE, horizontal_rec)
        pygame.draw.rect(screen, WHITE, [repaint_screen.block_len + CELL_SIDE * i - MARGIN + additional,
                                         MARGIN,
                                         CELL_SIDE - MARGIN - additional,
                                         repaint_screen.block_len - 2 * MARGIN])
        print(*horizontal_rec.center)
        screen.blit(horizontal_text, horizontal_text_rect)

    for i in range(n):
        for j in range(n):
            pass


def init(cell_side, n):
    pygame.init()
    pygame.display.set_caption('Японский кроссворд')
    repaint_screen.font = pygame.font.Font(FONT_PATH, 15)
    print(pygame.font.get_fonts())
    repaint_screen.block_len = TEXT_BLOCK_COEF * CELL_SIDE


def main():
    level = Level(TEST_PATH)
    init(CELL_SIDE, level.n)
    size = ((TEXT_BLOCK_COEF + level.n) * CELL_SIDE,
            (TEXT_BLOCK_COEF + level.n) * CELL_SIDE)
    screen = pygame.display.set_mode(size)
    field = Field(level.n, CELL_SIDE)
    clock = pygame.time.Clock()
    done = False
    repaint_screen(screen, field, level)
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        #repaint_screen(screen, field, level)
        pygame.display.flip()
        clock.tick(60)

    # Close the window and quit.
    pygame.quit()


if __name__ == '__main__':
    main()