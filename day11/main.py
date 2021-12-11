import os
from pathlib import Path
import itertools
import functools
from typing import List

input_p = Path(os.getcwd()) / 'input'
text = input_p.read_text()
matrix: List[List[int]] = []
for l in text.splitlines():
    matrix.append([int(i) for i in l])

def matrix_generator():
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            yield (i,j)

def get_neighbors(i, j):
    n_rows = len(matrix)
    n_cols = len(matrix[0])

    neighbors = [(i - 1, j - 1), (i - 1, j), (i - 1, j + 1), (i, j - 1), (i, j + 1), (i + 1, j - 1), (i + 1, j), (i + 1, j + 1)]
    neighbors = [n for n in neighbors if n[0] >= 0 and n[0] < n_rows and n[1] >= 0 and n[1] < n_cols]
    return neighbors
    

def process_step(matrix):

    flashed = set()

    for (i,j) in matrix_generator():
        matrix[i][j] += 1

    should_flash = [(i,j) for (i,j) in matrix_generator() if (matrix[i][j] > 9)]

    for (i,j) in should_flash:

        stack = [(i,j)] #all that will flash from the current position
        while len(stack) > 0:
            co = stack.pop()
            if co in flashed: #because it could have flashed in some previous position
                continue

            matrix[co[0]][co[1]] += 1
            flashed.add(co)

            for n in get_neighbors(co[0], co[1]):
                matrix[n[0]][n[1]] += 1
                if matrix[n[0]][n[1]] > 9 and n not in flashed:
                    stack.append(n)
    
    for (i, j) in flashed:
        matrix[i][j] = 0

    return len(flashed)

#part 1
result = sum([process_step(matrix) for _ in range(100)])


#part 2 
#refresh matrix cause the previous part already processed a 100 steps
matrix= []
for l in text.splitlines():
    matrix.append([int(i) for i in l])

i = 1
while True:
    res = process_step(matrix)
    if (res == 100):
        break
    i += 1

print(i)