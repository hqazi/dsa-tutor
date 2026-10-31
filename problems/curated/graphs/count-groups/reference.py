def count_groups(n, friendships):
    graph = [[] for _ in range(n)]
    for a, b in friendships:
        graph[a].append(b)
        graph[b].append(a)
    seen = [False] * n
    groups = 0
    for person in range(n):
        if seen[person]:
            continue
        groups += 1
        seen[person] = True
        stack = [person]
        while stack:
            cur = stack.pop()
            for friend in graph[cur]:
                if not seen[friend]:
                    seen[friend] = True
                    stack.append(friend)
    return groups
