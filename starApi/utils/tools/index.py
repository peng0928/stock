def to_yi(n):
    n = int(n)
    s = round(n / 100000000, 2)
    if s < 1:
        s = round(n / 10000, 2)
        s = str(s) + '万'
    else:
        s = str(s) + '亿'
    return s
