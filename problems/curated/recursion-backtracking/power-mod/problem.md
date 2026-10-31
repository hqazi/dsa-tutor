# Fast Power

**Topic:** Recursion & backtracking · **Difficulty:** Easy

Return `base` raised to the power `exp`, modulo `mod`.

`exp` can be as large as `10^18`, so multiplying `exp` times is far too slow. Use
recursion: `b^e` can be built from `b^(e // 2)`. Do not use Python's three-argument
`pow`.

## Examples

**Example 1**

```text
Input:  base = 2, exp = 10, mod = 1000
Output: 24
```

2^10 = 1024, and 1024 mod 1000 = 24.

**Example 2**

```text
Input:  base = 3, exp = 0, mod = 7
Output: 1
```

## Constraints

- 0 <= base <= 10^9
- 0 <= exp <= 10^18
- 1 <= mod <= 10^9

## Signature

```python
def power_mod(base: int, exp: int, mod: int) -> int:
```

## Your solution

Write it in `workspace/power-mod/solution.py`, then run the tests:

```bash
python scripts/run_tests.py power-mod
```
