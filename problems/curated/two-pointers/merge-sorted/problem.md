# Merge Two Leaderboards

**Topic:** Two pointers · **Difficulty:** Easy

Two leaderboards list scores in **non-decreasing** order. Merge them into a single
list in non-decreasing order, keeping every score (including duplicates).

Both lists are already sorted, so you can do this in O(n + m) without sorting.

## Examples

**Example 1**

```text
Input:  a = [1, 4, 9], b = [2, 3, 10]
Output: [1, 2, 3, 4, 9, 10]
```

**Example 2**

```text
Input:  a = [], b = [5, 5]
Output: [5, 5]
```

## Constraints

- 0 <= len(a), len(b) <= 10^5
- -10^9 <= values <= 10^9
- a and b are sorted

## Signature

```python
def merge_sorted(a: list[int], b: list[int]) -> list[int]:
```

## Your solution

Write it in `workspace/merge-sorted/solution.py`, then run the tests:

```bash
python scripts/run_tests.py merge-sorted
```
