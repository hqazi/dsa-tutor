# Balance Point

**Topic:** Prefix sums · **Difficulty:** Easy

Return the **leftmost** index `i` where the sum of the weights strictly to the left
of `i` equals the sum strictly to the right of `i`. An empty side sums to 0.
Return `-1` if there is no such index.

## Examples

**Example 1**

```text
Input:  weights = [1, 7, 3, 6, 5, 6]
Output: 3
```

Left of index 3: `1 + 7 + 3 = 11`; right: `5 + 6 = 11`.

**Example 2**

```text
Input:  weights = [1, 2, 3]
Output: -1
```

**Example 3**

```text
Input:  weights = [2, 1, -1]
Output: 0
```

At index 0 the left side is empty (0) and the right side is `1 - 1 = 0`.

## Constraints

- 0 <= len(weights) <= 10^5
- -1000 <= weights[i] <= 1000

## Signature

```python
def balance_index(weights: list[int]) -> int:
```

## Your solution

Write it in `workspace/balance-point/solution.py`, then run the tests:

```bash
python scripts/run_tests.py balance-point
```
