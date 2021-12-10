import os
from pathlib import Path
import itertools
import functools

input_p = Path(os.getcwd()) / 'input'
text = input_p.read_text()
lines = text.splitlines()

openings = set(["(", "[", "{", "<"])
opening_to_closing = {"(": ")", "[": "]", "{": "}", "<": ">"}
closings = set([")", "]", "}", ">"])
closing_to_score = {")": 3, "]": 57, "}": 1197, ">": 25137}

#part 1
def solve_line(line):
    stack = []
    for c in line:
        if c in openings:
            stack.append(opening_to_closing[c])
        else:
            expected = stack.pop()
            if expected != c:
                return c

    return ""

results = [solve_line(l) for l in lines]
results = [r for r in results if r != ""]
result = sum([closing_to_score[c] for c in results])
print(result)

#part 2
def get_line_closings(line):
    next_closings = []

    for c in line:
        if c in openings:
            next_closings.append(opening_to_closing[c])
        else:
            next_closings.pop()

    next_closings.reverse()
    return next_closings


def calculate_score(next_closings):
    to_score = {")": 1, "]": 2, "}": 3, ">": 4}
    reduce = lambda prev, curr: prev * 5 + to_score[curr]
    return functools.reduce(reduce, next_closings, 0)
    
incomplete_lines = [l for l in lines if solve_line(l) == ""]
line_closings = [get_line_closings(l) for l in incomplete_lines]
scores = [calculate_score(c) for c in line_closings]
scores.sort()
print(scores[int(len(scores) / 2)])
