import os
from pathlib import Path
from typing import Tuple, List
import functools
import itertools
import operator

def command_to_tuple(s: str) -> Tuple[str, int]:
    splits = s.split(" ")
    return (splits[0], int(splits[1]))

input_p = Path(os.getcwd()) / 'input'
text = input_p.read_text()
commands: List[Tuple[str, int]] = [command_to_tuple(l) for l in text.splitlines()]

forward_commands = [c[1] if c[0] == "forward" else 0 for c in commands]
up_commands = [c[1] if c[0] == "up" else 0 for c in commands]
down_commands = [c[1] if c[0] == "down" else 0 for c in commands]

print(sum(forward_commands) * (sum(down_commands) - sum(up_commands)))

#part 2
aim_increments = [down - up for (down,up) in zip(down_commands, up_commands)]
aims = itertools.accumulate(aim_increments, operator.add)

collect = lambda a,b: a + (b[0] * b[1])
depth = functools.reduce(collect, zip(aims, forward_commands), 0)

print(sum(forward_commands) * depth)
