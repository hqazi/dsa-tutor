# Same Letters, Same Shelf

**Topic:** Hash maps & sets · **Difficulty:** Medium

A librarian shelves words together when they use **exactly the same letters the
same number of times** (they are anagrams of each other).

Given `words`, return the groups. Every word appears in exactly one group, and
duplicate words both appear in their group.

## Examples

**Example 1**

```text
Input:  words = ["listen", "stone", "silent", "notes", "cat"]
Output: [["listen", "silent"], ["stone", "notes"], ["cat"]]
```

**Example 2**

```text
Input:  words = ["a"]
Output: [["a"]]
```

## Constraints

- 0 <= len(words) <= 10^4
- 0 <= len(words[i]) <= 50
- lowercase English letters only

## Signature

```python
def group_words(words: list[str]) -> list[list[str]]:
```

The order of the returned items does not matter.

## Your solution

Write it in `workspace/group-by-letters/solution.py`, then run the tests:

```bash
python scripts/run_tests.py group-by-letters
```
