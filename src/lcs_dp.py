def lcs_dp(a, b):
    m, n = len(a), len(b)
    L = [[0]*(n+1) for _ in range(m+1)]       # bordes a 0
    for i in range(1, m+1):
        for j in range(1, n+1):
            if a[i-1] == b[j-1]:
                L[i][j] = L[i-1][j-1] + 1
            else:
                L[i][j] = max(L[i-1][j], L[i][j-1])
    # reconstrucción hacia atrás desde L[m][n]
    i, j, res = m, n, []
    while i > 0 and j > 0:
        if a[i-1] == b[j-1]:
            res.append(a[i-1]); i -= 1; j -= 1
        elif L[i-1][j] >= L[i][j-1]:
            i -= 1
        else:
            j -= 1
    return "".join(reversed(res))
