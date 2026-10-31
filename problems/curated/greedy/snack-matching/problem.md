# Snacks for the Team

**Topic:** Greedy · **Difficulty:** Easy

Each person has an appetite, and each snack has a size. A person is content if they
get **one** snack whose size is at least their appetite. Each snack goes to at most
one person.

Return the largest number of people you can make content.

## Examples

**Example 1**

```text
Input:  appetites = [1, 2, 3], snacks = [1, 1]
Output: 1
```

Both snacks have size 1, so only the person with appetite 1 can be content.

**Example 2**

```text
Input:  appetites = [1, 2], snacks = [1, 2, 3]
Output: 2
```

## Constraints

- 0 <= len(appetites), len(snacks) <= 10^5
- 1 <= values <= 10^9

## Signature

```python
def max_content(appetites: list[int], snacks: list[int]) -> int:
```

## Your solution

Write it in `workspace/snack-matching/solution.py`, then run the tests:

```bash
python scripts/run_tests.py snack-matching
```
