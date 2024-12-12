from collections.abc import Iterator
from itertools import pairwise

import numpy as np
import pytest
from aocd.models import Puzzle
from scipy.ndimage import label
from shapely import LineString, MultiLineString, Polygon, box, union_all


def parse(data: str) -> np.ndarray:
    # convert letters to numbers using ord (their ascii value)
    return np.asarray([[ord(ch) for ch in l] for l in data.strip().splitlines()])


def iterate_regions(garden: np.ndarray) -> Iterator[Polygon]:
    """Iterate over all connected regions of the same value, yielding them as shapely.Polygons."""
    plants = np.unique(garden)
    for plant in plants:
        current_plant_mask = garden == plant  # boolean mask indicating all cells containing the current plant
        # label all connected regions:
        plant_regions, num = label(current_plant_mask)  # type: ignore[arg-type]
        for i in range(1, num + 1):
            region = plant_regions == i  # find all cells belonging to the current region
            # construct square boxes for every cell in the current region
            polys = [box(x, y, x + 1, y + 1) for y, x in zip(*np.where(region), strict=True)]
            # and then combine them into a single polygon
            region = union_all(polys)
            if not isinstance(region, Polygon):
                raise TypeError("Region is not a polygon")
            yield region


def count_sides(region: Polygon) -> int:
    """
    Count the number of sides of the given region. A region may have holes in it, which need to be counted as well.
    """
    perimeter = region.boundary
    if isinstance(perimeter, MultiLineString):  # a region with holes
        return sum(count_turns(line) for line in perimeter.geoms)  # count the main region and all holes

    return count_turns(perimeter)


def count_turns(line_string: LineString) -> int:
    """Count the number of turns in the given linestring."""
    coords = list(line_string.coords)
    turns = 0
    # initialize direction with the last direction we'll have, so we also account for the very first turn
    direction = (coords[-1][0] - coords[-2][0], coords[-1][1] - coords[-2][1])

    # the linestring is closed, with the first coordinate appearing again at the end, so this iterates all pairs:
    for a, b in pairwise(coords):
        current_dir = (b[0] - a[0], b[1] - a[1])
        # whenever we take a corner (the direction between successive points changes) -> new side
        if current_dir != direction:
            turns += 1
        direction = current_dir
    return turns


def part1(garden: np.ndarray) -> int:
    return sum(int(region.area) * int(region.length) for region in iterate_regions(garden))


def part2(garden: np.ndarray) -> int:
    return sum(int(region.area) * count_sides(region) for region in iterate_regions(garden))


@pytest.fixture
def puzzle_input() -> np.ndarray:
    return parse(Puzzle(2024, 12).input_data)


@pytest.fixture
def example_input() -> np.ndarray:
    return parse(
        """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
    """.strip()
    )


def test_part1(puzzle_input: np.ndarray) -> None:
    assert part1(puzzle_input) == 1421958


def test_example_part1(example_input: np.ndarray) -> None:
    assert part1(example_input) == 1930


def test_part2(puzzle_input: np.ndarray) -> None:
    assert part2(puzzle_input) == 885394


def test_example_part2(example_input: np.ndarray) -> None:
    assert part2(example_input) == 1206
