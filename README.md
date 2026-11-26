# Actividad 1 – Diseño, análisis y comparación de algoritmos (LCS)

Tres implementaciones de la **subsecuencia común más larga** (*Longest Common Subsequence*, LCS) de dos cadenas, con su análisis de complejidad y una comparación experimental de tiempo de CPU y memoria.

| Versión | Técnica | Tiempo | Memoria |
|---|---|---|---|
| **A** – `lcs_recursiva.py` | Recursiva directa, sin memorización | exponencial (peor caso: 2·C(m+n, m) − 1 llamadas) | O(m+n) (pila) |
| **B** – `lcs_hirschberg.py` | Divide y vencerás de Hirschberg | O(m·n) | O(n) |
| **C** – `lcs_dp.py` | Programación dinámica tabular | O(m·n) | O(m·n) |

> Asignatura: Diseño avanzado de algoritmos · Autor: **[Nombre y apellidos]**

## Requisitos

- Python 3.10 o superior (probado con 3.14)
- `make` (Linux/macOS; en Windows, usar Git Bash/WSL o ejecutar los tres comandos de la sección *Sin make*)
- Dependencias de Python: `matplotlib` y `pytest` (ver `requirements.txt`). No se usa ninguna librería específica de LCS.

## Ejecución con un único comando

```bash
git clone https://github.com/TU_USUARIO/lcs-actividad1.git
cd lcs-actividad1
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
make
```

`make` ejecuta en orden:

1. **`make test`** – pruebas de corrección (`pytest`).
2. **`make bench`** – experimentos; genera `data/resultados.csv`.
3. **`make plots`** – genera las gráficas `data/grafica_*.png` e imprime la tabla de resultados en Markdown.

El benchmark completo tarda unos minutos, porque la versión A en el peor caso con n = 14 necesita unos 7 s por medición y se repite varias veces. Para una prueba rápida:

```bash
python src/benchmark.py --rapido
```

### Sin `make`

```bash
python -m pytest tests -q
python src/benchmark.py
python src/graficas.py
```

## Estructura del proyecto

```
lcs-actividad1/
├── src/
│   ├── lcs_recursiva.py    # Versión A: recursiva directa (con contador de llamadas)
│   ├── lcs_hirschberg.py   # Versión B: Hirschberg (divide y vencerás, DP de dos filas)
│   ├── lcs_dp.py           # Versión C: programación dinámica tabular
│   ├── generador.py        # Generación reproducible de cadenas (aleatorias y peor caso)
│   ├── benchmark.py        # Medición de tiempo de CPU y memoria máxima
│   └── graficas.py         # Gráficas y tabla de resultados
├── tests/test_lcs.py       # Pruebas: casos límite, ejemplo del Tema 3 y 200 parejas aleatorias
├── data/                   # resultados.csv y gráficas generadas
├── Makefile
├── requirements.txt
└── README.md
```

## Metodología experimental

- **Datos:** para n ∈ {6, 8, 10, 12, 14, 16} se usa el **peor caso** de la versión A (`"A"*n` frente a `"B"*n`, sin símbolos comunes). Para n ∈ {100, 250, 500, 1000, 2000} se usan cadenas aleatorias sobre el alfabeto ACGT con semilla fija. La versión A solo se ejecuta en los tamaños pequeños.
- **Tiempo:** tiempo de CPU del proceso (`time.process_time`), mediana de 3 repeticiones.
- **Memoria:** pico de memoria asignada por Python (`tracemalloc`), en una ejecución aparte para no alterar el tiempo.
- **Aislamiento:** cada medición se ejecuta en un proceso nuevo, con un tiempo máximo de 60 s. Si se supera, la fila queda como `timeout` en el CSV.

### Limitaciones

- `tracemalloc` no cuenta la pila de llamadas, por lo que la memoria de la versión A queda infravalorada (teóricamente O(m+n) marcos de pila).
- Se mide una sola pareja por tamaño y los tiempos varían algo entre ejecuciones según la carga de la máquina.

## Resultados principales

Medidos en el equipo del autor (Python 3.14). Los valores exactos están en `data/resultados.csv`.

| n | A: tiempo (ms) | A: llamadas | B: tiempo (ms) | B: MB | C: tiempo (ms) | C: MB |
|---|---|---|---|---|---|---|
| 6 | 0,169 | 1 847 | 0,024 | 0,001 | 0,015 | 0,0005 |
| 8 | 2,38 | 25 739 | 0,031 | 0,0012 | 0,026 | 0,0009 |
| 10 | 35,4 | 369 511 | 0,039 | 0,0016 | 0,023 | 0,0012 |
| 12 | 489 | 5 408 311 | 0,039 | 0,0018 | 0,025 | 0,0016 |
| 14 | 7 392 | 80 233 199 | 0,046 | 0,002 | 0,029 | 0,002 |
| 16 | timeout (> 60 s) | 1 202 160 779 (medición individual: 122 s) | 0,064 | 0,0021 | 0,043 | 0,0026 |
| 100 | — | — | 1,65 | 0,0065 | 0,964 | 0,0863 |
| 250 | — | — | 8,86 | 0,0131 | 5,89 | 0,5202 |
| 500 | — | — | 35,1 | 0,0225 | 26,1 | 2,185 |
| 1000 | — | — | 154 | 0,0734 | 118 | 12,02 |
| 2000 | — | — | 602 | 0,1909 | 549 | 56,01 |

Conclusiones breves:

- **A** es exponencial: el número de llamadas coincide exactamente con 2·C(2n, n) − 1, y con n = 16 ya tarda más de dos minutos.
- **C** es la más simple y rápida, pero su memoria crece como n² (56 MB con n = 2000).
- **B** mantiene el tiempo O(m·n), con una constante algo mayor (entre 1,1 y 1,7 veces más lento que C), y reduce la memoria a O(n) (unas 290 veces menos con n = 2000).

La memoria completa, con el análisis detallado y las gráficas, está en el PDF de la entrega.

## Referencias

- Hirschberg, D. S. (1975). *A linear space algorithm for computing maximal common subsequences.* Communications of the ACM, 18(6), 341–343.
- Cormen, Leiserson, Rivest y Stein. *Introduction to Algorithms* (capítulo de programación dinámica, LCS).
- Material de la asignatura: Temas 1, 2 y 3.
