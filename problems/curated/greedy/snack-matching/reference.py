def max_content(appetites, snacks):
    appetites = sorted(appetites)
    snacks = sorted(snacks)
    person = 0
    for size in snacks:
        if person < len(appetites) and size >= appetites[person]:
            person += 1
    return person
