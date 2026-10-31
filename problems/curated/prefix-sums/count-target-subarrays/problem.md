# Count Target Stretches

**Topic:** Prefix sums · **Difficulty:** Medium

Return how many **contiguous, non-empty** subarrays of `nums` sum to exactly `k`.
Numbers can be negative, so a sliding window does not work here.

## Examples

**Example 1**

```text
Input:  nums = [1, 1, 1], k = 2
Output: 2
```

`[1, 1]` starting at index 0 and at index 1.

**Example 2**

```text
Input:  nums = [1, 2, 3], k = 3
Output: 2
```

`[1, 2]` and `[3]`.

## Constraints

- 0 <= len(nums) <= 10^5
- -1000 <= nums[i] <= 1000
- -10^7 <= k <= 10^7

## Signature

```python
def count_subarrays(nums: list[int], k: int) -> int:
```

## Your solution

Write it in `workspace/count-target-subarrays/solution.py`, then run the tests:

```bash
python scripts/run_tests.py count-target-subarrays
```
