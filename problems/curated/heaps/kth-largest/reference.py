import heapq

def kth_largest(scores, k):
    heap = []
    for s in scores:
        heapq.heappush(heap, s)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]
