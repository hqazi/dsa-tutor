# Best Week of Sales

**Topic:** Sliding window · **Difficulty:** Easy

`sales[i]` is the profit (possibly negative) on day `i`. Return the largest total
profit over any `k` **consecutive** days.

## Examples

**Example 1**

```text
Input:  sales = [2, 1, 5, 1, 3, 2], k = 3
Output: 9
```

Days 2–4 give `5 + 1 + 3 = 9`.

**Example 2**

```text
Input:  sales = [-4, -1, -7], k = 1
Output: -1
```

## Constraints

- 1 <= k <= len(sales) <= 10^5
- -10^4 <= sales[i] <= 10^4

## Signature

```python
def best_window(sales: list[int], k: int) -> int:
```

## Your solution

Write it in `workspace/best-window/solution.py`, then run the tests:

```bash
python scripts/run_tests.py best-window
```
