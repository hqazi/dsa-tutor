# Everyone Else's Product

**Topic:** Arrays & strings · **Difficulty:** Medium

Given a list `nums`, return a list `out` of the same length where `out[i]` is the
product of every element of `nums` **except** `nums[i]`.

Do it in O(n) time and **without using division** (zeros in the input would break
division anyway).

## Examples

**Example 1**

```text
Input:  nums = [1, 2, 3, 4]
Output: [24, 12, 8, 6]
```

For index 0: 2 × 3 × 4 = 24; for index 1: 1 × 3 × 4 = 12; and so on.

**Example 2**

```text
Input:  nums = [3, 0, 5]
Output: [0, 15, 0]
```

## Constraints

- 2 <= len(nums) <= 10^5
- -30 <= nums[i] <= 30
- every product fits in a 64-bit signed integer

## Signature

```python
def multiply_others(nums: list[int]) -> list[int]:
```

## Your solution

Write it in `workspace/multiply-others/solution.py`, then run the tests:

```bash
python scripts/run_tests.py multiply-others
```
