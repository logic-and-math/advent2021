import os
from pathlib import Path
import itertools
import functools
from typing import List

input_p = Path(os.getcwd()) / 'input'
text = input_p.read_text()
lines = text.splitlines()

full = lines[0][13:]
x_full, y_full = full.split(", ")
x_min, x_max = [int(i) for i in x_full[2:].split("..")]
y_min, y_max = [int(i) for i in y_full[2:].split("..")]


def x_solution_steps(x_velocity):
    steps = [] # at steps where it hits the solution but still has some velocity
    steps_plus = [] # at steps where it its the solution but it has 0 x velocity
    i = 0 # step
    vel = x_velocity # start velocity
    pos = 0 # start position

    while True:
        i += 1 # increase step
        pos += vel # increase x position by x velocity
        if vel != 0: # drag compensation
            vel += 1 if vel < 0 else -1

        if pos > x_max: # overshoot, no need to continue
            break

        is_valid = x_min <= pos <= x_max # is in target area
        if is_valid:
            if vel != 0: # can still move
                steps.append(i)
            else: # can't move anymore, finish
                steps_plus.append(i)
                break
        
        if vel == 0: # if not valid and vel is 0
            break
    return steps, steps_plus


x_values = range(1, x_max + 1)
x_to_sols = {x: x_solution_steps(x) for x in x_values if len(x_solution_steps(x)[0]) > 0 or len(x_solution_steps(x)[1]) > 0}

def get_y_values_for_step(x, step):
    y_finals = range(y_min, y_max + 1)
    
    y_values = []

    for y_final in y_finals:
        t = step * (step - 1) // 2
        if (y_final + t) % step != 0: #or (y_final + t) == 0:
            continue
        y_vel = (y_final + t) // step
        y_values.append(y_vel)

    return y_values

def get_y_values_for_step_plus(x, step):
    curr_step = step
    step_to_values = {}
    for curr_step in range(step, step + 500): # figure out termination condition
        y_values = get_y_values_for_step(x, curr_step)
        step_to_values[curr_step] = y_values

    return step_to_values


all_solutions = []
for (x, x_sols) in x_to_sols.items():
    steps = x_sols[0]
    for step in steps:
        y_values = get_y_values_for_step(x, step)
        for y in y_values:
            all_solutions.append((x, y, step))

    steps_plus = x_sols[1]
    for step_plus in steps_plus:
        steps_to_values = get_y_values_for_step_plus(x, step_plus)
        for (s, y_vals) in steps_to_values.items():
            for y in y_vals:
                all_solutions.append((x, y, s))

max_y = -10000000000
max_sol = None

for sol in all_solutions:
    y_pos = 0
    vel_y = sol[1]
    steps = sol[2]
    for i in range(steps):
        y_pos += vel_y
        if y_pos > max_y:
            max_y = y_pos
            max_sol = sol
        vel_y -= 1

#part 1
print(max_y)
print(max_sol)

#part 2
all_velocities = set([(sol[0], sol[1]) for sol in all_solutions])
print(len(all_velocities))