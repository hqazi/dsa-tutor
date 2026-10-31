# Count the Islands

**Topic:** Graphs · **Difficulty:** Medium

`grid` is a map where `1` is land and `0` is water. An **island** is a group of land
cells connected up, down, left or right (not diagonally). Return the number of
islands.

## Examples

**Example 1**

```text
Input:  grid = [[1, 1, 0, 0], [1, 0, 0, 1], [0, 0, 1, 1], [0, 0, 0, 0]]
Output: 2
```

**Example 2**

```text
Input:  grid = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
Output: 5
```

Diagonal neighbours do not connect, so there are 5 islands.

## Constraints

- 0 <= rows, cols <= 300
- grid[r][c] is 0 or 1

## Signature

```python
def count_islands(grid: list[list[int]]) -> int:
```

## Your solution

Write it in `workspace/count-islands/solution.py`, then run the tests:

```bash
python scripts/run_tests.py count-islands
```
