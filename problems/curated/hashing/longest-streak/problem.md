# Longest Streak of Days

**Topic:** Hash maps & sets · **Difficulty:** Medium

A habit tracker stores the day numbers on which you exercised, in no particular
order and possibly with duplicates. A **streak** is a run of consecutive day
numbers (`d, d+1, d+2, ...`) that all appear in the list.

Return the length of the longest streak. Aim for O(n) time: sorting works but is
O(n log n).

## Examples

**Example 1**

```text
Input:  days = [100, 4, 200, 1, 3, 2]
Output: 4
```

Days 1, 2, 3, 4 form a streak of 4.

**Example 2**

```text
Input:  days = [5, 5, 6]
Output: 2
```

## Constraints

- 0 <= len(days) <= 10^5
- -10^9 <= days[i] <= 10^9

## Signature

```python
def longest_streak(days: list[int]) -> int:
```

## Your solution

Write it in `workspace/longest-streak/solution.py`, then run the tests:

```bash
python scripts/run_tests.py longest-streak
```
