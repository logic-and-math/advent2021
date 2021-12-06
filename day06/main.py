import os
from pathlib import Path


input_p = Path(os.getcwd()) / 'input'
text = input_p.read_text()
numbers = [int(i) for i in text.split(",")]

def calc(start_day, counter, n_days) -> int:
    n_new_fishes = 1 + int( ( n_days - start_day - counter) / 6) #possible 
    new_fishes = [(start_day + counter + 1, 8, n_days)] + [(start_day + counter + i * 7 + 1, 8, n_days) for i in range(1, n_new_fishes)]
    new_fishes = [f for f in new_fishes if f[0] <= n_days] # real
    return len(new_fishes) + sum([calc(fish[0], fish[1], fish[2]) for fish in new_fishes])


print(sum(calc(0, n, 80) for n in numbers) + len(numbers))
