from collections import defaultdict, deque

def has_route(n, roads, start, end):
    graph = defaultdict(list)
    for a, b in roads:
        graph[a].append(b)
        graph[b].append(a)
    seen = {start}
    queue = deque([start])
    while queue:
        town = queue.popleft()
        if town == end:
            return True
        for nxt in graph[town]:
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return False
