def min_climb_cost(cost):
    a, b = 0, 0  # cheapest way to stand at step i - 2 and i - 1 without paying for them yet
    for i in range(2, len(cost) + 1):
        a, b = b, min(b + cost[i - 1], a + cost[i - 2])
    return b
