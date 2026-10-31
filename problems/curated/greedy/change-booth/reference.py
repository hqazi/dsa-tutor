def can_give_change(bills):
    fives = tens = 0
    for bill in bills:
        if bill == 5:
            fives += 1
        elif bill == 10:
            if fives == 0:
                return False
            fives -= 1
            tens += 1
        else:
            if tens and fives:      # prefer giving a 10: fives are more flexible
                tens -= 1
                fives -= 1
            elif fives >= 3:
                fives -= 3
            else:
                return False
    return True
