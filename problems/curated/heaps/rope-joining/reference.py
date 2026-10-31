import heapq

def min_join_cost(ropes):
    heap = list(ropes)
    heapq.heapify(heap)
    total = 0
    while len(heap) > 1:
        joined = heapq.heappop(heap) + heapq.heappop(heap)
        total += joined
        heapq.heappush(heap, joined)
    return total
