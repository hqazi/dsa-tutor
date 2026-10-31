def power_mod(base, exp, mod):
    if exp == 0:
        return 1 % mod
    half = power_mod(base, exp // 2, mod)
    result = half * half % mod
    if exp % 2:
        result = result * (base % mod) % mod
    return result
