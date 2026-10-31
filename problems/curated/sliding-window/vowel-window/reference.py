def max_vowels(text, k):
    vowels = set("aeiou")
    count = sum(ch in vowels for ch in text[:k])
    best = count
    for i in range(k, len(text)):
        count += (text[i] in vowels) - (text[i - k] in vowels)
        best = max(best, count)
    return best
