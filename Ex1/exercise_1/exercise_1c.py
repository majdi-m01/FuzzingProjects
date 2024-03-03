"""
Use this file to provide your solutions for exercise 1-1 c.
"""


def levenshtein_distance(s1: str, s2: str) -> int:
    d = [[0 for _ in range(len(s2)+1)] for _ in range(len(s1)+1)]
    for i in range(1, len(s1)+1):
        d[i][0] = i

    for j in range(1, len(s2)+1):
        d[0][j] = j

    for j in range(1, len(s2)+1):
        for i in range(1, len(s1)+1):
            if s1[i-1] == s2[j-1]:
                cost = 0
            else:
                cost = 1
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i-1][j-1] + cost)

    return d[len(s1)][len(s2)]
