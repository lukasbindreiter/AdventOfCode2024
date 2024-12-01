from typing import TypeAlias

import numpy as np
import pytest
from aocd.models import Puzzle

PuzzleInput: TypeAlias = np.ndarray


def parse(data: str) -> PuzzleInput:
    return np.array([list(l) for l in data.strip().splitlines()])


def part1(data: PuzzleInput) -> int:
    _ = data
    return 1


def part2(data: PuzzleInput) -> int:
    _ = data
    return 2


@pytest.fixture
def puzzle_input() -> PuzzleInput:
    return parse(Puzzle(2024, 0).input_data)


@pytest.fixture
def example_input() -> PuzzleInput:
    return parse(
        """
    """.strip()
    )


def test_part1(puzzle_input: PuzzleInput) -> None:
    assert part1(puzzle_input) == 0


def test_example_part1(example_input: PuzzleInput) -> None:
    assert part1(example_input) == 0


def test_part2(puzzle_input: PuzzleInput) -> None:
    assert part2(puzzle_input) == 0


def test_example_part2(example_input: PuzzleInput) -> None:
    assert part2(example_input) == 0
