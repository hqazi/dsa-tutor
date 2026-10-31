def subsets(players):
    out = []
    team = []

    def explore(i):
        if i == len(players):
            out.append(team[:])
            return
        team.append(players[i])      # choose
        explore(i + 1)
        team.pop()                   # undo
        explore(i + 1)               # skip

    explore(0)
    return out
