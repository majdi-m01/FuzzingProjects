def levenshtein_distance(s1: str, s2: str) -> int:
    d = [[0 for _ in range(len(s2))] for _ in range(len(s1))]
    for i in range(1, len(s1)):
        d[i][0] = i

    for j in range(1, len(s2)):
        d[0][j] = j
 
    for j in range(1, len(s2)):
        for i in range(1, len(s1)):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            d[i][j] = min(d[i-1][j] + 1, d[i][j-1] + 1, d[i][j] + cost)

    return d[-1][-1]
