# Most Vowels in a Window

**Topic:** Sliding window · **Difficulty:** Easy

Return the largest number of vowels (`a`, `e`, `i`, `o`, `u`) found in any
substring of `text` of length exactly `k`.

## Examples

**Example 1**

```text
Input:  text = "abciiidef", k = 3
Output: 3
```

`iii` holds 3 vowels.

**Example 2**

```text
Input:  text = "rhythm", k = 2
Output: 0
```

## Constraints

- 1 <= k <= len(text) <= 10^5
- text contains only lowercase English letters

## Signature

```python
def max_vowels(text: str, k: int) -> int:
```

## Your solution

Write it in `workspace/vowel-window/solution.py`, then run the tests:

```bash
python scripts/run_tests.py vowel-window
```
