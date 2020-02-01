import math
import pygame
import random
from enum import Enum

SCREEN_WIDTH = 512
SCREEN_HEIGHT = 480

CELL_WIDTH = 4
CELL_HEIGHT = 4

BLOCK_WIDTH = SCREEN_WIDTH/CELL_WIDTH
BLOCK_HEIGHT = SCREEN_HEIGHT/CELL_HEIGHT

STARTING_VALUES = [2, 2, 2, 2, 2, 2, 2, 4]

BG_COLOR = pygame.Color(0, 0, 0)
BLOCK_COLOR = pygame.Color(127, 127, 127)
TEXT_COLOR = pygame.Color(255, 255, 255)

MOVE_SPEED = 30

class State:
    IDLE = 0
    MOVING = 1


class ShiftState:
    SHIFT = 0
    COMBINE = 1
    STOP = 2


class BlockIndex:
    RECT = 0
    VALUE = 1


def create_block(cell_rows):
    empty_spaces = []

    for i in range(0, CELL_HEIGHT):
        for j in range(0, CELL_WIDTH):
            if cell_rows[i][j] is None:
                empty_spaces.append((i, j))

    new_block_space = random.choice(empty_spaces)

    cell_rows[new_block_space[0]][new_block_space[1]] = [
        pygame.Rect(
            BLOCK_WIDTH * new_block_space[1],
            BLOCK_HEIGHT * new_block_space[0],
            BLOCK_WIDTH,
            BLOCK_HEIGHT
        ),
        random.choice(STARTING_VALUES)
    ]


# returns True if the block is done moving
def check_cell(src_cell, dst_cell):
    if dst_cell is None:
        return ShiftState.SHIFT
    elif dst_cell[BlockIndex.VALUE] == src_cell[BlockIndex.VALUE]:
        return ShiftState.COMBINE
    else:
        return ShiftState.STOP


# returns True if a block will move
def up_event(cell_rows):
    any_moved = False
    for j in range(0, CELL_WIDTH):
        for i in range(0, CELL_HEIGHT):
            if cell_rows[i][j] is not None:
                new_y = i
                for k in range(i-1, -1, -1):
                    shift_state = check_cell(cell_rows[i][j], cell_rows[k][j])
                    if shift_state == ShiftState.SHIFT or shift_state == ShiftState.COMBINE:
                        new_y = k
                    if shift_state == ShiftState.COMBINE:
                        cell_rows[i][j][BlockIndex.VALUE] = cell_rows[i][j][BlockIndex.VALUE] * 2
                    if shift_state == ShiftState.COMBINE or shift_state == ShiftState.STOP:
                        break
                if new_y != i:
                    cell_rows[new_y][j] = cell_rows[i][j]
                    cell_rows[i][j] = None
                    any_moved = True
    return any_moved


# returns True if a block will move
def down_event(cell_rows):
    any_moved = False
    for j in range(0, CELL_WIDTH):
        for i in range(CELL_HEIGHT-1, -1, -1):
            if cell_rows[i][j] is not None:
                new_y = i
                for k in range(i+1, CELL_HEIGHT):
                    shift_state = check_cell(cell_rows[i][j], cell_rows[k][j])
                    if shift_state == ShiftState.SHIFT or shift_state == ShiftState.COMBINE:
                        new_y = k
                    if shift_state == ShiftState.COMBINE:
                        cell_rows[i][j][BlockIndex.VALUE] = cell_rows[i][j][BlockIndex.VALUE] * 2
                    if shift_state == ShiftState.COMBINE or shift_state == ShiftState.STOP:
                        break
                if new_y != i:
                    cell_rows[new_y][j] = cell_rows[i][j]
                    cell_rows[i][j] = None
                    any_moved = True
    return any_moved


# returns True if a block will move
def left_event(cell_rows):
    any_moved = False
    for i in range(0, CELL_HEIGHT):
        for j in range(0, CELL_WIDTH):
            if cell_rows[i][j] is not None:
                new_x = j
                for k in range(j-1, -1, -1):
                    shift_state = check_cell(cell_rows[i][j], cell_rows[i][k])
                    if shift_state == ShiftState.SHIFT or shift_state == ShiftState.COMBINE:
                        new_x = k
                    if shift_state == ShiftState.COMBINE:
                        cell_rows[i][j][BlockIndex.VALUE] = cell_rows[i][j][BlockIndex.VALUE] * 2
                    if shift_state == ShiftState.COMBINE or shift_state == ShiftState.STOP:
                        break
                if new_x != j:
                    cell_rows[i][new_x] = cell_rows[i][j]
                    cell_rows[i][j] = None
                    any_moved = True
    return any_moved


