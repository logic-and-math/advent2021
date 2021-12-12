import os
from pathlib import Path
import itertools
import functools
from typing import List

input_p = Path(os.getcwd()) / 'input'
text = input_p.read_text()

connections = []

for l in text.splitlines():
    c1, c2 = l.split("-")
    if c1 == 'start' or c2 == 'end':
        conn = (c1, c2)
    elif c2 == 'start' or c1 == 'end':
        conn = (c2, c1)
    else:
        conn = (c1, c2)
    
    connections.append(conn)

connections_map = {}
for conn in connections:
    x1, x2 = conn

    if x1 not in connections_map:
        connections_map[x1] = []
    connections_map[x1].append(x2)
    
    if x1 == 'start' or x2 == 'end':
        continue

    if x2 not in connections_map:
        connections_map[x2] = []
    connections_map[x2].append(x1)


solutions = []

def get_cave_counts(caves: List[str]):
    cave_counts = {}
    for cave in caves:
        cave_counts[cave] = cave_counts.get(cave, 0) + 1
    return cave_counts

def solve(cave, solution, allow_twice):
    solution.append(cave)

    if cave == 'end':
        solutions.append([c for c in solution])
        solution.pop()
        return
    
    large_filter = lambda c: c[0].isupper()
    small_filter = lambda c: c[0].islower()

    small_cave_counts = get_cave_counts([c for c in solution if small_filter(c)])
    any_cave_appears_twice = any([v >= 2 for v in small_cave_counts.values()])

    if allow_twice and not any_cave_appears_twice:
        count_filter = lambda c: small_cave_counts.get(c, 0) <= 1
    else:
        count_filter = lambda c: small_cave_counts.get(c, 0) == 0

    caves_to_visit = [c for c in connections_map[cave] if large_filter(c) or (small_filter(c) and count_filter(c))]
    for cave in caves_to_visit:
        solve(cave, solution, allow_twice)
    
    solution.pop()

solve('start', [], False)
print(len(solutions))

solutions.clear()
solve('start', [], True)
print(len(solutions))

