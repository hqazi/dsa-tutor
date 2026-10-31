# Is There a Route?

**Topic:** Graphs · **Difficulty:** Easy

There are `n` towns numbered `0` to `n - 1`. Each road `[a, b]` connects towns `a`
and `b` in both directions. Return `True` if you can travel from `start` to `end`.

## Examples

**Example 1**

```text
Input:  n = 4, roads = [[0, 1], [1, 2], [3, 3]], start = 0, end = 2
Output: True
```

**Example 2**

```text
Input:  n = 4, roads = [[0, 1], [2, 3]], start = 0, end = 3
Output: False
```

## Constraints

- 1 <= n <= 10^5
- 0 <= len(roads) <= 10^5
- 0 <= a, b, start, end < n

## Signature

```python
def has_route(n: int, roads: list[list[int]], start: int, end: int) -> bool:
```

## Your solution

Write it in `workspace/has-route/solution.py`, then run the tests:

```bash
python scripts/run_tests.py has-route
```
