# Is It a Search Tree?

**Topic:** Binary trees · **Difficulty:** Medium

A binary tree is a **binary search tree** if, for every node, every value in its
left subtree is strictly smaller than the node's value and every value in its
right subtree is strictly larger.

Return `True` if the tree is a binary search tree. An empty tree is one.
Checking only each node against its children is not enough.

## Examples

**Example 1**

```text
Input:  root = [2, 1, 3]
Output: True
```

**Example 2**

```text
Input:  root = [5, 1, 4, None, None, 3, 6]
Output: False
```

4 is in the right subtree of 5 but is smaller than 5.

## Constraints

- 0 <= number of nodes <= 10^4
- -2^31 <= node.val <= 2^31 - 1

## Signature

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def is_bst(root: TreeNode | None) -> bool:
```

`TreeNode` values are given to you already built; in the examples they are written as lists (trees in level order, `None` for a missing child).

## Your solution

Write it in `workspace/valid-search-tree/solution.py`, then run the tests:

```bash
python scripts/run_tests.py valid-search-tree
```
