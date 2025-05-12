# PathFinder - Resolvendo o Labirinto 2D com o Algoritmo A*

## Descrição do Projeto

O **PathFinder** é um projeto desenvolvido para encontrar o menor caminho em um labirinto 2D, utilizando o algoritmo A*. O objetivo é guiar um robô de resgate do ponto inicial (`S`) ao ponto final (`E`), evitando obstáculos (`1`) e movendo-se apenas por células livres (`0`). O algoritmo A* combina o custo do caminho percorrido (`g`) com uma estimativa heurística da distância até o destino (`h`), usando a **distância de Manhattan**, para determinar o caminho mais eficiente. O programa gera um novo labirinto aleatoriamente a cada execução e destaca o caminho encontrado em vermelho no terminal.

## Introdução ao Problema

O problema consiste em navegar por um labirinto representado como uma matriz 2D, onde:
- `0`: Célula livre (pode ser atravessada).
- `1`: Obstáculo (não pode ser atravessado).
- `S`: Ponto inicial (start).
- `E`: Ponto final (end).

O robô pode se mover nas direções **cima, baixo, esquerda e direita**, com um custo de movimento igual a **1** por célula. O algoritmo A* é ideal para este problema, pois garante o menor caminho (em termos de custo total) ao explorar eficientemente as possíveis rotas com base na soma de:
- **g(n)**: Custo do caminho desde o início até o nó atual.
- **h(n)**: Estimativa do custo restante até o destino (distância de Manhattan).
- **f(n) = g(n) + h(n)**: Custo total estimado.

## Requisitos

- **Python 3.6+**
- Nenhuma biblioteca externa é necessária (usa apenas bibliotecas padrão: `heapq`, `typing`, e `random`).
- Um terminal que suporte cores ANSI para visualizar o caminho destacado em vermelho (a maioria dos terminais modernos, como Windows Terminal, Linux, ou macOS, é compatível).

## Configuração e Execução

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/exemploaluno/pathfinder_a_star.git
   cd pathfinder_a_star
   ```

2. **Execute o programa**:
   ```bash
   python pathfinder.py
   ```
   - Um novo labirinto 10x10 será gerado automaticamente com 20% de probabilidade de obstáculos.
   - O caminho encontrado será destacado em vermelho no terminal.

3. **Modifique o labirinto** (opcional):
   - Edite a função `generate_random_maze` na função `main()` do arquivo `pathfinder.py` para alterar o tamanho do labirinto (linhas e colunas) ou a probabilidade de obstáculos.
   - Alternativamente, substitua a chamada a `generate_random_maze` por uma matriz fixa para testar labirintos específicos.
   - Certifique-se de que o labirinto contém exatamente um `S` e um `E`, e que as dimensões são consistentes.

## Funcionamento do Algoritmo A*

O algoritmo A* opera da seguinte forma:

1. **Inicialização**:
   - Localiza as posições de `S` e `E` na matriz do labirinto.
   - Cria uma fila de prioridade (`open_list`) com o nó inicial (`S`), inicializando seu custo `g = 0` e calculando `f = g + h`.

2. **Heurística**:
   - Usa a **distância de Manhattan**: `h(n) = |x_atual - x_final| + |y_atual - y_final|`.
   - Essa heurística é **admissível** (nunca superestima o custo real) e **consistente**, garantindo a optimalidade do caminho.

3. **Exploração**:
   - Remove o nó com menor `f(n)` da fila de prioridade.
   - Verifica seus vizinhos (cima, baixo, esquerda, direita).
   - Para cada vizinho válido:
     - Calcula o novo custo `g` (adicionando 1 ao custo do nó atual).
     - Calcula `h` (distância de Manhattan até `E`).
     - Se o novo `g` for menor que o anterior (ou o vizinho for novo), atualiza o caminho e adiciona à fila.

4. **Término**:
   - Se o nó atual for `E`, retorna o caminho encontrado.
   - If the queue empties without finding `E`, returns "No solution".

5. **Saída**:
   - Exibe o caminho como uma lista de coordenadas (ex.: `[s(0, 9), (1, 9), ..., e(8, 8)]`).
   - Mostra o labirinto com o caminho destacado em vermelho usando `*`.

## Geração de Labirintos Aleatórios

A cada execução, o programa gera um novo labirinto com as seguintes características:
- Tamanho padrão: 10x10 (pode ser ajustado).
- Probabilidade de obstáculos: 20% (cada célula livre tem 20% de chance de se tornar um obstáculo).
- Posições de `S` e `E` são escolhidas aleatoriamente.
- Um teste interno com A* garante que existe um caminho válido entre `S` e `E`. Se não houver caminho, um novo labirinto é gerado.

## Visualização do Caminho

O caminho encontrado é destacado no labirinto usando o símbolo `*`, que aparece em **vermelho** no terminal (usando códigos ANSI). Isso torna o trajeto visualmente distinto do restante do labirinto, facilitando a compreensão do caminho percorrido pelo robô.

## Exemplo de Entrada e Saída

### Entrada
Um labirinto 10x10 gerado aleatoriamente (exemplo):
```
0 0 1 0 0 0 1 0 0 S
0 1 0 0 1 0 0 0 1 0
0 0 0 1 0 0 0 1 0 0
1 0 0 0 0 1 0 0 0 0
0 0 1 0 0 0 0 0 1 0
0 1 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 1 0 0
0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0 0 E
1 0 0 0 0 0 0 0 1 0
```

### Saída
```
Labirinto inicial:
0 0 1 0 0 0 1 0 0 S
0 1 0 0 1 0 0 0 1 0
0 0 0 1 0 0 0 1 0 0
1 0 0 0 0 1 0 0 0 0
0 0 1 0 0 0 0 0 1 0
0 1 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 1 0 0
0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0 0 E
1 0 0 0 0 0 0 0 1 0

