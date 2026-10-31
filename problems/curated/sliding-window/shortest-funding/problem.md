# Shortest Funding Window

**Topic:** Sliding window · **Difficulty:** Medium

A crowdfunding page lists the **positive** amounts pledged each hour. Return the
length of the shortest run of consecutive hours whose pledges add up to at least
`goal`. If no run reaches the goal, return `0`.

## Examples

**Example 1**

```text
Input:  amounts = [2, 3, 1, 2, 4, 3], goal = 7
Output: 2
```

`4 + 3` reaches 7 in 2 hours.

**Example 2**

```text
Input:  amounts = [1, 1, 1], goal = 5
Output: 0
```

## Constraints

- 0 <= len(amounts) <= 10^5
- 1 <= amounts[i] <= 10^4
- 1 <= goal <= 10^9

## Signature

```python
def shortest_window(amounts: list[int], goal: int) -> int:
```

## Your solution

Write it in `workspace/shortest-funding/solution.py`, then run the tests:

```bash
python scripts/run_tests.py shortest-funding
```
