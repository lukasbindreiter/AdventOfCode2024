import re
from collections import Counter
from typing import TypeAlias

import numpy as np
import pytest
from aocd.models import Puzzle

PuzzleInput: TypeAlias = tuple[np.ndarray, np.ndarray]


def parse(data: str) -> PuzzleInput:
    nums = np.array([list(map(int, re.findall(r"\d+", line))) for line in data.strip().splitlines()])
    return nums[:, 0], nums[:, 1]


def part1(a: np.ndarray, b: np.ndarray) -> int:
    a.sort()
    b.sort()
    return np.abs(a - b).sum()


def part2(a: np.ndarray, b: np.ndarray) -> int:
    occurrences = Counter(b)
    return sum(val * occurrences[val] for val in a)


@pytest.fixture
def puzzle_input() -> PuzzleInput:
    return parse(Puzzle(2024, 1).input_data)


@pytest.fixture
def example_input() -> PuzzleInput:
    return parse(
        """
3   4
4   3
2   5
1   3
3   9
3   3
    """.strip()
    )


def test_part1(puzzle_input: PuzzleInput) -> None:
    assert part1(*puzzle_input) == 1941353


def test_example_part1(example_input: PuzzleInput) -> None:
    assert part1(*example_input) == 11


def test_part2(puzzle_input: PuzzleInput) -> None:
    assert part2(*puzzle_input) == 22539317


def test_example_part2(example_input: PuzzleInput) -> None:
    assert part2(*example_input) == 31
