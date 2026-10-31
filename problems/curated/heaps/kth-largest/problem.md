# K-th Best Score

**Topic:** Heaps · **Difficulty:** Easy

Return the `k`-th largest value in `scores` (counting duplicates: in `[5, 5, 3]`
the 2nd largest is 5). Try a heap of size `k` rather than sorting everything.

## Examples

**Example 1**

```text
Input:  scores = [3, 2, 1, 5, 6, 4], k = 2
Output: 5
```

**Example 2**

```text
Input:  scores = [3, 2, 3, 1, 2, 4, 5, 5, 6], k = 4
Output: 4
```

## Constraints

- 1 <= k <= len(scores) <= 10^5
- -10^4 <= scores[i] <= 10^4

## Signature

```python
def kth_largest(scores: list[int], k: int) -> int:
```

## Your solution

Write it in `workspace/kth-largest/solution.py`, then run the tests:

```bash
python scripts/run_tests.py kth-largest
```
