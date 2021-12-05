import os
from pathlib import Path
from typing import Tuple, List
from dataclasses import dataclass
from collections import Counter

import functools
import itertools
import operator

@dataclass
class Vent:
    start: Tuple[int, int]
    end: Tuple[int, int]


def line_to_vent(l: str) -> Vent:
    def coord_to_tuple(coord: str) -> Tuple[int, int]:
        first, second = coord.split(",")
        return (int(first), int(second))

    start_s, end_s = l.split(' -> ')
    return Vent(coord_to_tuple(start_s), coord_to_tuple(end_s))


def get_points_horizontal(v: Vent) -> List[Tuple[int, int]]:
    range_start = min(v.start[0], v.end[0])
    range_end = max(v.start[0], v.end[0]) + 1
    return [(x, v.start[1]) for x in range(range_start, range_end)]


def get_points_vertical(v: Vent) -> List[Tuple[int, int]]:
    range_start = min(v.start[1], v.end[1])
    range_end = max(v.start[1], v.end[1]) + 1
    return [(v.start[0], y) for y in range(range_start, range_end)]


def get_points_diagonal(v: Vent) -> List[Tuple[int, int]]:
    start_point = min(v.start, v.end, key=lambda p: p[0])
    end_point = max(v.start, v.end, key=lambda p: p[0])

    slope = 1 if end_point[1] > start_point[1] else -1
    y = lambda x: slope * (x - start_point[0]) + start_point[1]

    return [(x, y(x)) for x in range(start_point[0], end_point[0] + 1)]

input_p = Path(os.getcwd()) / 'input'
text = input_p.read_text()
vents = [line_to_vent(l) for l in text.splitlines()]

horizontal = [v for v in vents if v.start[1] == v.end[1]]
vertical = [v for v in vents if v.start[0] == v.end[0]]
diagonal = [v for v in vents if v not in horizontal and v not in vertical]

horizontal_points = [get_points_horizontal(v) for v in horizontal]
vertical_points = [get_points_vertical(v) for v in vertical]
diagonal_points = [get_points_diagonal(v) for v in diagonal]

all_points = itertools.chain(*horizontal_points, *vertical_points, *diagonal_points)

counter = Counter(all_points)
more_than_2 = [k for k in counter.keys() if counter[k] >= 2]
print(len(more_than_2))