def is_mirror(text):
    i, j = 0, len(text) - 1
    while i < j:
        if not text[i].isalnum():
            i += 1
        elif not text[j].isalnum():
            j -= 1
        elif text[i].lower() != text[j].lower():
            return False
        else:
            i += 1
            j -= 1
    return True
