# How Tall Is the Tree?

**Topic:** Binary trees · **Difficulty:** Easy

Return the **depth** of a binary tree: the number of nodes on the longest path from
the root down to a leaf. An empty tree has depth 0.

## Examples

**Example 1**

```text
Input:  root = [3, 9, 20, None, None, 15, 7]
Output: 3
```

The path 3 → 20 → 15 has three nodes.

**Example 2**

```text
Input:  root = []
Output: 0
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

def max_depth(root: TreeNode | None) -> int:
```

`TreeNode` values are given to you already built; in the examples they are written as lists (trees in level order, `None` for a missing child).

## Your solution

Write it in `workspace/tree-depth/solution.py`, then run the tests:

```bash
python scripts/run_tests.py tree-depth
```
