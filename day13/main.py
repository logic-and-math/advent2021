import os
from pathlib import Path
import itertools
import functools
from typing import List

input_p = Path(os.getcwd()) / 'input'
text = input_p.read_text()
lines = text.splitlines()

def line_to_instruction(l):
    s = l[11:]
    name, number = s.split("=")
    return (name, int(number))

split_index = [i for (i,l) in enumerate(lines) if l == ""][0]
coordinates = [(int(s.split(",")[1]), int(s.split(",")[0])) for s in lines[:split_index]]
instructions = [line_to_instruction(l) for l in lines[split_index + 1:]]


def fold(coordinates, instruction):
    if instruction[0] == 'y':
        bottom_coordinates = [c for c in coordinates if c[0] > instruction[1]]
        top_coordinates = [c for c in coordinates if c[0] < instruction[1]]
        new_locations = [(instruction[1] - (c[0] - instruction[1]), c[1]) for c in bottom_coordinates]

        new_coordinates = set()
        for c in new_locations + top_coordinates:
            new_coordinates.add(c)
    else:
        
        left_coordinates = [c for c in coordinates if c[1] < instruction[1]]
        right_coordinates = [c for c in coordinates if c[1] > instruction[1]]
        new_locations = [(c[0], instruction[1] - (c[1] - instruction[1])) for c in right_coordinates]

        new_coordinates = set()
        for c in new_locations + left_coordinates:
            new_coordinates.add(c)


    return list(new_coordinates)


for instruction in instructions:
    coordinates = fold(coordinates, instruction)

n_rows = max([c[0] for c in coordinates]) + 1
n_cols = max([c[1] for c in coordinates]) + 1
points_set = set(coordinates)

for i in range(n_rows):
    for j in range(n_cols):
        if (i,j) in points_set:
            print("#", end="")
        else:
            print(".", end="")
    print("")
