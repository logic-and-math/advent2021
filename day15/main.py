import os
from pathlib import Path
import itertools
import functools
from typing import List
import sys
from sortedcontainers import SortedSet
from queue import PriorityQueue


sys.setrecursionlimit(10000000)
input_p = Path(os.getcwd()) / 'input'
text = input_p.read_text()
lines = text.splitlines()

matrix = []
for l in lines:
    matrix.append([int(i) for i in l])
n_rows = len(matrix)
n_cols = len(matrix[0])


def get_neighbors(i, j, n_rows, n_cols):
    possible = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
    valid = [n for n in possible if n[0] >= 0 and n[0] < n_rows and n[1] >= 0 and n[1] < n_cols]
    return valid


def djikstra(my_matrix, n_rows, n_cols):
    large_number = 10000000000000
    start = (0,0)
    target = (n_rows - 1, n_cols - 1)

    all_indexes = [(i,j) for i in range(n_rows) for j in range(n_cols)]

    vertices = set(all_indexes)
    prev = {}  
    dist = {v: large_number for v in all_indexes}
    dist[start] = 0
    
    prior_queue = PriorityQueue()
    for (i,j) in all_indexes[1:]:
        prior_queue.put_nowait(((i,j), large_number))
    prior_queue.put_nowait(( (0,0), 0))

    while len(vertices) > 0:
        curr_v = prior_queue.get_nowait()[0]
        if curr_v not in vertices:
            continue
        
        vertices.remove(curr_v)

        if curr_v == target:
            break

        for n in get_neighbors(curr_v[0], curr_v[1], n_rows, n_cols):
            if n not in vertices:
                continue

            alt = dist[curr_v] + my_matrix[n[0]][n[1]]

            if alt < dist[n]:
                dist[n] = alt
                prev[n] = curr_v
                prior_queue.put_nowait((n, alt))
    return dist, prev


dist, prev = djikstra(matrix, n_rows, n_cols)
target = (n_rows - 1, n_cols - 1)
path = [target]

while True:
    if path[-1] not in prev:
        break
    path.append(prev[path[-1]])

print(sum([matrix[t[0]][t[1]] for t in path]))

def increment_matrix(matrix):
    new_matrix = []
    for i in range(n_rows):
        new_matrix.append([])
        for j in range(n_cols):
            new_value = matrix[i][j] + 1
            if new_value == 10:
                new_value = 1
            new_matrix[-1].append(new_value)

    return new_matrix


def increment_row(row):
    new_row = []
    for v in row:
        new_v = v + 1
        if new_v == 10:
            new_v = 1
        new_row.append(new_v)
    return new_row

full_matrix = [row for row in matrix] # start by filling the row

for i in range(4): # then create all rows
    prev_matrix = full_matrix[-n_rows : ]
    new_matrix = increment_matrix(prev_matrix)
    full_matrix.extend(new_matrix)

#then propagate rows to columns

for row in full_matrix:
    for i in range(4):
        row.extend(increment_row(row[-n_cols:]))
    print(row)
dist, prev = djikstra(full_matrix, n_rows * 5, n_cols * 5)
target = (n_rows * 5 - 1, n_cols * 5 - 1)
path = [target]

while True:
    if path[-1] not in prev:
        break
    path.append(prev[path[-1]])

print(sum([full_matrix[t[0]][t[1]] for t in path]))
