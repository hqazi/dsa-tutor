# First Lonely Letter

**Topic:** Hash maps & sets · **Difficulty:** Easy

Return the index of the first character in `s` that appears **exactly once** in the
whole string. If every character repeats, return `-1`.

## Examples

**Example 1**

```text
Input:  s = "swiss"
Output: 1
```

`s` appears three times; `w` appears once and is at index 1.

**Example 2**

```text
Input:  s = "aabb"
Output: -1
```

**Example 3**

```text
Input:  s = "level"
Output: 2
```

## Constraints

- 0 <= len(s) <= 10^5
- s contains only lowercase English letters

## Signature

```python
def first_unique(s: str) -> int:
```

## Your solution

Write it in `workspace/first-unique-char/solution.py`, then run the tests:

```bash
python scripts/run_tests.py first-unique-char
```
