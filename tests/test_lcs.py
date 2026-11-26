import random
import pytest
from lcs_recursiva import lcs_rec
from lcs_hirschberg import hirschberg
from lcs_dp import lcs_dp

VERSIONES = [lcs_rec, hirschberg, lcs_dp]

def es_subsecuencia(s, t):
    it = iter(t)
    return all(c in it for c in s)   # c in it consume el iterador: respeta el orden

CASOS = [
    ("ABCBDAB", "BDCABA", 4),
    ("ACCGGTCGAGTGCGCGGAAGCCGGCCGAA"[:14], "GTCGTTCGGAATGCCGTTGCTCTGTAAA"[:14], None),
    ("ABC", "ABC", 3),        # idénticas
    ("AAA", "BBB", 0),        # sin nada en común
    ("", "ABC", 0),           # cadena vacía
    ("A", "A", 1),
    ("A", "B", 0),
]

@pytest.mark.parametrize("f", VERSIONES)
@pytest.mark.parametrize("a,b,esperado", CASOS)
def test_casos(f, a, b, esperado):
    r = f(a, b)
    assert es_subsecuencia(r, a) and es_subsecuencia(r, b)
    assert len(r) == len(lcs_dp(a, b))
    if esperado is not None:
        assert len(r) == esperado

def test_tema3_dp_y_hirschberg():
    A = "ACCGGTCGAGTGCGCGGAAGCCGGCCGAA"
    B = "GTCGTTCGGAATGCCGTTGCTCTGTAAA"
    assert len(lcs_dp(A, B)) == 20
    assert len(hirschberg(A, B)) == 20

def test_aleatorio():
    random.seed(7)
    for _ in range(200):
        a = "".join(random.choice("ACGT") for _ in range(random.randint(0, 12)))
        b = "".join(random.choice("ACGT") for _ in range(random.randint(0, 12)))
        longitudes = {len(f(a, b)) for f in VERSIONES}
        assert len(longitudes) == 1, (a, b)
        for f in VERSIONES:
            r = f(a, b)
            assert es_subsecuencia(r, a) and es_subsecuencia(r, b)
