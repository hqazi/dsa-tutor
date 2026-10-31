# Drop the K-th From the End

**Topic:** Linked lists · **Difficulty:** Medium

Remove the `k`-th node **counting from the end** of the list (`k = 1` is the last
node) and return the head of the resulting list. `k` is always valid.

Try to do it in one pass with two pointers. Watch out for removing the head itself.

## Examples

**Example 1**

```text
Input:  head = [1, 2, 3, 4, 5], k = 2
Output: [1, 2, 3, 5]
```

The 2nd node from the end holds 4.

**Example 2**

```text
Input:  head = [1], k = 1
Output: []
```

## Constraints

- 1 <= length <= 10^5
- 1 <= k <= length

## Signature

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def remove_kth_from_end(head: ListNode | None, k: int) -> ListNode | None:
```

`ListNode` values are given to you already built; in the examples they are written as lists (trees in level order, `None` for a missing child).

## Your solution

Write it in `workspace/drop-kth-from-end/solution.py`, then run the tests:

```bash
python scripts/run_tests.py drop-kth-from-end
```
