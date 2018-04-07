import os
import pygame
from level import Level
from field import Field, TEXT_BLOCK_COEF
import pickle
from constants import *

TEST_PATH = 'levels/level2'
FONT_PATH = 'fonts/qarmic.ttf'
SAVE_PATH = 'save_data'


def save(field):
    with open(SAVE_PATH + '/field.pkl', 'wb') as f:
        pickle.dump(field, f, 2)


def load():
    try:
        with open(SAVE_PATH + '/field.pkl', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None


def process_click(x, y, field):
    n = field.n
    if x < process_click.block_len + BIG_MARGIN or y < process_click.block_len + BIG_MARGIN:
        return
    current_y = process_click.block_len + BIG_MARGIN
    done = False
    for i in range(1, n + 2):
        current_x = process_click.block_len + BIG_MARGIN
        for j in range(1, n + 2):
            if x <= current_x and y <= current_y:
                done = True
                break
            current_x += process_click.cell_side + (BIG_MARGIN if j % 5 == 0 else SMALL_MARGIN)
        if done:
            break
        current_y += process_click.cell_side + (BIG_MARGIN if i % 5 == 0 else SMALL_MARGIN)
    field.switch_state(i - 2, j - 2)


def draw_text(screen, rect, number, text, is_vertical):
    length = (text.get_rect().topright[0] - text.get_rect().topleft[0] + 1)
    x, y = rect.center
    if is_vertical:
        x, y = y, x
    x = draw_text.block_len - number * (SMALL_MARGIN + length) - (SMALL_MARGIN if number > 1 else 0)
    if is_vertical:
        x, y = y, x
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)


def redraw_side(screen, level, block_len, cell_side):
    n = level.n
    left_top_square = pygame.Rect(0, 0, block_len,block_len)
    x = block_len + BIG_MARGIN
    pygame.draw.rect(screen, WHITE, left_top_square)
    for i in range(1, n + 1):
        vertical_rect = pygame.Rect(x, 0, cell_side, block_len)
        pygame.draw.rect(screen, WHITE, vertical_rect)
        for position, value in enumerate(reversed(level.columns[i - 1])):
            draw_text(screen, vertical_rect, position + 1, redraw_side.numbers[value], True)
        x += cell_side + (BIG_MARGIN if i % 5 == 0 else SMALL_MARGIN)
    y = block_len + BIG_MARGIN
    for i in range(1, n + 1):
        horizontal_rect = pygame.Rect(0, y, block_len, cell_side)
        pygame.draw.rect(screen, WHITE, horizontal_rect)
        for position, value in enumerate(reversed(level.rows[i - 1])):
            draw_text(screen, horizontal_rect, position + 1, redraw_side.numbers[value], False)
        y += cell_side + (BIG_MARGIN if i % 5 == 0 else SMALL_MARGIN)


def draw_cross(screen, rect):
    pygame.draw.line(screen, RED, [n + 1 for n in rect.topleft], [n - 1 for n in rect.bottomright], 3)
    pygame.draw.line(screen, RED,
                     (rect.topright[0] - 1, rect.topright[1] + 1),
                     (rect.bottomleft[0] + 1, rect.bottomleft[1] - 1), 3)


def redraw_field(screen, field, block_len, cell_side):
    n = field.n
    y = block_len + BIG_MARGIN
    for i in range(1, n + 1):
        x = block_len + BIG_MARGIN
        for j in range(1, n + 1):
            inner_rect = pygame.Rect(x, y, cell_side, cell_side)
            color = WHITE
            if field.state[i - 1][j - 1] == 1:
                color = BLACK
            pygame.draw.rect(screen, color, inner_rect)
            if field.state[i - 1][j - 1] == 2:
                draw_cross(screen, inner_rect)
            x += cell_side + (BIG_MARGIN if j % 5 == 0 else SMALL_MARGIN)
        y += cell_side + (BIG_MARGIN if i % 5 == 0 else SMALL_MARGIN)


def redraw(screen, field, level):
    screen.fill(GRAY)
    redraw_side(screen, level, redraw.block_len, redraw.cell_side)
    redraw_field(screen, field, redraw.block_len, redraw.cell_side)


def init(cell_side, level):
    n = level.n
    pygame.init()
    pygame.display.set_caption('Японский кроссворд')
    font = pygame.font.Font(FONT_PATH, 15)
    redraw.block_len = TEXT_BLOCK_COEF * cell_side
    redraw.cell_side = cell_side
    process_click.cell_side = cell_side
    draw_cross.cell_side = cell_side
    process_click.block_len = redraw.block_len
    size = redraw.block_len + (n // 5) * BIG_MARGIN + (n - n // 5) * SMALL_MARGIN + n * cell_side
    screen = pygame.display.set_mode((size, size))
    draw_text.block_len = redraw.block_len
    redraw_side.numbers = {}
    for i in range(n):
        redraw_side.numbers[i] = font.render(str(i), True, BLACK)
    return screen


def main():
    level = Level(TEST_PATH)
    screen = init(CELL_SIDE, level)
    field = load()
    if field is None:
        field = Field(level.n, CELL_SIDE)
    clock = pygame.time.Clock()
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                process_click(x, y, field)
        redraw(screen, field, level)
        pygame.display.flip()
        clock.tick(60)
        save(field)

    pygame.quit()


if __name__ == '__main__':
    main()
