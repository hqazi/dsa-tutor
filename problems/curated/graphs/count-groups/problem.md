# Friend Groups

**Topic:** Graphs · **Difficulty:** Easy

`n` people are numbered `0` to `n - 1`. Each friendship `[a, b]` links two people.
Friends of friends belong to the same group. Return the number of groups (someone
with no friends forms a group alone).

## Examples

**Example 1**

```text
Input:  n = 5, friendships = [[0, 1], [1, 2], [3, 4]]
Output: 2
```

**Example 2**

```text
Input:  n = 3, friendships = []
Output: 3
```

## Constraints

- 1 <= n <= 10^5
- 0 <= len(friendships) <= 10^5
- 0 <= a, b < n

## Signature

```python
def count_groups(n: int, friendships: list[list[int]]) -> int:
```

## Your solution

Write it in `workspace/count-groups/solution.py`, then run the tests:

```bash
python scripts/run_tests.py count-groups
```
