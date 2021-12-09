import os
from pathlib import Path

input_p = Path(os.getcwd()) / 'input'
text = input_p.read_text()
matrix = []
for l in text.splitlines():
    matrix.append([int(c) for c in l])

n_columns = len(matrix[0])
n_rows = len(matrix)

def get_neighbors(row, col):
    neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
    neighbors_filtered = [n for n in neighbors if n[0] >= 0 and n[0] < n_rows and n[1] >= 0 and n[1] < n_columns]
    return neighbors_filtered

def is_low_point(row, col):
    neighbors = get_neighbors(row, col)
    return all([matrix[row][col] < matrix[i][j] for (i,j) in neighbors])

# part 1
low_points = []
for i in range(n_rows):
    for j in range(n_columns):
        if is_low_point(i, j):
            low_points.append((i,j))

low_points_values = [matrix[i][j] for (i,j) in low_points]
risk_levels = [v + 1 for v in low_points_values]
print(sum(risk_levels))

#part 2
basins = []
for l_p in low_points:
    visited = set()
    stack = [l_p]

    while len(stack) > 0:
        p = stack.pop()
        visited.add(p)
        p_value = matrix[p[0]][p[1]]

        neighbors = get_neighbors(p[0], p[1])
        for n in neighbors:
            n_value = matrix[n[0]][n[1]]
            if n not in visited and n_value != 9 and n_value > p_value:
                stack.append(n)

    basins.append(list(visited))

basins_sorted = sorted(basins, key=lambda b: len(b), reverse=True)
result = len(basins_sorted[0]) * len(basins_sorted[1]) * len(basins_sorted[2])
print(result)