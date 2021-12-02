import os
from pathlib import Path
from typing import Tuple, List
import functools

def command_to_tuple(s: str) -> Tuple[str, int]:
    splits = s.split(" ")
    return (splits[0], int(splits[1]))

input_p = Path(os.getcwd()) / 'input'
text = input_p.read_text()
commands: List[Tuple[str, int]] = [command_to_tuple(l) for l in text.splitlines()]

forward_commands = [c[1] for c in commands if c[0] == "forward"]
up_commands = [c[1] for c in commands if c[0] == "up"]
down_commands = [c[1] for c in commands if c[0] == "down"]

#first part
add = lambda a,b: a + b
horizontal = functools.reduce(add, forward_commands, 0)
depth = functools.reduce(add, down_commands, 0)
depth -= functools.reduce(add, up_commands, 0)

print(horizontal * depth)

#second part
aim = 0
horizontal = 0
depth = 0
for command in commands:
    if command[0] == "down":
        aim += command[1]
    elif command[0] == "up":
        aim -= command[1]
    else:
        horizontal += command[1]
        depth += aim * command[1]

print(horizontal * depth)