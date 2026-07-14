import heapq

# Goal state
GOAL = ((1, 2, 3),
        (4, 5, 6),
        (7, 8, 0))


class PuzzleNode:
    def __init__(self, state, parent=None, move="", g=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.g = g  # Cost from start
        self.h = self.manhattan_distance()
        self.f = self.g + self.h

    def manhattan_distance(self):
        distance = 0
        for i in range(3):
            for j in range(3):
                value = self.state[i][j]
                if value != 0:
                    goal_x = (value - 1) // 3
                    goal_y = (value - 1) % 3
                    distance += abs(i - goal_x) + abs(j - goal_y)
        return distance

    def __lt__(self, other):
        return self.f < other.f


def get_neighbors(state):
    neighbors = []
    directions = {
        "Up": (-1, 0),
        "Down": (1, 0),
        "Left": (0, -1),
        "Right": (0, 1)
    }

    # Find blank (0)
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                x, y = i, j

    for move, (dx, dy) in directions.items():
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = [list(row) for row in state]
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            neighbors.append((tuple(map(tuple, new_state)), move))

    return neighbors


def reconstruct_path(node):
    path = []
    while node.parent:
        path.append(node.move)
        node = node.parent
    return path[::-1]


def a_star(start):
    open_list = []
    closed_set = set()

    start_node = PuzzleNode(start)
    heapq.heappush(open_list, start_node)

    while open_list:
        current = heapq.heappop(open_list)

        if current.state == GOAL:
            return reconstruct_path(current)

        closed_set.add(current.state)

        for neighbor_state, move in get_neighbors(current.state):
            if neighbor_state in closed_set:
                continue

            neighbor = PuzzleNode(
                neighbor_state,
                current,
                move,
                current.g + 1
            )
            heapq.heappush(open_list, neighbor)

    return None


def print_state(state):
    for row in state:
        print(row)
    print()


# Example initial state
start_state = (
    (1, 2, 3),
    (4, 0, 6),
    (7, 5, 8)
)

print("Initial State:")
print_state(start_state)

solution = a_star(start_state)

if solution:
    print("Solution found!")
    print("Number of moves:", len(solution))
    print("Moves:")
    for move in solution:
        print(move)
else:
    print("No solution exists.")
