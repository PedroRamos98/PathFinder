import heapq
import random
from typing import List, Tuple, Optional

# Códigos ANSI para cores no terminal
RED = "\033[91m"
RESET = "\033[0m"

# ------------------------ FUNÇÕES AUXILIARES ------------------------

def manhattan_distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
    """Calcula a distância de Manhattan entre dois pontos."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def find_start_end(maze: List[List[str]]) -> Tuple[Optional[Tuple[int, int]], Optional[Tuple[int, int]]]:
    """Encontra as posições de início ('S') e fim ('E') no labirinto."""
    start = end = None
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 'S':
                start = (i, j)
            elif maze[i][j] == 'E':
                end = (i, j)
    return start, end

def is_valid_move(maze: List[List[str]], pos: Tuple[int, int]) -> bool:
    """Verifica se a posição é válida (dentro dos limites e não é obstáculo)."""
    rows, cols = len(maze), len(maze[0])
    return 0 <= pos[0] < rows and 0 <= pos[1] < cols and maze[pos[0]][pos[1]] != '1'

def get_neighbors(pos: Tuple[int, int], maze: List[List[str]]) -> List[Tuple[int, int]]:
    """Retorna os vizinhos válidos (cima, baixo, esquerda, direita)."""
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    return [ (pos[0]+dx, pos[1]+dy) for dx, dy in directions if is_valid_move(maze, (pos[0]+dx, pos[1]+dy)) ]

# ------------------------ GERAÇÃO DO LABIRINTO ------------------------

def generate_random_maze(rows: int = 10, cols: int = 10, obstacle_prob: float = 0.2) -> List[List[str]]:
    """Gera um labirinto aleatório com obstáculos, 'S' (start) e 'E' (end)."""
    maze = [['0' for _ in range(cols)] for _ in range(rows)]

    # Posicionar 'S' (início)
    start_x, start_y = random.randint(0, rows - 1), random.randint(0, cols - 1)
    maze[start_x][start_y] = 'S'

    # Posicionar 'E' (fim) em local diferente
    while True:
        end_x, end_y = random.randint(0, rows - 1), random.randint(0, cols - 1)
        if (end_x, end_y) != (start_x, start_y):
            maze[end_x][end_y] = 'E'
            break

    # Inserir obstáculos aleatórios
    for i in range(rows):
        for j in range(cols):
            if maze[i][j] not in ['S', 'E'] and random.random() < obstacle_prob:
                maze[i][j] = '1'

    # Verifica se existe caminho com A*
    if not a_star(maze, validate_only=True):
        return generate_random_maze(rows, cols, obstacle_prob)

    return maze

# ------------------------ A* ALGORITHM ------------------------

def a_star(maze: List[List[str]], validate_only: bool = False) -> Optional[List[Tuple[int, int]]]:
    """Executa o algoritmo A* no labirinto para encontrar o menor caminho."""
    start, end = find_start_end(maze)
    if not start or not end:
        if not validate_only:
            print("Labirinto inválido: faltando 'S' ou 'E'.")
        return None

    # Fila de prioridade: (f_score, posição atual, caminho até aqui)
    open_list = [(0, start, [start])]
    heapq.heapify(open_list)

    # g_score = custo do início até o nó atual
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
            tentative_g_score = g_scores[current] + 1

            if neighbor not in g_scores or tentative_g_score < g_scores[neighbor]:
                g_scores[neighbor] = tentative_g_score
                h_score = manhattan_distance(neighbor, end)
                total_score = tentative_g_score + h_score
                heapq.heappush(open_list, (total_score, neighbor, path + [neighbor]))

    if not validate_only:
        print("Sem solução: nenhum caminho de 'S' até 'E'.")
    return None

# ------------------------ EXIBIÇÃO ------------------------

def display_maze_with_path(maze: List[List[str]], path: List[Tuple[int, int]]) -> None:
    """Exibe o labirinto com o caminho encontrado colorido."""
    maze_copy = [row[:] for row in maze]
    for x, y in path:
        if maze_copy[x][y] not in ['S', 'E']:
            maze_copy[x][y] = '*'

    print("Labirinto com caminho encontrado (em vermelho):")
    for row in maze_copy:
        print(' '.join(f"{RED}{cell}{RESET}" if cell == '*' else cell for cell in row))

# ------------------------ MAIN ------------------------

def main():
    """Executa a geração do labirinto, encontra o caminho e exibe o resultado."""
    maze = generate_random_maze(rows=10, cols=10, obstacle_prob=0.2)

    print("Labirinto gerado:")
    for row in maze:
        print(' '.join(row))

    path = a_star(maze)

    if path:
        print("\nCoordenadas do menor caminho:")
        formatted = [f"{'s' if maze[x][y] == 'S' else 'e' if maze[x][y] == 'E' else ''}({x}, {y})" for x, y in path]
        print('[' + ', '.join(formatted) + ']\n')
        display_maze_with_path(maze, path)

if __name__ == "__main__":
    main()
