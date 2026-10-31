def insert_position(sorted_ids, target):
    lo, hi = 0, len(sorted_ids)
    while lo < hi:
        mid = (lo + hi) // 2
        if sorted_ids[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo
