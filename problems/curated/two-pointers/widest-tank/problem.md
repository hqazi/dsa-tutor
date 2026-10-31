# Widest Water Tank

**Topic:** Two pointers · **Difficulty:** Medium

You have a row of vertical walls; `walls[i]` is the height of the wall at position
`i`. Pick **two** walls; together with the ground they form a tank. The water it
holds is `(j - i) * min(walls[i], walls[j])`.

Return the most water any pair of walls can hold.

## Examples

**Example 1**

```text
Input:  walls = [1, 8, 6, 2, 5, 4, 8, 3, 7]
Output: 49
```

Walls at positions 1 and 8 (heights 8 and 7) are 7 apart: `7 * 7 = 49`.

**Example 2**

```text
Input:  walls = [2, 2]
Output: 2
```

## Constraints

- 2 <= len(walls) <= 10^5
- 0 <= walls[i] <= 10^4

## Signature

```python
def max_water(walls: list[int]) -> int:
```

## Your solution

Write it in `workspace/widest-tank/solution.py`, then run the tests:

```bash
python scripts/run_tests.py widest-tank
```
