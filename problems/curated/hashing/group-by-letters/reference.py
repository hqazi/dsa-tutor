from collections import defaultdict

def group_words(words):
    groups = defaultdict(list)
    for w in words:
        counts = [0] * 26
        for ch in w:
            counts[ord(ch) - 97] += 1
        groups[tuple(counts)].append(w)
    return list(groups.values())
