def ultima_fila(a, b):
    prev = [0]*(len(b)+1)
    for x in a:
        cur = [0]*(len(b)+1)
        for j in range(1, len(b)+1):
            if x == b[j-1]:
                cur[j] = prev[j-1] + 1
            else:
                cur[j] = max(prev[j], cur[j-1])
        prev = cur
    return prev          # prev[j] = LCS(a, b[:j])

def hirschberg(a, b):
    if len(a) == 0 or len(b) == 0:
        return ""
    if len(a) == 1:
        return a if a in b else ""          # caso base
    mid = len(a)//2
    a1, a2 = a[:mid], a[mid:]
    fwd = ultima_fila(a1, b)
    bwd = ultima_fila(a2[::-1], b[::-1])    # sobre cadenas invertidas
    n = len(b)
    # bwd[n-j] = LCS(a2, b[j:])
    k = max(range(n+1), key=lambda j: fwd[j] + bwd[n-j])
    return hirschberg(a1, b[:k]) + hirschberg(a2, b[k:])
