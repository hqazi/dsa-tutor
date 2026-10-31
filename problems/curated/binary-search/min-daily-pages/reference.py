def min_daily_pages(chapters, days):
    def days_needed(limit):
        used, today = 1, 0
        for c in chapters:
            if today + c > limit:
                used += 1
                today = 0
            today += c
        return used

    lo, hi = max(chapters), sum(chapters)
    while lo < hi:
        mid = (lo + hi) // 2
        if days_needed(mid) <= days:
            hi = mid
        else:
            lo = mid + 1
    return lo
