import os
from pathlib import Path
import itertools
from dataclasses import dataclass
from typing import List

@dataclass
class Entry:
    signals: List[str]
    outputs: List[str]

def line_to_entry(l) -> Entry:
    signals_s, outputs_s = l.split(" | ")
    return Entry(signals_s.split(" "), outputs_s.split(" "))

input_p = Path(os.getcwd()) / 'input'
text = input_p.read_text()
entries = [line_to_entry(l) for l in text.splitlines()]

#first part
n_digits_to_digit = {2: 1, 4: 4, 3: 7, 7: 8}
digits = [d for e in entries for d in e.outputs if len(d) in n_digits_to_digit]
print(len(digits))

#second part
letters = ["a", "b", "c", "d", "e", "f", "g"]
letter_to_pos = {l: i for (i,l) in enumerate(letters)}
def_configuration = ["abcefg", "cf", "acdeg", "acdfg", "bcdf", "abdfg", "abdefg", "acf", "abcdefg", "abcdfg"]

def conf_from_mappings(mappings):
    new_configuration = []
    for s in def_configuration:
        new_s = "".join([letters[mappings[letter_to_pos[c]]] for c in s])
        new_configuration.append(new_s)
    return new_configuration

def check_solution(signals, mappings):
    new_configuration = conf_from_mappings(mappings)
    sorted_signals = set(["".join(sorted(s)) for s in signals])
    sorted_conf = set(["".join(sorted(s)) for s in new_configuration])

    return sorted_signals == sorted_conf

def find_solution(signals, mappings, marked, pos):

    if pos == len(letters):
        res = check_solution(signals, mappings)
        return mappings if res else None

    for i in range(len(letters)):
        if not marked[i]:
            mappings[pos] = i
            marked[i] = True

            res = find_solution(signals, mappings, marked, pos + 1)
            if res is not None:
                return res

            marked[i] = False
    

def calculate_value(outputs, solution):
    conf = conf_from_mappings(solution)
    conf_sorted_to_value = {"".join(sorted(s)): i for (i,s) in enumerate(conf)}
    outputs_sorted = ["".join(sorted(s)) for s in outputs]

    output_value = [str(conf_sorted_to_value[s]) for s in outputs_sorted]
    return output_value

result = 0
for entry in entries:
    mappings = [0] * len(letters)
    marked = [False] * len(letters)

    solution = find_solution(entry.signals, mappings, marked, 0)
    value = int("".join(calculate_value(entry.outputs, solution)))
    result += value

print(result)