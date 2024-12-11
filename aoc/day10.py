from typing import TypeAlias

import networkx as nx
import numpy as np
import pytest
from aocd.models import Puzzle

PuzzleInput: TypeAlias = tuple[np.ndarray, list[tuple[int, int]], list[tuple[int, int]]]


def parse(data: str) -> PuzzleInput:
    topo = np.asarray([list(map(int, line)) for line in data.split("\n")])
    trailheads = list(zip(*np.where(topo == 0), strict=True))
    end_positions = list(zip(*np.where(topo == 9), strict=True))
    return topo, trailheads, end_positions


def graph_from_topo(topo: np.ndarray) -> nx.Graph:
    graph = nx.grid_2d_graph(*topo.shape).to_directed()
    edges = [(src, dst) for src, dst in graph.edges if (topo[src] + 1) == topo[dst]]
    return graph.edge_subgraph(edges)


def part1(topo: np.ndarray, trailheads: list[tuple[int, int]], end_positions: list[tuple[int, int]]) -> int:
    graph = graph_from_topo(topo)

    score = 0
    for end in end_positions:
        shortest_path_from_all_positions = nx.single_target_shortest_path(graph, end)
        for start in shortest_path_from_all_positions:
            if start in trailheads:
                score += 1

    return score


def part2(topo: np.ndarray, trailheads: list[tuple[int, int]], end_positions: list[tuple[int, int]]) -> int:
    graph = graph_from_topo(topo)

    score = 0
    for start in trailheads:
        for end in end_positions:
            score += len(list(nx.all_simple_paths(graph, start, end)))

    return score


@pytest.fixture
def puzzle_input() -> PuzzleInput:
    return parse(Puzzle(2024, 10).input_data)


@pytest.fixture
def example_input() -> PuzzleInput:
    return parse(
        """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
    """.strip()
    )


def test_part1(puzzle_input: PuzzleInput) -> None:
    assert part1(*puzzle_input) == 548


def test_example_part1(example_input: PuzzleInput) -> None:
    assert part1(*example_input) == 36


def test_part2(puzzle_input: PuzzleInput) -> None:
    assert part2(*puzzle_input) == 1252


def test_example_part2(example_input: PuzzleInput) -> None:
    assert part2(*example_input) == 81
