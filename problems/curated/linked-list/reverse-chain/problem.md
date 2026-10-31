# Reverse the Chain

**Topic:** Linked lists · **Difficulty:** Easy

Given the head of a singly linked list, reverse the list **by rewiring the `next`
pointers** and return the new head. Do not build a new list.

## Examples

**Example 1**

```text
Input:  head = [1, 2, 3, 4, 5]
Output: [5, 4, 3, 2, 1]
```

**Example 2**

```text
Input:  head = []
Output: []
```

## Constraints

- 0 <= length <= 10^5
- -10^5 <= node.val <= 10^5

## Signature

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list(head: ListNode | None) -> ListNode | None:
```

`ListNode` values are given to you already built; in the examples they are written as lists (trees in level order, `None` for a missing child).

## Your solution

Write it in `workspace/reverse-chain/solution.py`, then run the tests:

```bash
python scripts/run_tests.py reverse-chain
```
