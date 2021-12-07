import os
from pathlib import Path
import itertools

input_p = Path(os.getcwd()) / 'input'
text = input_p.read_text()
numbers = [int(i) for i in text.split(",")]
possible_positions = range(min(numbers), max(numbers) + 1)

def calculate_cost(position, fuel_function):
    return sum([fuel_function(n, position) for n in numbers if n != position])        

fuel_function_1 = lambda n,p: abs(n - p)

def fuel_function_2(n,p):
    x = abs(n - p)
    return int( x * (x + 1) / 2 )

min_cost_1 = min([calculate_cost(p, fuel_function_1) for p in possible_positions])
print(min_cost_1)

min_cost_2 = min([calculate_cost(p, fuel_function_2) for p in possible_positions])
print(min_cost_2)