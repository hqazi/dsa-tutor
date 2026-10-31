# Two Receipts

**Topic:** Hash maps & sets · **Difficulty:** Easy

You are reconciling expenses. Given a list of receipt `amounts` and a `target`,
find two **different positions** `i < j` with `amounts[i] + amounts[j] == target`
and return `[i, j]`.

If several pairs work, return the one with the **smallest `j`**; if there is still
a tie, the one with the smallest `i`. If no pair works, return `[]`.

## Examples

**Example 1**

```text
Input:  amounts = [5, 9, 3, 6, 8], target = 11
Output: [0, 3]
```

At `j = 3`, `5 + 6 = 11`. The pair `3 + 8` also works, but its `j` is larger.

**Example 2**

```text
Input:  amounts = [4, 4, 4], target = 8
Output: [0, 1]
```

The smallest `j` is 1, and the only `i` before it is 0.

**Example 3**

```text
Input:  amounts = [1, 2], target = 10
Output: []
```

## Constraints

- 0 <= len(amounts) <= 10^5
- -10^9 <= amounts[i], target <= 10^9

## Signature

```python
def find_pair(amounts: list[int], target: int) -> list[int]:
```

## Your solution

Write it in `workspace/pair-with-target/solution.py`, then run the tests:

```bash
python scripts/run_tests.py pair-with-target
```
