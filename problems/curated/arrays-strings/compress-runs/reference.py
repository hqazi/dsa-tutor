def compress_runs(log):
    parts = []
    i = 0
    while i < len(log):
        j = i
        while j < len(log) and log[j] == log[i]:
            j += 1
        run = j - i
        parts.append(log[i] if run == 1 else log[i] + str(run))
        i = j
    return "".join(parts)
