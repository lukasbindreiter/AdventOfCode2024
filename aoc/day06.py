from collections.abc import Iterator
from typing import TypeAlias

import numpy as np
import pytest
from aocd.models import Puzzle

PuzzleInput: TypeAlias = tuple[complex, complex, set[complex], set[complex]]

# using complex numbers to represent 2D-coordinates and directions
UP = -1 + 0j
RIGHT_TURN = -1j


def parse(data: str) -> PuzzleInput:
    grid = np.array([list(l) for l in data.strip().splitlines()])
    # pad our grid with a wall on all sides, so we can easily find out when we leave the grid
    grid = np.pad(grid, 1, constant_values="+")

    border = coords_of(grid, "+")  # a set of coords denoting the bounds of the grid
    obstructions = coords_of(grid, "#")  # a set of coords of all obstacles
    (start_pos,) = coords_of(grid, "^")  # exactly one starting position
    start_direction = UP
    return start_pos, start_direction, obstructions, border


def coords_of(grid: np.ndarray, ch: str) -> set[complex]:
    """Return a set of coordinates of all grid cells containing the given character"""
    return {(int(y) + 1j * int(x)) for y, x in zip(*np.where(grid == ch), strict=True)}


def simulate_guard_movement(
    start_pos: complex, start_direction: complex, obstructions: set[complex], border: set[complex]
) -> Iterator[tuple[complex, complex]]:
    """Generator that simulates the guards movement, yielding every (position, facing_direction) tuple along the way"""
    pos = start_pos
    facing = start_direction

    while pos not in border:  # stop as soon as we leave the grid
        yield pos, facing
        if (pos + facing) not in obstructions:  # the position in front of us is not obstructed
            pos += facing
        else:  # otherwise, turn
            facing *= RIGHT_TURN


def find_visited_positions(
    start_pos: complex, start_direction: complex, obstructions: set[complex], border: set[complex]
) -> set[complex]:
    """Return a set of all positions that the guard visits on its way"""
    visited = set()
    for pos, _ in simulate_guard_movement(start_pos, start_direction, obstructions, border):
        visited.add(pos)
    return visited


def part1(start_pos: complex, start_direction: complex, obstructions: set[complex], border: set[complex]) -> int:
    return len(find_visited_positions(start_pos, start_direction, obstructions, border))


def part2(start_pos: complex, start_direction: complex, obstructions: set[complex], border: set[complex]) -> int:
    # to avoid checking every position in the grid, we only check positions that are actually reachable on the path
    positions_to_check = find_visited_positions(start_pos, start_direction, obstructions, border) - {start_pos}
    possible_obstructions = set()

    for pos in positions_to_check:
        if contains_loop(start_pos, start_direction, obstructions | {pos}, border):
            possible_obstructions.add(pos)

    return len(possible_obstructions)


def contains_loop(
    start_pos: complex, start_direction: complex, obstructions: set[complex], border: set[complex]
) -> bool:
    """Checks if the guard movement with the given obstructions would result in a loop"""
    seen_states = set()

    for pos, facing in simulate_guard_movement(start_pos, start_direction, obstructions, border):
        if (pos, facing) in seen_states:  # we have been here before -> loop
            return True
        seen_states.add((pos, facing))

    return False


@pytest.fixture
def puzzle_input() -> PuzzleInput:
    return parse(Puzzle(2024, 6).input_data)


@pytest.fixture
def example_input() -> PuzzleInput:
    return parse(
        """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
    """.strip()
    )


def test_part1(puzzle_input: PuzzleInput) -> None:
    assert part1(*puzzle_input) == 4988


def test_example_part1(example_input: PuzzleInput) -> None:
    assert part1(*example_input) == 41


def test_part2(puzzle_input: PuzzleInput) -> None:
    assert part2(*puzzle_input) == 1697


def test_example_part2(example_input: PuzzleInput) -> None:
    assert part2(*example_input) == 6
