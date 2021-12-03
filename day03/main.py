import os
from pathlib import Path
from typing import Tuple, List
import functools
import itertools
import operator

def str_to_list_int(input: str) -> List[int]:
    return [0 if c == '0' else 1 for c in input]

def binary_to_decimal(binary: List[int]) -> int:
    decimal = 0
    for (i, d) in enumerate(reversed(binary)):
        decimal += (2**i)*d
    return decimal


def get_most_common_bits(numbers: List[int], n_bits: int) -> List[int]:
    
    collect = lambda a,b: [x + y for (x,y) in zip(a,b)]
    sum_by_digit = functools.reduce(collect, numbers, [0] * n_bits)

    n_numbers_half = len(numbers) * 1.0 / 2
    return [1 if d * 1.0 >= n_numbers_half else 0 for d in sum_by_digit]


def get_second_measurement(numbers: List[int], n_bits: int, most_common: bool = True) -> List[int]:
    
    filtered_numbers = numbers
    for i in range(n_bits):
        most_common_bits = get_most_common_bits(filtered_numbers, n_bits)
        value_to_compare = most_common_bits[i] if most_common else int(not most_common_bits[i])
        filtered_numbers = [n for n in filtered_numbers if n[i] == value_to_compare]
        if len(filtered_numbers) == 1:
            break
        
    return filtered_numbers[0]


input_p = Path(os.getcwd()) / 'input'
text = input_p.read_text()
numbers: List[List[int]] = [str_to_list_int(l) for l in text.splitlines()]
n_bits = len(numbers[0])

most_common_bits = get_most_common_bits(numbers, n_bits)
gamma_rate = [d for d in most_common_bits]
epsilon = [int(not d)  for d in most_common_bits]
print(binary_to_decimal(gamma_rate) * binary_to_decimal(epsilon))


oxygen_rate = get_second_measurement(numbers, n_bits, True)
co2_rate = get_second_measurement(numbers, n_bits, False)
print(binary_to_decimal(oxygen_rate) * binary_to_decimal(co2_rate))