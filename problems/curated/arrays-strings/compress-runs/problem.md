# Compress the Sensor Log

**Topic:** Arrays & strings · **Difficulty:** Easy

A sensor writes its readings as a string of lowercase letters, and long stretches
of the same letter are common. To save space, replace every run of a repeated
letter by the letter followed by the length of the run. A run of length 1 is
written as just the letter.

Return the compressed string.

## Examples

**Example 1**

```text
Input:  log = "aaabccdddd"
Output: "a3bc2d4"
```

Runs: `aaa`, `b`, `cc`, `dddd` become `a3`, `b`, `c2`, `d4`.

**Example 2**

```text
Input:  log = "xyz"
Output: "xyz"
```

**Example 3**

```text
Input:  log = "zzzzzzzzzzzz"
Output: "z12"
```

A run of twelve is written with two digits: `z12`.

## Constraints

- 0 <= len(log) <= 10^5
- log contains only lowercase English letters

## Signature

```python
def compress_runs(log: str) -> str:
```

## Your solution

Write it in `workspace/compress-runs/solution.py`, then run the tests:

```bash
python scripts/run_tests.py compress-runs
```
