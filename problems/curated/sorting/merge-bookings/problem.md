# Merge Room Bookings

**Topic:** Sorting & intervals · **Difficulty:** Medium

Each booking is `[start, end]` with `start <= end`, both ends included. Merge every
set of bookings that **overlap or touch** (share at least one point, so `[1, 3]`
and `[3, 5]` merge into `[1, 5]`).

Return the merged bookings sorted by start time.

## Examples

**Example 1**

```text
Input:  bookings = [[1, 3], [8, 10], [2, 6], [15, 18]]
Output: [[1, 6], [8, 10], [15, 18]]
```

`[1, 3]` and `[2, 6]` overlap and become `[1, 6]`.

**Example 2**

```text
Input:  bookings = [[1, 4], [4, 5]]
Output: [[1, 5]]
```

## Constraints

- 0 <= len(bookings) <= 10^5
- 0 <= start <= end <= 10^9

## Signature

```python
def merge_bookings(bookings: list[list[int]]) -> list[list[int]]:
```

## Your solution

Write it in `workspace/merge-bookings/solution.py`, then run the tests:

```bash
python scripts/run_tests.py merge-bookings
```
