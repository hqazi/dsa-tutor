# Back-to-Back Meetings

**Topic:** Sorting & intervals · **Difficulty:** Easy

Each meeting is `[start, end]` and occupies the time from `start` up to but **not
including** `end`, so a meeting ending at 10 and one starting at 10 do not clash.

Return `True` if one person can attend every meeting (no two overlap).

## Examples

**Example 1**

```text
Input:  meetings = [[9, 10], [13, 15], [10, 12]]
Output: True
```

**Example 2**

```text
Input:  meetings = [[1, 5], [4, 6]]
Output: False
```

The first meeting runs until 5, but the second starts at 4.

## Constraints

- 0 <= len(meetings) <= 10^5
- 0 <= start < end <= 10^9

## Signature

```python
def can_attend_all(meetings: list[list[int]]) -> bool:
```

## Your solution

Write it in `workspace/can-attend-all/solution.py`, then run the tests:

```bash
python scripts/run_tests.py can-attend-all
```
