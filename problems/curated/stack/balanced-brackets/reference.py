def is_balanced(code):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in code:
        if ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
        else:
            stack.append(ch)
    return not stack
