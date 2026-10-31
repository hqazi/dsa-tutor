# Cheapest Way to Join Ropes

**Topic:** Heaps · **Difficulty:** Easy

You have ropes of the given lengths and want a single rope. Joining two ropes of
lengths `a` and `b` costs `a + b` and produces a rope of length `a + b`.

Return the minimum total cost to join all the ropes into one. With zero or one
rope the cost is 0.

## Examples

**Example 1**

```text
Input:  ropes = [4, 3, 2, 6]
Output: 29
```

Join 2 + 3 (cost 5), then 4 + 5 (cost 9), then 6 + 9 (cost 15): 29 in total.

**Example 2**

```text
Input:  ropes = [8]
Output: 0
```

## Constraints

- 0 <= len(ropes) <= 10^5
- 1 <= ropes[i] <= 10^4

## Signature

```python
def min_join_cost(ropes: list[int]) -> int:
```

## Your solution

Write it in `workspace/rope-joining/solution.py`, then run the tests:

```bash
python scripts/run_tests.py rope-joining
```
