from collections import Counter

def frequency_sort(nums):
    counts = Counter(nums)
    return sorted(nums, key=lambda x: (-counts[x], x))
