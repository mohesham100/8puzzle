import copy
import random
import pygame

WIDTH = 400
HEIGHT = 400
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
COLR_TILE = (223, 220, 218)
BACKGROUND = (26, 31, 40)
COLR_NUM = (0, 0, 128)
SPACECING = 1


class Game:
    def __init__(self):
        self.solved = False
        self.goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        self.initial_state = self.generate_valid_board(copy.deepcopy(self.goal_state))
    
    def generate_valid_board(self, state):
        board = self.shuffle(state)
        
        while not self.is_solvable(board):
            board = self.shuffle(state)
        
        return board
    
    def shuffle(self, state):
        for _ in range(50):
            pos_A = (random.randint(0, 2), random.randint(0, 2))
            pos_B = (random.randint(0, 2), random.randint(0, 2))

            while pos_A == pos_B:
                pos_B = (random.randint(0, 2), random.randint(0, 2))
                pos_A = (random.randint(0, 2), random.randint(0, 2))

            self.swap(pos_A, pos_B, state)

        return state

    def swap(self, pos_A, pos_B, board):
        i, j = pos_A
        k, l = pos_B
        board[i][j], board[k][l] = board[k][l], board[i][j]

    def is_solvable(self, state):
        flatten_state = [num for row in state for num in row]
        inversions = 0

        for i in range(len(flatten_state)):
            if flatten_state[i] == 0:
                continue
            for j in range(i + 1, len(flatten_state)):
                if flatten_state[j] == 0:
                    continue
                if flatten_state[i] > flatten_state[j]:
                    inversions += 1

        return inversions % 2 == 0

    def get_blank_pos(self):
        for i in range(3):
            for j in range(3):
                if self.initial_state[i][j] == 0:
                    return (i, j)
    
    def is_neighbor(self, pos_A, pos_B):
        if pos_A[0] == pos_B[0] and abs(pos_A[1] - pos_B[1]) == 1:
            return True
        elif pos_A[1] == pos_B[1] and abs(pos_A[0] - pos_B[0]) == 1:
            return True
    
    def move_tile(self, pos_x, pos_y):
        blank_pos = self.get_blank_pos()

        if blank_pos != (pos_x, pos_y):
            if blank_pos[0] == pos_x or blank_pos[1] == pos_y:
                if self.is_neighbor(blank_pos, (pos_x, pos_y)):
                    self.swap(blank_pos, (pos_x, pos_y), self.initial_state)

    def is_solved(self):
        if self.initial_state == self.goal_state:
            self.solved = True
            return True

        return False

    def draw_win(self):
        font = pygame.font.Font('freesansbold.ttf', 24)

        pygame.draw.rect(SCREEN, 'black', [50, 50, 300, 200], 0, 10)

        won_text1 = font.render(f'You Won!', True, 'white')
        won_text2 = font.render('Press ENTER to restart', True, 'white')
        won_text3 = font.render('Press ESCAPE to quit', True, 'white')

        SCREEN.blit(won_text1, (140, 65))
        SCREEN.blit(won_text2, (70, 145))
        SCREEN.blit(won_text3, (70, 185))

    def draw_board(self):
        font = pygame.font.Font('freesansbold.ttf', 42)
        for i in range(3):
            for j in range(3):
                val = self.initial_state[i][j]
                pos_x = j * WIDTH // 3 + SPACECING
                pos_y = i * HEIGHT // 3 + SPACECING
                width_rect = WIDTH // 3 - 2 * SPACECING
                height_rect = HEIGHT // 3 - 2 * SPACECING

                board_rect = pygame.Rect(pos_x, pos_y, width_rect, height_rect)

                if val:
                    border_rect = pygame.Rect(pos_x, pos_y, width_rect, height_rect)
                    pygame.draw.rect(SCREEN, (43, 52, 66), border_rect, 1, 5)
                    pygame.draw.rect(SCREEN, COLR_TILE, board_rect, border_radius=5)
                    text_surface = font.render(str(val), True, COLR_NUM)
                    text_rect = text_surface.get_rect(center=(pos_x + width_rect//2, pos_y + height_rect//2))
                    SCREEN.blit(text_surface, text_rect)
                    pygame.draw.rect(
                        SCREEN, 'black',
                        [pos_x, pos_y, WIDTH//3-2*SPACECING, HEIGHT//3-2*SPACECING],
                        1, 5
                    )
                else:
                    pygame.draw.rect(SCREEN, BACKGROUND, board_rect, border_radius=5)

    def reset(self):
        self.solved = False
        self.goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        self.initial_state = self.generate_valid_board(copy.deepcopy(self.goal_state))
