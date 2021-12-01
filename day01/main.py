import os
from pathlib import Path

input_p = Path(os.getcwd()) / 'input'
text = input_p.read_text()
measurements = [int(i) for i in text.splitlines()]

increases = [measurements[i] for i in range(1, len(measurements)) if measurements[i] > measurements[i-1]]
print(len(increases))

triplets = [[measurements[i-1], measurements[i], measurements[i+1]] for i in range(1, len(measurements) - 1)]
increases_triplets = [triplets[i] for i in range(1, len(triplets)) if sum(triplets[i]) > sum(triplets[i-1])]
print(len(increases_triplets))