def longest_streak(days):
    present = set(days)
    best = 0
    for d in present:
        if d - 1 not in present:
            length = 1
            while d + length in present:
                length += 1
            best = max(best, length)
    return best
