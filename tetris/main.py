import sys
import time

import pygame
from pygame.locals import *
from tetris.window import Board



# pygame.draw.rect(screen, WHITE, (10, 10, 100, 10))
def main():
    # Initialize pygame
    pygame.init()

    myfont = pygame.font.SysFont('Comic Sans MS', 30)

    # Get new board game
    board = Board()
    board.start_game()



    clock = pygame.time.Clock()
    fps = 60
    ticks = 0


    running = True
    pressed_key_tick = 0
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                pressed_key_tick = ticks
                if event.key == K_q:
                    running = False
                elif event.key == K_SPACE:
                    board.rotate()
                elif event.key == K_RIGHT:
                    board.move_piece(1, 0)
                elif event.key == K_LEFT:
                    board.move_piece(-1, 0)
                elif event.key == K_DOWN:
                    board.move_piece(0, 1)
                elif event.key == K_UP:
                    board.fast_drop_piece()
                elif event.key == K_RETURN:
                    board.get_piece()

        # Check pressed keys
        keystate = pygame.key.get_pressed()
        if ticks > pressed_key_tick + fps/4:
            if keystate[K_RIGHT] and ticks % int(fps/10) == 0:
                board.move_piece(1, 0)
            elif keystate[K_LEFT] and ticks % int(fps/10) == 0:
                board.move_piece(-1, 0)
            elif keystate[K_DOWN] and ticks % int(fps/30) == 0:
                board.move_piece(0, 1)


        pygame.display.update()
        clock.tick(fps)
        ticks += 1
        if ticks % fps == 0:
            board.move_piece(0, 1)
        board.draw_board()

if __name__ == '__main__':
    main()
