import heapq

# Dictionary to store goal positions
goal_pos = {}

# Heuristic Function (Manhattan Distance)
def heuristic(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            if value != 0:
                x, y = goal_pos[value]
                distance += abs(i - x) + abs(j - y)
    return distance

# Find blank tile
def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

# Generate neighboring states
def get_neighbors(state):
    neighbors = []
    x, y = find_blank(state)

    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dx, dy in moves:
        nx, ny = x + dx, y + dy

        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = [row[:] for row in state]
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            neighbors.append(new_state)

    return neighbors

# Convert state to tuple
def state_to_tuple(state):
    return tuple(tuple(row) for row in state)

# A* Search Algorithm
def solve(initial, goal):
    open_list = []
    visited = set()

    heapq.heappush(open_list, (heuristic(initial), 0, initial, []))

    while open_list:
        f, g, current, path = heapq.heappop(open_list)

        if current == goal:
            return path + [current]

        current_tuple = state_to_tuple(current)

        if current_tuple in visited:
            continue

        visited.add(current_tuple)

        for neighbor in get_neighbors(current):
            if state_to_tuple(neighbor) not in visited:
                heapq.heappush(
                    open_list,
                    (
                        g + 1 + heuristic(neighbor),
                        g + 1,
                        neighbor,
                        path + [current],
                    ),
                )

    return None

# ---------------- MAIN PROGRAM ----------------

print("========== 8-Puzzle Solver ==========")
print("Leave the blank tile empty.")
print("Example:")
print("Row 1: 1,2,3")
print("Row 2: 4,,6")
print("Row 3: 7,5,8\n")

# Initial State
print("Enter Initial State:")
initial = []

for i in range(3):
    while True:
        row = input(f"Row {i+1}: ").split(",")
        if len(row) == 3:
            row = [0 if x.strip() == "" else int(x) for x in row]
            initial.append(row)
            break
        else:
            print("Please enter exactly 3 values separated by commas.")

# Goal State
print("\nEnter Goal State:")
goal = []

for i in range(3):
    while True:
        row = input(f"Row {i+1}: ").split(",")
        if len(row) == 3:
            row = [0 if x.strip() == "" else int(x) for x in row]
            goal.append(row)
            break
        else:
            print("Please enter exactly 3 values separated by commas.")

# Store goal positions
for i in range(3):
    for j in range(3):
        goal_pos[goal[i][j]] = (i, j)

# Solve the puzzle
solution = solve(initial, goal)

# Display Result
if solution:
    print("\nSolution Found!")
    print("Number of Moves:", len(solution) - 1)

    for step, state in enumerate(solution):
        print(f"\nStep {step}")
        for row in state:
            print([" " if x == 0 else x for x in row])
else:
    print("\nNo solution exists.")