# returns True if a block will move
def right_event(cell_rows):
    any_moved = False
    for i in range(0, CELL_HEIGHT):
        for j in range(CELL_WIDTH-1, -1, -1):
            if cell_rows[i][j] is not None:
                new_x = j
                for k in range(j+1, CELL_WIDTH):
                    shift_state = check_cell(cell_rows[i][j], cell_rows[i][k])
                    if shift_state == ShiftState.SHIFT or shift_state == ShiftState.COMBINE:
                        new_x = k
                    if shift_state == ShiftState.COMBINE:
                        cell_rows[i][j][BlockIndex.VALUE] = cell_rows[i][j][BlockIndex.VALUE] * 2
                    if shift_state == ShiftState.COMBINE or shift_state == ShiftState.STOP:
                        break
                if new_x != j:
                    cell_rows[i][new_x] = cell_rows[i][j]
                    cell_rows[i][j] = None
                    any_moved = True
    return any_moved


# returns True is moving is done
def do_move(cell_rows):
    any_moved = False
    for i in range(0, CELL_HEIGHT):
        for j in range(0, CELL_WIDTH):
            if cell_rows[i][j] is not None:
                rect = cell_rows[i][j][BlockIndex.RECT]
                if rect.top < BLOCK_HEIGHT * i:
                    rect.top = min(rect.top+MOVE_SPEED, BLOCK_HEIGHT * i)
                    any_moved = True
                elif rect.top > BLOCK_HEIGHT * i:
                    rect.top = max(rect.top-MOVE_SPEED, BLOCK_HEIGHT * i)
                    any_moved = True
                elif rect.left < BLOCK_WIDTH * j:
                    rect.left = min(rect.left+MOVE_SPEED, BLOCK_WIDTH * j)
                    any_moved = True
                elif rect.left > BLOCK_WIDTH * j:
                    rect.left = max(rect.left-MOVE_SPEED, BLOCK_WIDTH * j)
                    any_moved = True
    return not any_moved


def draw(cell_rows):
    font = pygame.font.SysFont("Arial", 32, bold=True)
    surface = pygame.display.get_surface()
    surface.fill(BG_COLOR)
    for i in range(0, CELL_HEIGHT):
        for j in range(0, CELL_WIDTH):
            if cell_rows[i][j] is not None:
                rect = cell_rows[i][j][BlockIndex.RECT]
                value = cell_rows[i][j][BlockIndex.VALUE]
                color_grade = int(min(255, 25*(math.log2(value))))
                block_color = pygame.Color(255, color_grade, color_grade)
                text_color = TEXT_COLOR if color_grade < 127 else BG_COLOR
                pygame.draw.rect(surface, block_color, rect)
                text_surface = font.render(str(value), True, text_color)
                text_top = (rect.top + BLOCK_HEIGHT/2 - text_surface.get_height()/2)
                text_left = (rect.left + BLOCK_WIDTH/2 - text_surface.get_width()/2)
                surface.blit(text_surface, (text_left, text_top))
    pygame.display.flip()

 
def main():

    cell_rows = []
    for i in range(0, CELL_HEIGHT):
        cell_row = []
        for j in range(0, CELL_WIDTH):
            cell_row.append(None)
        cell_rows.append(cell_row)

    state = State.IDLE
    move_step = 0

    create_block(cell_rows)
     
    pygame.init()

    pygame.display.set_caption("2048")
     
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
     
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif state == State.IDLE:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if up_event(cell_rows):
                            state = State.MOVING
                    elif event.key == pygame.K_DOWN:
                        if down_event(cell_rows):
                            state = State.MOVING
                    elif event.key == pygame.K_LEFT:
                        if left_event(cell_rows):
                            state = State.MOVING
                    elif event.key == pygame.K_RIGHT:
                        if right_event(cell_rows):
                            state = State.MOVING
        if state == State.MOVING:
            if do_move(cell_rows):
                create_block(cell_rows)
                state = State.IDLE
        draw(cell_rows)

     
     
if __name__=="__main__":
    main()