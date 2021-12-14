import os
from pathlib import Path
import itertools
import functools
from typing import List

input_p = Path(os.getcwd()) / 'input'
text = input_p.read_text()
lines = text.splitlines()

def line_to_rule(l):
    split = l.split(" -> ")
    return (split[0], split[1])

start = lines[0]
rules = [line_to_rule(l) for l in lines[2:]]
rules_map = {r[0]: r[1] for r in rules}

#part 1
def do_step(polymer):
    pairs = [polymer[i:i+2] for i in range(0, len(polymer) - 1)]
    new_pairs = [p[0] + rules_map.get(p,"") + p[1] for p in pairs]

    pairs_for_joining = [p if i == 0 else p[1:] for (i,p) in enumerate(new_pairs)]
    new_polymer = "".join(pairs_for_joining)
    return new_polymer

polymer = start
for i in range(10):
    polymer = do_step(polymer)

counts = {}
for c in polymer:
    counts[c] = counts.get(c, 0) + 1

print(max(counts.values()) - min(counts.values()))
print("####################")

# part 2
polymer = start

pair_counts = {} # pair to count
n_duplicates = {} #char to count

#build initial pairs and initial duplicate characters (whenever a pair splits the new character is duplicated and propagated)
pairs = [polymer[i:i+2] for i in range(0, len(polymer) - 1)]
for p in pairs:
    pair_counts[p] = pair_counts.get(p, 0) + 1
    if p != pairs[0]:
        n_duplicates[p[0]] = n_duplicates.get(p[0], 0) + 1


for i in range(40):

    pairs_to_add = {} #pair to count
    pairs_to_remove = {} #pair to count

    for (p, v) in pair_counts.items():
        if p in rules_map:

            new_char = rules_map[p]
            n_duplicates[new_char] = n_duplicates.get(new_char, 0) +  v

            n_p_1 = p[0] + new_char
            n_p_2 = new_char + p[1]
            
            pairs_to_add[n_p_1] = pairs_to_add.get(n_p_1, 0) + v
            pairs_to_add[n_p_2] = pairs_to_add.get(n_p_2, 0) + v

            pairs_to_remove[p] = pairs_to_remove.get(p, 0) - v

    for (p,v) in pairs_to_add.items():
        pair_counts[p] = pair_counts.get(p, 0) + v
    for (p,v) in pairs_to_remove.items():
        pair_counts[p] += v


chars = set()
for (k,v) in pair_counts.items():
    if v != 0:
        chars.add(k[0])
        chars.add(k[1])

counts = {}
for c in chars:
    pairs_containing_char = [(k,v) for (k,v) in pair_counts.items() if k[0] == c or k[1] == c]
    total = 0
    for (k,v) in pairs_containing_char:

        if k == c + c: #BB,CC...
            total += 2 * v
        else:
            total += v
    counts[c] = total - n_duplicates.get(c,0)
    # print(c, ": ", total - n_duplicates.get(c, 0))

print(max(counts.values()) - min(counts.values()))
