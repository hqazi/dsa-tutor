# Nearest Charging Stations

**Topic:** Heaps · **Difficulty:** Medium

Each station is a point `[x, y]`; you are at `[0, 0]`. Return the `k` stations
closest to you (straight-line distance), **ordered from closest to farthest**.
Break distance ties by smaller `x`, then smaller `y`.

Try a heap so you do not have to sort every station when `k` is small.

## Examples

**Example 1**

```text
Input:  stations = [[1, 3], [-2, 2], [2, -2]], k = 2
Output: [[-2, 2], [2, -2]]
```

Distances squared: 10, 8, 8. The two at distance 8 tie, and `[-2, 2]` has the smaller `x`.

**Example 2**

```text
Input:  stations = [[3, 3], [5, -1], [-2, 4]], k = 1
Output: [[3, 3]]
```

## Constraints

- 1 <= k <= len(stations) <= 10^5
- -10^4 <= x, y <= 10^4
- stations may repeat

## Signature

```python
def k_closest(stations: list[list[int]], k: int) -> list[list[int]]:
```

## Your solution

Write it in `workspace/closest-stations/solution.py`, then run the tests:

```bash
python scripts/run_tests.py closest-stations
```
