def count_ways(steps):
    a, b = 1, 1  # ways to reach step i - 1 and step i
    for _ in range(steps - 1):
        a, b = b, a + b
    return b if steps else 1
