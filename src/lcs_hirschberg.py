def ultima_fila(a, b, a0, a1, b0, b1, invertir=False):
    """Última fila de la tabla DP de a[a0:a1] frente a b[b0:b1] (dos filas, O(n)).
    Con invertir=True recorre ambos tramos de derecha a izquierda, sin copiarlos."""
    n = b1 - b0
    prev = [0] * (n + 1)
    idx_a = range(a1 - 1, a0 - 1, -1) if invertir else range(a0, a1)
    for i in idx_a:
        x = a[i]
        cur = [0] * (n + 1)
        for j in range(1, n + 1):
            y = b[b1 - j] if invertir else b[b0 + j - 1]
            cur[j] = prev[j - 1] + 1 if x == y else max(prev[j], cur[j - 1])
        prev = cur
    return prev


def punto_corte(a, b, a0, am, a1, b0, b1):
    """Calcula k en una función aparte: fwd y bwd se liberan al volver."""
    n = b1 - b0
    fwd = ultima_fila(a, b, a0, am, b0, b1)                 # LCS(a[a0:am], b[b0:b0+j])
    bwd = ultima_fila(a, b, am, a1, b0, b1, invertir=True)  # LCS(a[am:a1], b[b0+j:b1]) = bwd[n-j]
    return max(range(n + 1), key=lambda j: fwd[j] + bwd[n - j])


def _rec(a, b, a0, a1, b0, b1, salida):
    if a0 == a1 or b0 == b1:
        return
    if a1 - a0 == 1:                                        # caso base
        if a[a0] in b[b0:b1]:
            salida.append(a[a0])
        return
    am = (a0 + a1) // 2
    k = b0 + punto_corte(a, b, a0, am, a1, b0, b1)
    _rec(a, b, a0, am, b0, k, salida)
    _rec(a, b, am, a1, k, b1, salida)


def hirschberg(a, b):
    salida = []
    _rec(a, b, 0, len(a), 0, len(b), salida)
    return "".join(salida)
