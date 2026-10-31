# Every Possible Team

**Topic:** Recursion & backtracking · **Difficulty:** Easy

Given a list of **distinct** player ids, return every possible team, that is every
subset of `players`, including the empty team and the full team.

Each team should list its players in the order they appear in `players`. The
order of the teams does not matter.

## Examples

**Example 1**

```text
Input:  players = [1, 2, 3]
Output: [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]
```

**Example 2**

```text
Input:  players = []
Output: [[]]
```

## Constraints

- 0 <= len(players) <= 12
- player ids are distinct

## Signature

```python
def subsets(players: list[int]) -> list[list[int]]:
```

The order of the returned items does not matter.

## Your solution

Write it in `workspace/all-subsets/solution.py`, then run the tests:

```bash
python scripts/run_tests.py all-subsets
```
