from collections import defaultdict
from functools import cmp_to_key
from typing import TypeAlias

import pytest
from aocd.models import Puzzle


class PageOrdering:
    def __init__(self, rules: dict[int, set[int]]) -> None:
        """Creates a page ordering helper, based from a set of rules in the form { after: {before_a, before_b, ...} }"""
        self.rules = rules

    def compare(self, page_a: int, page_b: int) -> int:
        """Compare two pages, return -1 if page_a < page_b, 1 if page_a > page_b, 0 if equal"""
        if page_a == page_b:
            return 0

        before_b = self.rules.get(page_b, set())
        return -1 if page_a in before_b else 1


Updates: TypeAlias = list[list[int]]
PuzzleInput: TypeAlias = tuple[Updates, PageOrdering]


def parse(data: str) -> PuzzleInput:
    orderings, updates = data.strip().split("\n\n")

    rules = defaultdict(set)
    for ordering in orderings.splitlines():
        before, after = map(int, ordering.split("|"))
        rules[after].add(before)
    page_order = PageOrdering(dict(rules))

    updates = [list(map(int, line.split(","))) for line in updates.splitlines()]
    return updates, page_order


def part1(updates: Updates, ordering_rules: PageOrdering) -> int:
    middle_page_sum = 0

    for update in updates:
        if update == sorted(update, key=cmp_to_key(ordering_rules.compare)):
            middle_page_sum += update[len(update) // 2]

    return middle_page_sum


def part2(updates: Updates, ordering_rules: PageOrdering) -> int:
    middle_page_sum = 0

    for update in updates:
        right_order = sorted(update, key=cmp_to_key(ordering_rules.compare))
        if update != right_order:
            middle_page_sum += right_order[len(right_order) // 2]

    return middle_page_sum


@pytest.fixture
def puzzle_input() -> PuzzleInput:
    return parse(Puzzle(2024, 5).input_data)


@pytest.fixture
def example_input() -> PuzzleInput:
    return parse(
        """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
    """.strip()
    )


def test_part1(puzzle_input: PuzzleInput) -> None:
    assert part1(*puzzle_input) == 5374


def test_example_part1(example_input: PuzzleInput) -> None:
    assert part1(*example_input) == 143


def test_part2(puzzle_input: PuzzleInput) -> None:
    assert part2(*puzzle_input) == 4260


def test_example_part2(example_input: PuzzleInput) -> None:
    assert part2(*example_input) == 123
