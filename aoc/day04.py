from itertools import product
from typing import TypeAlias

import numpy as np
import pytest
from aocd.models import Puzzle

PuzzleInput: TypeAlias = np.ndarray


def parse(data: str) -> PuzzleInput:
    return np.array([list(l) for l in data.strip().splitlines()])


def is_match(word: str, target: str) -> bool:
    """Check if the given word matches the target string in forward or reverse order"""
    return word == target or word[::-1] == target


def part1(word_search: PuzzleInput) -> int:
    target = "XMAS"
    height, width = word_search.shape
    count = 0
    for y, x in product(range(height), range(width)):
        if x <= (width - len(target)):  # we have enough space to the right to check horizontally
            horizontal = "".join(word_search[y, x : x + len(target)])
            if is_match(horizontal, target):
                count += 1
        if y <= (height - len(target)):  # we have enough space to the bottom to check vertically
            vertical = "".join(word_search[y : y + len(target), x])
            if is_match(vertical, target):
                count += 1

            if x <= (width - len(target)):  # check the diagonal from the top left to the bottom right
                diagonal = "".join(word_search[y + i, x + i] for i in range(len(target)))
                if is_match(diagonal, target):
                    count += 1
            if x >= len(target) - 1:  # check the diagonal from the top right to the bottom left
                diagonal = "".join(word_search[y + i, x - i] for i in range(len(target)))
                if is_match(diagonal, target):
                    count += 1

    return count


def part2(word_search: PuzzleInput) -> int:
    target = "MAS"
    height, width = word_search.shape
    count = 0
    for y, x in product(range(height), range(width)):
        if x <= (width - len(target)) and y <= (height - len(target)):
            box = word_search[y : y + len(target), x : x + len(target)]  # the square box potentially containing the X
            diagonal_left_right = "".join(box.diagonal())
            diagonal_right_left = "".join(np.fliplr(box).diagonal())
            if is_match(diagonal_left_right, target) and is_match(diagonal_right_left, target):
                count += 1
    return count


@pytest.fixture
def puzzle_input() -> PuzzleInput:
    return parse(Puzzle(2024, 4).input_data)


@pytest.fixture
def example_input() -> PuzzleInput:
    return parse(
        """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
    """.strip()
    )


def test_part1(puzzle_input: PuzzleInput) -> None:
    assert part1(puzzle_input) == 2603


def test_example_part1(example_input: PuzzleInput) -> None:
    assert part1(example_input) == 18


def test_part2(puzzle_input: PuzzleInput) -> None:
    assert part2(puzzle_input) == 1965


def test_example_part2(example_input: PuzzleInput) -> None:
    assert part2(example_input) == 9
