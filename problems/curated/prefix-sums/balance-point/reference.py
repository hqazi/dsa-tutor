def balance_index(weights):
    total = sum(weights)
    left = 0
    for i, w in enumerate(weights):
        if left == total - left - w:
            return i
        left += w
    return -1
