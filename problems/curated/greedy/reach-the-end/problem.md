# Stepping Stones

**Topic:** Greedy · **Difficulty:** Medium

You stand on stone `0`. From stone `i` you may jump forward **up to** `jumps[i]`
stones. Return `True` if you can reach the last stone.

## Examples

**Example 1**

```text
Input:  jumps = [2, 3, 1, 1, 4]
Output: True
```

**Example 2**

```text
Input:  jumps = [3, 2, 1, 0, 4]
Output: False
```

Every route lands on stone 3, whose jump length is 0.

## Constraints

- 1 <= len(jumps) <= 10^5
- 0 <= jumps[i] <= 10^5

## Signature

```python
def can_reach_end(jumps: list[int]) -> bool:
```

## Your solution

Write it in `workspace/reach-the-end/solution.py`, then run the tests:

```bash
python scripts/run_tests.py reach-the-end
```
