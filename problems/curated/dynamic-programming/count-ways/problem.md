# Ways Up the Stairs

**Topic:** Dynamic programming · **Difficulty:** Easy

You climb a staircase of `steps` steps, taking either **1 or 2** steps at a time.
Return the number of different ways to reach the top. There is exactly one way to
climb zero steps.

## Examples

**Example 1**

```text
Input:  steps = 3
Output: 3
```

1+1+1, 1+2 and 2+1.

**Example 2**

```text
Input:  steps = 1
Output: 1
```

## Constraints

- 0 <= steps <= 90

## Signature

```python
def count_ways(steps: int) -> int:
```

## Your solution

Write it in `workspace/count-ways/solution.py`, then run the tests:

```bash
python scripts/run_tests.py count-ways
```
