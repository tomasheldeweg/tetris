import random
import numpy as np
import pygame
from tetris.pieces import Piece, COLOURS, SHAPES

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)





class Board:

    def __init__(self, dim=600):
        self.dim = dim
        self.size = (dim, dim)
        self.BLOCK_SIZE = dim / 30
        self.BOARD_HEIGHT = 24
        self.BOARD_WIDTH = 10
        pygame.font.init()
        self.FONT = pygame.font.SysFont('calibri', int(dim/50))
        self.grid = np.zeros((self.BOARD_HEIGHT, self.BOARD_WIDTH))
        self.p = Piece(random.choice(list(SHAPES)))
        self.next_p = Piece(random.choice(list(SHAPES)))
        self.level = 0
        self.score = 0
        self.total_lines = 0
        self.start_game()

    def start_game(self):
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Tetris')
        self._draw_layout()
        self._draw_score()
        self._draw_next_piece()

    def _reset_game(self):
        self.screen.fill(BLACK)
        self.level = 0
        self.score = 0
        self.total_lines = 0
        self.p = Piece(random.choice(list(SHAPES)))
        self.next_p = Piece(random.choice(list(SHAPES)))
        self.grid = np.zeros((self.BOARD_HEIGHT, self.BOARD_WIDTH))
        self._draw_layout()
        self.draw_board()
        self._draw_score()
        self._draw_next_piece()



    def get_piece(self):
        self._check_complete_lines()
        self.p = self.next_p
        self.next_p = Piece(random.choice(list(SHAPES)))

        if not self._valid_piece_position():
            print(' GAME OVER ')
            pygame.time.wait(3000)
            self._reset_game()
            return None

        self.score += 20 * (self.level + 1)
        self._draw_score()
        self._draw_next_piece()



    def _check_complete_lines(self):
        completed_lines = np.where(self.grid.all(axis=1))[0]
        if completed_lines.size != 0:
            print('line_completed')
            nr_lines = completed_lines.size
            np.zeros((self.BOARD_HEIGHT, self.BOARD_WIDTH))
            remaining_rows = np.delete(self.grid, completed_lines, axis=0)
            new_rows = np.zeros((nr_lines, self.BOARD_WIDTH))
            self.grid = np.concatenate((new_rows, remaining_rows), axis=0)

            # Scoring
            if nr_lines == 1:
                self.score += 50 * (self.level + 1)
            elif nr_lines == 2:
                self.score += 150 * (self.level + 1)
            elif nr_lines == 3:
                self.score += 250 * (self.level + 1)
            elif nr_lines == 4:
                self.score += 1000 * (self.level + 1)
            self.total_lines += nr_lines
            self.level = int(self.total_lines / 10)


    def _draw_layout(self):
        # Playing field
        xpos = self.dim / 3
        ypos = self.dim / 10

        # Draw grid y lines
        for line in range(self.BOARD_WIDTH + 1):
            if line == 0 or line == self.BOARD_WIDTH:
                pygame.draw.line(self.screen, RED, (xpos + line * self.BLOCK_SIZE, ypos),
                                 (xpos + line * self.BLOCK_SIZE, self.size[1] - ypos), 2)
            else:
                pygame.draw.line(self.screen, WHITE, (xpos + line * self.BLOCK_SIZE, ypos),
                                 (xpos + line * self.BLOCK_SIZE, self.size[1] - ypos), 1)

        # Draw grid x lines
        for line in range(self.BOARD_HEIGHT + 1):
            if line == 0 or line == self.BOARD_HEIGHT:
                pygame.draw.line(self.screen, RED, (xpos, ypos + line * self.BLOCK_SIZE),
                                 (self.size[0] - xpos, ypos + line * self.BLOCK_SIZE), 2)
            else:
                pygame.draw.line(self.screen, WHITE, (xpos, ypos + line * self.BLOCK_SIZE),
                                 (self.size[0] - xpos, ypos + line * self.BLOCK_SIZE), 1)

        # Score layout
        score_x = self.dim - self.BLOCK_SIZE * 8
        score_y = self.dim / 10
        points = [(score_x, score_y),
                  (score_x + self.BLOCK_SIZE * 7, score_y),
                  (score_x + self.BLOCK_SIZE * 7, score_y + 70),
                  (score_x, score_y + 70)]
        pygame.draw.lines(self.screen, WHITE, True, points, 1)

        xpos = self.dim / 9
        ypos = self.dim / 10
        # Next piece layout
        for line in range(5):
            if line == 0 or line == 4:
                pygame.draw.line(self.screen, RED, (xpos + line * self.BLOCK_SIZE, ypos),
                                 (xpos + line * self.BLOCK_SIZE, ypos + self.BLOCK_SIZE * 4), 2)
            else:
                pygame.draw.line(self.screen, WHITE, (xpos + line * self.BLOCK_SIZE, ypos),
                                 (xpos + line * self.BLOCK_SIZE, ypos + self.BLOCK_SIZE * 4), 1)

        # Draw grid x lines
        for line in range(5):
            if line == 0 or line == 4:
                pygame.draw.line(self.screen, RED, (xpos, ypos + line * self.BLOCK_SIZE),
                                 (xpos + self.BLOCK_SIZE * 4, ypos + line * self.BLOCK_SIZE), 2)
            else:
                pygame.draw.line(self.screen, WHITE, (xpos, ypos + line * self.BLOCK_SIZE),
                                 (xpos + self.BLOCK_SIZE * 4, ypos + line * self.BLOCK_SIZE), 1)

    def _draw_piece(self):
        # Drawing start position
        xpos = self.dim / 3
        ypos = self.dim / 10
        colour = COLOURS[self.p.value]
        for (y, x) in tuple(zip(*self.p.coords)):
            pygame.draw.rect(
                self.screen,
                colour,
                (xpos + x * self.BLOCK_SIZE + 1, ypos + y * self.BLOCK_SIZE + 1, self.BLOCK_SIZE - 1,
                 self.BLOCK_SIZE - 1)
            )

    def _draw_next_piece(self):
        # Drawing start position
        xpos = self.dim / 9
        ypos = self.dim / 10
        for y in range(self.next_p.piece.shape[1]):
            for x in range(self.next_p.piece.shape[0]):
                colour = COLOURS[self.next_p.piece[y, x]]
                pygame.draw.rect(
                    self.screen,
                    colour,
                    (xpos + x * self.BLOCK_SIZE + 1, ypos + y * self.BLOCK_SIZE + 1, self.BLOCK_SIZE - 1, self.BLOCK_SIZE - 1)
                )

    def _draw_grid(self):
        # Drawing start position
        xpos = self.dim / 3
        ypos = self.dim / 10

        for y in range(self.BOARD_HEIGHT):
            for x in range(self.BOARD_WIDTH):
                colour = COLOURS[self.grid[y, x]]
                pygame.draw.rect(
                    self.screen,
                    colour,
                    (xpos + x * self.BLOCK_SIZE + 1, ypos + y * self.BLOCK_SIZE + 1, self.BLOCK_SIZE - 1, self.BLOCK_SIZE - 1)
                )

    def _draw_score(self):
        score = self.FONT.render(f"score: {self.score}", True, WHITE, BLACK)
        level = self.FONT.render(f"level: {self.level}", True, WHITE, BLACK)
        lines = self.FONT.render(f"lines: {self.total_lines}", True, WHITE, BLACK)
        self.screen.blit(score, (self.dim - self.BLOCK_SIZE * 8 + 10, self.dim / 10 + 10))
        self.screen.blit(level, (self.dim - self.BLOCK_SIZE * 8 + 10, self.dim / 10 + 30))
        self.screen.blit(lines, (self.dim - self.BLOCK_SIZE * 8 + 10, self.dim / 10 + 50))

    def draw_board(self):
        self._draw_grid()
        self._draw_piece()

    def move_piece(self, x, y):
        if self.p:
            if self._valid_piece_position(x, y):
                self.p.move(x, y)
            elif y > 0:
                self._piece_to_board()
                self.get_piece()

    def fast_drop_piece(self):
        if self.p:
            y = 1
            while self._valid_piece_position(0, y):
                y += 1
            self.move_piece(0, y-1)
            self._piece_to_board()
            self.get_piece()

    def _piece_to_board(self):
        self.grid[self.p.coords] = self.p.value

    def rotate(self):
        if self.p:
            self.p.rotate()
        if not self._valid_piece_position():
            self.p.rotate(-1)

    def _valid_piece_position(self, x=0, y=0):
        px = self.p.coords[1] + x
        py = self.p.coords[0] + y
        out_of_bounds = False
        if any(x >= 10 or x < 0 for x in px):
            out_of_bounds = True
        elif any(y >= 24 for y in py):
            out_of_bounds = True

        return not (out_of_bounds or np.any(self.grid[[py, px]]))
