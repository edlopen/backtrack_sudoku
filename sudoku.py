import pygame
import time
import sys


BOARD_LENTH = 9

SAMPLE_BOARD = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]
pygame.init()
pygame.font.init()
BLACK = pygame.Color('black')
WHITE = pygame.Color('white')
FONT = pygame.font.SysFont('Arial', 30)


class Sudoku:

    def __init__(self, board=SAMPLE_BOARD):
        self.board = board
        # TODO: init pygame

        WINDOW_WIDTH, WINDOW_HEIGHT  = (540, 540)
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        #
        self.screen.fill(WHITE)
        self.rect_board = self.initGrid(self.board)
        pygame.display.flip()
        self.clock.tick(60)

    def catch_quit_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    def get_first_empty(self):
        for i, row in enumerate(self.board):
            for j, item in enumerate(row):
                if item == 0:
                    return (i, j)
        return None

    def initGrid(self, board):
        rect_board = []
        blockSize = 60 #Set the size of the grid block
        for i, row in enumerate(board):
            acu_row = []
            for j, item in enumerate(row):
                rect = pygame.Rect(i*blockSize, j*blockSize, blockSize, blockSize)
                pygame.draw.rect(self.screen, BLACK, rect, 1)
                if item:
                    text = FONT.render(str(item), True, BLACK)
                    self.screen.blit(text, rect.center)
                    acu_row.append([rect, text])
            rect_board.append(acu_row)
        return rect_board

    def solve(self):
        ''' Backtrack solution algorithm and GUI updates as it goes through '''
        self.catch_quit_game()
        first_empty = self.get_first_empty()
        if not first_empty:
            return True
        else:
            row, col = first_empty
        for i in range(1,10):
            if self.valid((row, col), i):
                self.board[row][col] = i
                self.updateGrid(row, col, i)
                if self.solve():
                    time.sleep(10)
                    return True
                # if False, then backtrack
                self.board[row][col] = 0
                self.updateGrid(row, col, i)
        return False

    def updateGrid(self, row, col, number):
        self.screen.fill(WHITE)
        self.initGrid(self.board)
        pygame.display.flip()
        time.sleep(0.1)

    def valid(self, position, number):
        row_pos, col_pos = position
        for i in range(0, BOARD_LENTH):
            # check number in row
            if number == self.board[row_pos][i] and i != row_pos:
                return False
            # check number in colum
            if number == self.board[i][col_pos] and i != col_pos:
                return False
            # check number in box
            row_box, col_box = row_pos // 3, col_pos // 3
            for i in range(row_box * 3, row_box * 3 + 3):
                for j in range(col_box * 3, col_box * 3 + 3):
                    if self.board[i][j] == number and (i, j) != position:
                        return False
        return True


Sudoku().solve()
