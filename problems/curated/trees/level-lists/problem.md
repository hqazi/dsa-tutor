# Level by Level

**Topic:** Binary trees · **Difficulty:** Medium

Return the values of a binary tree **level by level**, from the root down, and
left to right within each level.

## Examples

**Example 1**

```text
Input:  root = [3, 9, 20, None, None, 15, 7]
Output: [[3], [9, 20], [15, 7]]
```

**Example 2**

```text
Input:  root = []
Output: []
```

## Constraints

- 0 <= number of nodes <= 10^4

## Signature

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def levels(root: TreeNode | None) -> list[list[int]]:
```

`TreeNode` values are given to you already built; in the examples they are written as lists (trees in level order, `None` for a missing child).

## Your solution

Write it in `workspace/level-lists/solution.py`, then run the tests:

```bash
python scripts/run_tests.py level-lists
```
