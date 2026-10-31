def can_reach_end(jumps):
    furthest = 0
    for i, j in enumerate(jumps):
        if i > furthest:
            return False
        furthest = max(furthest, i + j)
    return True
