# Square Root, Rounded Down

**Topic:** Binary search · **Difficulty:** Easy

Return the largest integer `r` with `r * r <= x`.

Do not use `math.sqrt`, `math.isqrt`, `** 0.5` or similar helpers: binary search
for `r`. `x` can be as large as `10^18`, so counting up from 0 is far too slow.

## Examples

**Example 1**

```text
Input:  x = 8
Output: 2
```

2 × 2 = 4 ≤ 8 but 3 × 3 = 9 > 8.

**Example 2**

```text
Input:  x = 49
Output: 7
```

## Constraints

- 0 <= x <= 10^18

## Signature

```python
def floor_sqrt(x: int) -> int:
```

## Your solution

Write it in `workspace/floor-sqrt/solution.py`, then run the tests:

```bash
python scripts/run_tests.py floor-sqrt
```
