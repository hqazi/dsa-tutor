# Cheapest Climb

**Topic:** Dynamic programming · **Difficulty:** Easy

Step `i` of a staircase charges `cost[i]` when you land on it. You may start on
step 0 or step 1, and from any step you move up 1 or 2 steps. The top is just past
the last step.

Return the minimum total cost to reach the top.

## Examples

**Example 1**

```text
Input:  cost = [10, 15, 20]
Output: 15
```

Start on step 1 (15) and jump two steps to the top.

**Example 2**

```text
Input:  cost = [1, 100, 1, 1, 1, 100, 1, 1, 100, 1]
Output: 6
```

## Constraints

- 2 <= len(cost) <= 10^5
- 0 <= cost[i] <= 999

## Signature

```python
def min_climb_cost(cost: list[int]) -> int:
```

## Your solution

Write it in `workspace/min-climb-cost/solution.py`, then run the tests:

```bash
python scripts/run_tests.py min-climb-cost
```