Menor caminho (em coordenadas):
[s(0, 9), (1, 9), (2, 9), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9), e(8, 8)]

Labirinto com o caminho destacado (caminho em vermelho):
0 0 1 0 0 0 1 0 0 S
0 1 0 0 1 0 0 0 1 *
0 0 0 1 0 0 0 1 0 *
1 0 0 0 0 1 0 0 0 *
0 0 1 0 0 0 0 0 1 *
0 1 0 0 0 0 0 0 0 *
0 0 0 0 1 0 0 1 0 *
0 0 1 0 0 0 0 0 0 *
0 0 0 0 0 1 0 0 0 E
1 0 0 0 0 0 0 0 1 0
```
(Note: Os asteriscos `*` aparecem em vermelho no terminal, mas não são visíveis em texto simples.)

### Caso Sem Solução
Embora improvável devido à validação do labirinto, se um labirinto sem caminho for fornecido manualmente, a saída será:
```
No solution: No path exists from S to E.
```

## Estrutura do Código

- **Funções principais**:
  - `manhattan_distance(p1, p2)`: Calcula a distância de Manhattan.
  - `find_start_end(maze)`: Localiza `S` e `E`.
  - `is_valid_move(maze, pos)`: Verifica se uma posição é válida.
  - `get_neighbors(pos, maze)`: Retorna vizinhos válidos.
  - `generate_random_maze(rows, cols, obstacle_prob)`: Gera um labirinto aleatório.
  - `a_star(maze, validate_only=False)`: Implementa o algoritmo A*, com opção de validação.
  - `display_maze_with_path(maze, path)`: Exibe o labirinto com o caminho em vermelho.
  - `main()`: Função principal para executar o programa.

- **Boas práticas**:
  - Código comentado e organizado.
  - Tipagem explícita com `typing`.
  - Tratamento de erros para labirintos inválidos.
  - Modularidade para facilitar manutenção.
  - Uso de cores ANSI para visualização clara.

## Contribuições

Este projeto foi desenvolvido por **Pedro Moreira Ramos**, **Davi Aguilar Nunes Oliveira** e **Rafael Parreira Chequer**. Contribuições incluem:
- Implementação do algoritmo A*.
- Adição de geração de labirintos aleatórios.
- Visualização do caminho em vermelho no terminal.
- Testes com diferentes labirintos.
- Redação e atualização do README.md.
- Commits no repositório GitHub.

## Como Contribuir

1. Faça um fork do repositório.
2. Crie uma branch para suas alterações (`git checkout -b feature/nova-funcionalidade`).
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`).
4. Push para a branch (`git push origin feature/nova-funcionalidade`).
5. Abra um Pull Request.
