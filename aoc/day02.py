import re
from typing import TypeAlias

import numpy as np
import pytest
from aocd.models import Puzzle

PuzzleInput: TypeAlias = list[np.ndarray]


def parse(data: str) -> PuzzleInput:
    return [np.asarray(list(map(int, re.findall(r"\d+", line)))) for line in data.strip().splitlines()]


def is_safe(report: np.ndarray) -> bool | np.bool:
    differences = np.diff(report)
    # check we have level increases or decreases of minimum 1 and maximum 3
    if np.abs(differences).max() > 3 or np.abs(differences).min() < 1:
        return False

    # check if the report is monotonic
    return np.all(differences >= 0) or np.all(differences <= 0)


def part1(reports: PuzzleInput) -> int:
    return sum(1 if is_safe(report) else 0 for report in reports)


def is_safe_with_removals(report: np.ndarray) -> bool:
    if is_safe(report):
        return True

    return any(is_safe(np.concat((report[:i], report[i + 1 :]))) for i in range(len(report)))


def part2(reports: PuzzleInput) -> int:
    return sum(1 if is_safe_with_removals(report) else 0 for report in reports)


@pytest.fixture
def puzzle_input() -> PuzzleInput:
    return parse(Puzzle(2024, 2).input_data)


@pytest.fixture
def example_input() -> PuzzleInput:
    return parse(
        """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
    """.strip()
    )


def test_part1(puzzle_input: PuzzleInput) -> None:
    assert part1(puzzle_input) == 379


def test_example_part1(example_input: PuzzleInput) -> None:
    assert part1(example_input) == 2


def test_part2(puzzle_input: PuzzleInput) -> None:
    assert part2(puzzle_input) == 430


def test_example_part2(example_input: PuzzleInput) -> None:
    assert part2(example_input) == 4
