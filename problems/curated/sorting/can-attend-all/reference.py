def can_attend_all(meetings):
    ordered = sorted(meetings)
    for prev, cur in zip(ordered, ordered[1:]):
        if cur[0] < prev[1]:
            return False
    return True
