def balanced_strings(pairs):
    out = []

    def build(prefix, opened, closed):
        if len(prefix) == 2 * pairs:
            out.append(prefix)
            return
        if opened < pairs:
            build(prefix + "(", opened + 1, closed)
        if closed < opened:
            build(prefix + ")", opened, closed + 1)

    build("", 0, 0)
    return out
