def shortest_window(amounts, goal):
    best = len(amounts) + 1
    total = 0
    left = 0
    for right, x in enumerate(amounts):
        total += x
        while total >= goal:
            best = min(best, right - left + 1)
            total -= amounts[left]
            left += 1
    return best if best <= len(amounts) else 0
