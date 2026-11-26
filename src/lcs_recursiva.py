llamadas = 0

def lcs_rec(a, b):
    """LCS recursiva directa, sin memorización. Tiempo exponencial."""
    global llamadas
    llamadas = 0
    def f(i, j):
        global llamadas
        llamadas += 1
        if i == 0 or j == 0:
            return ""
        if a[i-1] == b[j-1]:
            return f(i-1, j-1) + a[i-1]
        x, y = f(i-1, j), f(i, j-1)
        return x if len(x) >= len(y) else y
    return f(len(a), len(b))
