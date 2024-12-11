from functools import cache
from typing import TypeAlias

import pytest
from aocd.models import Puzzle

PuzzleInput: TypeAlias = list[int]


def parse(data: str) -> PuzzleInput:
    return list(map(int, data.strip().split(" ")))


@cache
def expands_to(stone: int, remaining_blinks: int) -> int:
    """
    Calculate how many stones the given stone will expand to with the given number of remaining blinks

    Designing the function like this allows us to use dynamic programming by caching previously computed results,
    since the stones always follow repeatable patterns

    Returns:
        Number of stones this stone will expand to in the remaining number of blinks
    """
    if remaining_blinks <= 1:
        return 2 if len(str(stone)) % 2 == 0 else 1

    if stone == 0:
        return expands_to(1, remaining_blinks - 1)

    as_str = str(stone)
    if len(as_str) % 2 == 0:
        left_stone = int(as_str[: len(as_str) // 2])
        right_stone = int(as_str[len(as_str) // 2 :])
        return expands_to(left_stone, remaining_blinks - 1) + expands_to(right_stone, remaining_blinks - 1)

    return expands_to(stone * 2024, remaining_blinks - 1)


def part1(stones: PuzzleInput, blinks: int = 25) -> int:
    return sum(expands_to(stone, blinks) for stone in stones)


def part2(stones: PuzzleInput) -> int:
    return part1(stones, 75)


@pytest.fixture
def puzzle_input() -> PuzzleInput:
    return parse(Puzzle(2024, 11).input_data)


@pytest.fixture
def example_input() -> PuzzleInput:
    return parse(
        """
125 17
    """.strip()
    )


def test_part1(puzzle_input: PuzzleInput) -> None:
    assert part1(puzzle_input) == 202019


def test_example_part1(example_input: PuzzleInput) -> None:
    assert part1(example_input) == 55312


def test_part2(puzzle_input: PuzzleInput) -> None:
    assert part2(puzzle_input) == 239321955280205


def test_example_part2(example_input: PuzzleInput) -> None:
    assert part2(example_input) == 65601038650482
