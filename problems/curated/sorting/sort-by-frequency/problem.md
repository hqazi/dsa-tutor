# Most Common First

**Topic:** Sorting & intervals · **Difficulty:** Easy

Sort `nums` so that values that occur **more often come first**. Values with the
same count are ordered by **value, smallest first**. Equal values stay together.

## Examples

**Example 1**

```text
Input:  nums = [4, 6, 4, 2, 6, 6]
Output: [6, 6, 6, 4, 4, 2]
```

6 appears 3 times, 4 twice, 2 once.

**Example 2**

```text
Input:  nums = [3, 1, 2, 1, 3]
Output: [1, 1, 3, 3, 2]
```

1 and 3 both appear twice, so the smaller value (1) goes first.

## Constraints

- 0 <= len(nums) <= 10^5
- -10^4 <= nums[i] <= 10^4

## Signature

```python
def frequency_sort(nums: list[int]) -> list[int]:
```

## Your solution

Write it in `workspace/sort-by-frequency/solution.py`, then run the tests:

```bash
python scripts/run_tests.py sort-by-frequency
```
