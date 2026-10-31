def max_haul(stalls):
    skip, take = 0, 0  # best total so far if the previous stall was skipped / taken
    for value in stalls:
        skip, take = max(skip, take), skip + value
    return max(skip, take)
