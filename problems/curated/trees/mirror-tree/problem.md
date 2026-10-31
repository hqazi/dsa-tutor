# Mirror the Tree

**Topic:** Binary trees · **Difficulty:** Easy

Turn a binary tree into its **mirror image**: at every node, swap the left and
right subtrees. Return the root.

## Examples

**Example 1**

```text
Input:  root = [4, 2, 7, 1, 3, 6, 9]
Output: [4, 7, 2, 9, 6, 3, 1]
```

**Example 2**

```text
Input:  root = [2, 1]
Output: [2, None, 1]
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

def mirror(root: TreeNode | None) -> TreeNode | None:
```

`TreeNode` values are given to you already built; in the examples they are written as lists (trees in level order, `None` for a missing child).

## Your solution

Write it in `workspace/mirror-tree/solution.py`, then run the tests:

```bash
python scripts/run_tests.py mirror-tree
```
