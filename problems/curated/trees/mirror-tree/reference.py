def mirror(root):
    if root is None:
        return None
    root.left, root.right = mirror(root.right), mirror(root.left)
    return root
