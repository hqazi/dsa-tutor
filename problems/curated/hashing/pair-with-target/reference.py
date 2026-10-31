def find_pair(amounts, target):
    first = {}
    for j, x in enumerate(amounts):
        if target - x in first:
            return [first[target - x], j]
        if x not in first:
            first[x] = j
    return []
