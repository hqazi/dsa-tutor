def best_window(sales, k):
    window = sum(sales[:k])
    best = window
    for i in range(k, len(sales)):
        window += sales[i] - sales[i - k]
        best = max(best, window)
    return best
