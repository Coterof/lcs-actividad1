import random


def generar_par(n, semilla=42, alfabeto="ACGT"):
    """Par de cadenas aleatorias de longitud n, reproducible."""
    rng = random.Random(semilla + n)
    a = "".join(rng.choice(alfabeto) for _ in range(n))
    b = "".join(rng.choice(alfabeto) for _ in range(n))
    return a, b


def generar_peor_caso(n):
    """Sin caracteres en común: A hace ~2*C(2n,n) llamadas (peor caso)."""
    return "A" * n, "B" * n


def generar(n, tipo="aleatorio"):
    return generar_peor_caso(n) if tipo == "peor" else generar_par(n)
