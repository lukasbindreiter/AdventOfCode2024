import re
from dataclasses import dataclass
from typing import Self, TypeAlias

import pytest
from aocd.models import Puzzle
from sympy import Eq, solve, symbols


@dataclass(frozen=True)
class Vec2:
    x: int
    y: int

    @classmethod
    def parse(cls, line: str) -> Self:
        x, y = map(int, re.findall(r"\d+", line))
        return cls(x, y)

    def __add__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.x + other.x, self.y + other.y)


@dataclass(frozen=True)
class ClawMachine:
    button_a: Vec2
    button_b: Vec2
    prize: Vec2

    @classmethod
    def parse(cls, machine_data: str) -> Self:
        a, b, prize = machine_data.strip().split("\n")
        return cls(Vec2.parse(a), Vec2.parse(b), Vec2.parse(prize))

    def shift_prize(self, offset: Vec2) -> "ClawMachine":
        return ClawMachine(self.button_a, self.button_b, self.prize + offset)


PuzzleInput: TypeAlias = list[ClawMachine]


def parse(data: str) -> PuzzleInput:
    return [ClawMachine.parse(machine_data) for machine_data in data.strip().split("\n\n")]


def solve_linear_equation(machine: ClawMachine) -> int:
    a, b = symbols("a b", integer=True)
    eq1 = Eq(machine.button_a.x * a + machine.button_b.x * b, machine.prize.x)
    eq2 = Eq(machine.button_a.y * a + machine.button_b.y * b, machine.prize.y)

    # Solve the system of equations for a and b
    solution = solve((eq1, eq2), (a, b))
    if not isinstance(solution, list):  # for one solution sympy returns a single solution instead of a list
        solution = [solution]

    if len(solution) == 0:
        return 0  # no solution

    return min(3 * int(sol[a]) + int(sol[b]) for sol in solution)


def part1(machines: PuzzleInput) -> int:
    return sum(solve_linear_equation(m) for m in machines)


def part2(machines: PuzzleInput) -> int:
    offset = 10000000000000
    return sum(solve_linear_equation(m.shift_prize(Vec2(offset, offset))) for m in machines)


@pytest.fixture
def puzzle_input() -> PuzzleInput:
    return parse(Puzzle(2024, 13).input_data)


@pytest.fixture
def example_input() -> PuzzleInput:
    return parse(
        """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
    """.strip()
    )


def test_part1(puzzle_input: PuzzleInput) -> None:
    assert part1(puzzle_input) == 29711


def test_example_part1(example_input: PuzzleInput) -> None:
    assert part1(example_input) == 480


def test_part2(puzzle_input: PuzzleInput) -> None:
    assert part2(puzzle_input) == 94955433618919


def test_example_part2(example_input: PuzzleInput) -> None:
    assert part2(example_input) == 875318608908
