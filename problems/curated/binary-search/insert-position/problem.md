# Where Does It Go?

**Topic:** Binary search · **Difficulty:** Easy

`sorted_ids` is sorted in strictly increasing order. If `target` is in the list,
return its index. Otherwise return the index where it would have to be inserted to
keep the list sorted.

Use binary search: O(log n).

## Examples

**Example 1**

```text
Input:  sorted_ids = [1, 3, 5, 6], target = 5
Output: 2
```

**Example 2**

```text
Input:  sorted_ids = [1, 3, 5, 6], target = 2
Output: 1
```

2 belongs between 1 and 3, at index 1.

**Example 3**

```text
Input:  sorted_ids = [1, 3, 5, 6], target = 7
Output: 4
```

## Constraints

- 0 <= len(sorted_ids) <= 10^5
- values are distinct and increasing
- -10^9 <= target <= 10^9

## Signature

```python
def insert_position(sorted_ids: list[int], target: int) -> int:
```

## Your solution

Write it in `workspace/insert-position/solution.py`, then run the tests:

```bash
python scripts/run_tests.py insert-position
```
