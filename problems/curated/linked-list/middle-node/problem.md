# Middle of the Train

**Topic:** Linked lists · **Difficulty:** Easy

Return the **middle node** of a linked list. If there are two middle nodes (even
length), return the second one. Return `None` for an empty list.

The result is checked as the list that starts at the returned node. Try to find it
in a single pass.

## Examples

**Example 1**

```text
Input:  head = [1, 2, 3, 4, 5]
Output: [3, 4, 5]
```

The middle node holds 3, so the answer is the list starting there.

**Example 2**

```text
Input:  head = [1, 2, 3, 4, 5, 6]
Output: [4, 5, 6]
```

The two middles hold 3 and 4; return the second.

## Constraints

- 0 <= length <= 10^5

## Signature

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def middle_node(head: ListNode | None) -> ListNode | None:
```

`ListNode` values are given to you already built; in the examples they are written as lists (trees in level order, `None` for a missing child).

## Your solution

Write it in `workspace/middle-node/solution.py`, then run the tests:

```bash
python scripts/run_tests.py middle-node
```
