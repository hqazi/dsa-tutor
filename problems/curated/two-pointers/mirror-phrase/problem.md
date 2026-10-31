# Mirror Phrase

**Topic:** Two pointers · **Difficulty:** Easy

A phrase is a **mirror phrase** if it reads the same forwards and backwards after
you drop everything except letters and digits and ignore upper/lower case.

Return `True` if `text` is a mirror phrase. Try to use O(1) extra space.

## Examples

**Example 1**

```text
Input:  text = "Was it a car, or a cat I saw?"
Output: True
```

**Example 2**

```text
Input:  text = "race a car"
Output: False
```

Keeping letters gives `raceacar`, which is not the same backwards.

## Constraints

- 0 <= len(text) <= 2 · 10^5
- text contains printable ASCII characters

## Signature

```python
def is_mirror(text: str) -> bool:
```

## Your solution

Write it in `workspace/mirror-phrase/solution.py`, then run the tests:

```bash
python scripts/run_tests.py mirror-phrase
```
