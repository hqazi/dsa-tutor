def fewest_coins(coins, amount):
    INF = amount + 1
    best = [0] + [INF] * amount
    for total in range(1, amount + 1):
        for c in coins:
            if c <= total and best[total - c] + 1 < best[total]:
                best[total] = best[total - c] + 1
    return best[amount] if best[amount] != INF else -1
