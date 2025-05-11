import heapq
import random
from typing import List, Tuple, Optional

# ANSI color codes for terminal output
RED = "\033[91m"
RESET = "\033[0m"

def manhattan_distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
    """Calculate Manhattan distance between two points."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def find_start_end(maze: List[List[str]]) -> Tuple[Optional[Tuple[int, int]], Optional[Tuple[int, int]]]:
    """Find the start ('S') and end ('E') positions in the maze."""
    start = None
    end = None
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 'S':
                start = (i, j)
            elif maze[i][j] == 'E':
                end = (i, j)
    return start, end

def is_valid_move(maze: List[List[str]], pos: Tuple[int, int]) -> bool:
    """Check if the position is within bounds and not an obstacle."""
    rows, cols = len(maze), len(maze[0])
    return 0 <= pos[0] < rows and 0 <= pos[1] < cols and maze[pos[0]][pos[1]] != '1'

def get_neighbors(pos: Tuple[int, int], maze: List[List[str]]) -> List[Tuple[int, int]]:
    """Get valid neighboring positions (up, down, left, right)."""
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    neighbors = []
    for dx, dy in directions:
        new_pos = (pos[0] + dx, pos[1] + dy)
        if is_valid_move(maze, new_pos):
            neighbors.append(new_pos)
    return neighbors

def generate_random_maze(rows: int = 10, cols: int = 10, obstacle_prob: float = 0.2) -> List[List[str]]:
    """Generate a random maze with 'S', 'E', obstacles ('1'), and free cells ('0')."""
    # Initialize maze with free cells
    maze = [['0' for _ in range(cols)] for _ in range(rows)]
    
    # Place start ('S') and end ('E') randomly
    start_x, start_y = random.randint(0, rows-1), random.randint(0, cols-1)
    maze[start_x][start_y] = 'S'
    
    # Ensure 'E' is not at the same position as 'S'
    while True:
        end_x, end_y = random.randint(0, rows-1), random.randint(0, cols-1)
        if (end_x, end_y) != (start_x, start_y):
            maze[end_x][end_y] = 'E'
            break
    
    # Add random obstacles
    for i in range(rows):
        for j in range(cols):
            if maze[i][j] not in ['S', 'E'] and random.random() < obstacle_prob:
                maze[i][j] = '1'
    
    # Ensure there is a path from S to E (simplified check by running A* internally)
    if not a_star(maze, validate_only=True):
        # If no path exists, retry generating a new maze
        return generate_random_maze(rows, cols, obstacle_prob)
    
    return maze

def a_star(maze: List[List[str]], validate_only: bool = False) -> Optional[List[Tuple[int, int]]]:
    """Implement A* algorithm to find the shortest path from S to E."""
    start, end = find_start_end(maze)
    
    if not start or not end:
        if not validate_only:
            print("Invalid maze: Missing start ('S') or end ('E').")
        return None
    
    # Priority queue: (f_score, position, path)
    open_list = [(0, start, [start])]
    heapq.heapify(open_list)
    
    # Track visited nodes and their g_scores
    g_scores = {start: 0}
    visited = set()
    
    while open_list:
        f_score, current, path = heapq.heappop(open_list)
        
        if current == end:
            return path
        
        if current in visited:
            continue
        
        visited.add(current)
        
        for neighbor in get_neighbors(current, maze):
            # Cost to move to neighbor is always 1
            tentative_g_score = g_scores.get(current, float('inf')) + 1
            
            if neighbor not in g_scores or tentative_g_score < g_scores[neighbor]:
                # Update g_score and path
                g_scores[neighbor] = tentative_g_score
                h_score = manhattan_distance(neighbor, end)
                f_score = tentative_g_score + h_score
                new_path = path + [neighbor]
                heapq.heappush(open_list, (f_score, neighbor, new_path))
    
    if not validate_only:
        print("No solution: No path exists from S to E.")
    return None

def display_maze_with_path(maze: List[List[str]], path: List[Tuple[int, int]]) -> None:
    """Display the maze with the path highlighted in red using '*'."""
    maze_copy = [row[:] for row in maze]
    for x, y in path:
        if maze_copy[x][y] not in ['S', 'E']:
            maze_copy[x][y] = '*'
    
    print("Labirinto com o caminho destacado (caminho em vermelho):")
    for row in maze_copy:
        colored_row = []
        for cell in row:
            if cell == '*':
                colored_row.append(f"{RED}{cell}{RESET}")
            else:
                colored_row.append(cell)
        print(' '.join(colored_row))

def main():
    """Main function to run the PathFinder with a random maze."""
    # Generate a random 10x10 maze with 20% obstacle probability
    maze = generate_random_maze(rows=10, cols=10, obstacle_prob=0.2)
    
    print("Labirinto inicial:")
    for row in maze:
        print(' '.join(row))
    
    path = a_star(maze)
    
    if path:
        print("\nMenor caminho (em coordenadas):")
        path_str = [f"{'s' if maze[x][y] == 'S' else 'e' if maze[x][y] == 'E' else ''}({x}, {y})" for x, y in path]
        print('[' + ', '.join(path_str) + ']')
        print()
        display_maze_with_path(maze, path)

if __name__ == "__main__":
    main()