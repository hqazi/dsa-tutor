# Range Totals

**Topic:** Prefix sums · **Difficulty:** Easy

You are given `nums` and a list of `queries`. Each query `[l, r]` asks for
`nums[l] + nums[l+1] + ... + nums[r]` (both ends included).

Return the answers in query order. There can be as many queries as numbers, so
avoid re-adding the same elements for every query.

## Examples

**Example 1**

```text
Input:  nums = [3, -1, 4, 1, 5], queries = [[0, 2], [1, 3], [4, 4]]
Output: [6, 4, 5]
```

`3 - 1 + 4 = 6`, `-1 + 4 + 1 = 4`, and `5`.

**Example 2**

```text
Input:  nums = [10], queries = []
Output: []
```

## Constraints

- 1 <= len(nums) <= 10^5
- 0 <= len(queries) <= 10^5
- 0 <= l <= r < len(nums)
- -10^4 <= nums[i] <= 10^4

## Signature

```python
def range_totals(nums: list[int], queries: list[list[int]]) -> list[int]:
```

## Your solution

Write it in `workspace/range-totals/solution.py`, then run the tests:

```bash
python scripts/run_tests.py range-totals
```
