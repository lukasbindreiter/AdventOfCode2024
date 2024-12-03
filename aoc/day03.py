import re
from typing import TypeAlias

import pytest
from aocd.models import Puzzle

Instructions: TypeAlias = list[str]


def parse(data: str) -> Instructions:
    return list(re.findall(r"mul\(\d+,\d+\)|don't\(\)|do\(\)", data))


def evaluate(multiplication: str) -> int:
    m = re.match(r"mul\((\d+),(\d+)\)", multiplication)
    if not m:
        raise ValueError(f"Invalid input: {multiplication}")
    return int(m.group(1)) * int(m.group(2))


def part1(instructions: Instructions) -> int:
    return sum(evaluate(instruction) for instruction in instructions if instruction.startswith("mul"))


def part2(instructions: Instructions) -> int:
    enabled = True
    total = 0
    for instruction in instructions:
        match instruction:
            case "do()":
                enabled = True
            case "don't()":
                enabled = False
            case _:
                if enabled:
                    total += evaluate(instruction)

    return total


@pytest.fixture
def puzzle_input() -> Instructions:
    return parse(Puzzle(2024, 3).input_data)


@pytest.fixture
def example_input() -> Instructions:
    return parse(
        """
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
    """.strip()
    )


@pytest.fixture
def example_input2() -> Instructions:
    return parse(
        """
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
    """.strip()
    )


def test_part1(puzzle_input: Instructions) -> None:
    assert part1(puzzle_input) == 171183089


def test_example_part1(example_input: Instructions) -> None:
    assert part1(example_input) == 161


def test_part2(puzzle_input: Instructions) -> None:
    assert part2(puzzle_input) == 63866497


def test_example_part2(example_input2: Instructions) -> None:
    assert part2(example_input2) == 48
