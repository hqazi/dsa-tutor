# Quiet Night Market

**Topic:** Dynamic programming · **Difficulty:** Medium

A market has a row of stalls; `stalls[i]` is how much stall `i` would pay you for a
delivery. You cannot deliver to **two neighbouring stalls** on the same night.

Return the most you can earn in one night.

## Examples

**Example 1**

```text
Input:  stalls = [2, 7, 9, 3, 1]
Output: 12
```

Stalls 0, 2 and 4: `2 + 9 + 1 = 12`.

**Example 2**

```text
Input:  stalls = [5, 1, 1, 5]
Output: 10
```

The two ends: `5 + 5 = 10`.

## Constraints

- 0 <= len(stalls) <= 10^5
- 0 <= stalls[i] <= 10^4

## Signature

```python
def max_haul(stalls: list[int]) -> int:
```

## Your solution

Write it in `workspace/max-haul/solution.py`, then run the tests:

```bash
python scripts/run_tests.py max-haul
```
