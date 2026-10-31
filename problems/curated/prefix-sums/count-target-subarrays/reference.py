from collections import defaultdict

def count_subarrays(nums, k):
    seen = defaultdict(int)
    seen[0] = 1
    running = 0
    count = 0
    for x in nums:
        running += x
        count += seen[running - k]
        seen[running] += 1
    return count
