import pygame
import sys
from gameplay import Game
from ia import AStarSolver
WIDTH = 400
HEIGHT = 400
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
COLR_TILE = (223, 220, 218)
BACKGROUND = (26, 31, 40)
COLR_NUM = (0, 0, 128)
SPACECING = 1

pygame.init()

pygame.display.set_caption('8-PUZZLE')

CLOCK = pygame.time.Clock()

game = Game()

resolver_ia = AStarSolver(game.initial_state, game.goal_state)

while True:
    SCREEN.fill(BACKGROUND)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                game.reset()
                resolver_ia = AStarSolver(game.initial_state, game.goal_state)
                resolver_ia.reset()

            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.key == pygame.K_SPACE and not game.solved and not resolver_ia.is_running:
                solution_path = resolver_ia.solve()
                resolver_ia.is_running = True

        if event.type == pygame.MOUSEBUTTONDOWN and not game.solved:
            pos_x = event.pos[1] // (WIDTH // 3 - SPACECING)
            pos_y = event.pos[0] // (HEIGHT // 3 - SPACECING)
            game.move_tile(pos_x, pos_y)

    if resolver_ia.solution_path:
        game.initial_state = solution_path.pop()
        pygame.time.wait(270)

    game.draw_board()

    if game.is_solved():
        game.draw_win()

    pygame.display.update()

    CLOCK.tick(60)
