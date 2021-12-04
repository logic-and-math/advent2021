import os
from pathlib import Path
from typing import Tuple, List
import functools
import itertools
import operator


input_p = Path(os.getcwd()) / 'input'
text = input_p.read_text()
lines = [l for l in text.splitlines() if l != '']

numbers = [int(i) for i in lines[0].split(',')]
numbers_to_pos = {n:i for (i,n) in enumerate(numbers)}

boards: List[List[List[int]]] = []
for (i, l) in enumerate(lines[1:]):
    if i % 5 == 0: # first row of the new board
        boards.append([])
    row = [int(i) for i in l.lstrip().replace('  ',' ').split(' ')]
    boards[-1].append(row)


def get_row_win(row: List[int]) -> int:
    positions = [numbers_to_pos[i] for i in row]
    return max(positions)


def get_board_win(board: List[List[int]]) -> int: #(when does the board win
    row_wins = [get_row_win(row) for row in board]
    board_transposed = map(list, zip(*board))
    col_wins = [get_row_win(col) for col in board_transposed]
    return min(row_wins + col_wins)


def calculate_board_score(board: List[List[int]]) -> int:
    win_position = get_board_win(board)
    numbers_set = set(numbers[:win_position + 1])
    score = sum([board[i][j] for i in range(5) for j in range(5) if board[i][j] not in numbers_set])
    return score * numbers[win_position]

winning_board = min(boards, key=lambda b: get_board_win(b))
last_winning_board = max(boards, key=lambda b: get_board_win(b))

print(calculate_board_score(winning_board))
print(calculate_board_score(last_winning_board))