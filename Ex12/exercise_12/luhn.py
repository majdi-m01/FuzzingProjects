def luhn(digits):
    try:
        f = 0
        for n in digits[::2]:
            for d in str(int(n) * 2):
                f += int(d)
        s = 0
        for n in digits[1::2]:
            s += int(n)
        return ((((f + s) // 10) + 1) * 10 - (f + s)) % 10
    except:
        return None
