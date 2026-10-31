# Days Until Warmer

**Topic:** Stacks · **Difficulty:** Medium

`temps[i]` is the temperature on day `i`. For each day, return how many days you
must wait for a **strictly warmer** day. If no warmer day comes, use `0`.

## Examples

**Example 1**

```text
Input:  temps = [13, 14, 15, 11, 9, 12, 16, 13]
Output: [1, 1, 4, 2, 1, 1, 0, 0]
```

Day 3 (11°) waits until day 5 (12°): 2 days.

**Example 2**

```text
Input:  temps = [30, 30, 30]
Output: [0, 0, 0]
```

## Constraints

- 0 <= len(temps) <= 10^5
- -50 <= temps[i] <= 60

## Signature

```python
def wait_days(temps: list[int]) -> list[int]:
```

## Your solution

Write it in `workspace/days-until-warmer/solution.py`, then run the tests:

```bash
python scripts/run_tests.py days-until-warmer
```
