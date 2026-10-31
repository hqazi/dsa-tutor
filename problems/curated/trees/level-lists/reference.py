from collections import deque

def levels(root):
    if root is None:
        return []
    out = []
    queue = deque([root])
    while queue:
        row = []
        for _ in range(len(queue)):
            node = queue.popleft()
            row.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        out.append(row)
    return out
