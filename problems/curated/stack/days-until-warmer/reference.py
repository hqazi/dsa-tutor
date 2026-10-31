def wait_days(temps):
    out = [0] * len(temps)
    stack = []  # indices of days still waiting, temperatures non-increasing
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:
            j = stack.pop()
            out[j] = i - j
        stack.append(i)
    return out
