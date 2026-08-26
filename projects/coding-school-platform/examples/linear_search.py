import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from coding_school.curriculum import curriculum_catalog


def linear_search(numbers: list[int], target: int) -> int:
    """Return the target's first index, or -1 when it is absent."""
    for index, number in enumerate(numbers):
        if number == target:
            return index
    return -1


linear = next(item for item in curriculum_catalog() if item.id == "student-linear-search")
assert "function linearSearch" in linear.starter_code
assert linear_search([55, 9, 10, 1, 5, 3, 8, 7], 5) == 4
assert linear_search([55, 9, 10], 100) == -1
print("Linear Search Treasure Hunt examples passed")
