import heapq as hq
import copy

class AStarSolver:
    def __init__(self, initial_state, goal_state):
        self.is_running = False
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.solution_path = []

    def manhattan_dist(self, x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    def calc_heuristic(self, state):
        heuristic = 0
        for i in range(3):
            for j in range(3):
                value = state[i][j]
                if value != 0:
                    goal_pos = self.get_goal_position(value)
                    heuristic += self.manhattan_dist(i, j, goal_pos[0], goal_pos[1])
        return heuristic

    def get_goal_position(self, value):
        for i in range(3):
            for j in range(3):
                if self.goal_state[i][j] == value:
                    return (i, j)

    def get_blank_position(self, state):
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    return (i, j)

    def is_goal_state(self, state):
        return state == self.goal_state

    def generate_next_states(self, state):
        next_states = []
        blank_pos = self.get_blank_position(state)
        pos_moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up

        for move in pos_moves:
            new_state = copy.deepcopy(state)
            x, y = blank_pos[0] + move[0], blank_pos[1] + move[1]

            if 0 <= x < 3 and 0 <= y < 3:
                new_state[blank_pos[0]][blank_pos[1]] = new_state[x][y]
                new_state[x][y] = 0
                next_states.append(new_state)

        return next_states

    def solve(self):
        priority_queue = []
        hq.heappush(priority_queue, (self.calc_heuristic(self.initial_state), self.initial_state))
        visited_states = set()
        came_from = {}

        while priority_queue:
            current_state = hq.heappop(priority_queue)[1]

            if self.is_goal_state(current_state):
                self.solution_path = [current_state]
                while current_state!=self.initial_state:
                    current_state = came_from[str(current_state)]
                    self.solution_path.append(current_state)

                return self.solution_path

            visited_states.add(str(current_state))
            next_states = self.generate_next_states(current_state)

            for next_state in next_states:
                if str(next_state) not in visited_states:
                    hq.heappush(priority_queue, (self.calc_heuristic(next_state), next_state))
                    came_from[str(next_state)] = current_state

    def reset(self):
        self.solution_path = []
        self.is_running = False
