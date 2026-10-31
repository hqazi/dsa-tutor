from collections import deque

def can_finish(courses, prereqs):
    unlocks = [[] for _ in range(courses)]
    waiting = [0] * courses
    for a, b in prereqs:
        unlocks[b].append(a)
        waiting[a] += 1
    ready = deque(c for c in range(courses) if waiting[c] == 0)
    done = 0
    while ready:
        c = ready.popleft()
        done += 1
        for nxt in unlocks[c]:
            waiting[nxt] -= 1
            if waiting[nxt] == 0:
                ready.append(nxt)
    return done == courses
