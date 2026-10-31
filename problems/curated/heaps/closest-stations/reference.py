import heapq

def k_closest(stations, k):
    # heapq.nsmallest keeps a heap of size k internally
    best = heapq.nsmallest(k, stations, key=lambda p: (p[0] * p[0] + p[1] * p[1], p[0], p[1]))
    return [list(p) for p in best]
