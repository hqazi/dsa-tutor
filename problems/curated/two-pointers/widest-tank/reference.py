def max_water(walls):
    i, j = 0, len(walls) - 1
    best = 0
    while i < j:
        best = max(best, (j - i) * min(walls[i], walls[j]))
        if walls[i] < walls[j]:
            i += 1
        else:
            j -= 1
    return best
