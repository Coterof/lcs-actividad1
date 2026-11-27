# Actividad 1 – Diseño, análisis y comparación de algoritmos (LCS)

Tres implementaciones de la **subsecuencia común más larga** (*Longest Common Subsequence*, LCS) de dos cadenas, con su análisis de complejidad y una comparación experimental de tiempo de CPU y memoria.

| Versión | Técnica | Tiempo | Memoria |
|---|---|---|---|
| **A** – `lcs_recursiva.py` | Recursiva directa, sin memorización | exponencial (peor caso: 2·C(m+n, m) − 1 llamadas) | O(m+n) (pila) |
| **B** – `lcs_hirschberg.py` | Divide y vencerás de Hirschberg | O(m·n) | O(n) |
| **C** – `lcs_dp.py` | Programación dinámica tabular | O(m·n) | O(m·n) |

> Asignatura: Diseño avanzado de algoritmos · Autor: **César Otero Fernández**

---

## Guía rápida

Con Python 3.9 o superior instalado, desde la carpeta del proyecto:

```bash
python -m pip install -r requirements.txt
python run_all.py
```

Funciona igual en Linux, macOS y Windows, y no necesita `make`. En unos minutos ejecuta los tests, los experimentos y genera las gráficas en `data/`. Para una comprobación rápida (unos segundos): `python run_all.py --rapido`.

Si `python` no se reconoce, prueba `python3` (Linux/macOS) o `py` (Windows). Las instrucciones detalladas por sistema están más abajo.

---

## Requisitos

- **Python 3.9 o superior** (desarrollado y probado con 3.14).
- **Dependencias:** `matplotlib` (gráficas) y `pytest` (tests), indicadas en `requirements.txt`. Los algoritmos y el benchmark solo usan la librería estándar, y no se utiliza ninguna librería específica de LCS.
- `make` es **opcional**.

## Instalación y ejecución paso a paso

Primero, descargar el proyecto (cualquiera de las dos formas):

```bash
git clone https://github.com/Coterof/lcs-actividad1.git
cd lcs-actividad1
```
o bien descargar el ZIP desde GitHub (*Code → Download ZIP*), descomprimirlo y abrir una terminal en esa carpeta.

### Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run_all.py          # o simplemente: make
```
En Debian/Ubuntu, si falla la creación del entorno: `sudo apt install python3-venv`.

### macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run_all.py          # o simplemente: make
```

### Windows (PowerShell o CMD)

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1      # en CMD: .venv\Scripts\activate.bat
pip install -r requirements.txt
python run_all.py
```
Si PowerShell bloquea la activación del entorno, ejecutar antes `Set-ExecutionPolicy -Scope Process Bypass`, o usar CMD. En Windows no hace falta `make`: `run_all.py` hace lo mismo.

### Sin entorno virtual (opción más corta)

Si no se quiere crear un entorno virtual:
```bash
python -m pip install --user -r requirements.txt
python run_all.py
```

### Google Colab (sin instalar nada)

En un cuaderno nuevo de https://colab.research.google.com, ejecutar en una celda:
```python
!git clone https://github.com/Coterof/lcs-actividad1.git
%cd lcs-actividad1
!pip install -r requirements.txt
!python run_all.py --rapido
```
Quitar `--rapido` para el experimento completo. Las gráficas quedan en la carpeta `data/` del entorno de Colab.

## Formas de ejecutar el proyecto

Las tres hacen exactamente lo mismo (tests → experimentos → gráficas):

| Forma | Comando | Cuándo usarla |
|---|---|---|
| Script de Python | `python run_all.py` | En cualquier sistema (recomendada) |
| Make | `make` (con otro intérprete: `make PYTHON=python3`) | Linux/macOS |
| Manual | `python -m pytest tests -q` · `python src/benchmark.py` · `python src/graficas.py` | Para ejecutar solo una parte |

Opciones útiles:
- **Solo tests:** `python -m pytest tests -q` (o `make test`). Deben pasar 23 pruebas.
- **Solo una comprobación rápida de los experimentos:** `python src/benchmark.py --rapido`.
- **Medidas extra de la versión A** (cadenas aleatorias y peor caso con n = 16; las cifras citadas en la memoria): `python src/extra_a.py`. Tarda unos minutos.
- **Probar una versión suelta**, por ejemplo Hirschberg:
  ```bash
  python -c "import sys; sys.path.insert(0, 'src'); from lcs_hirschberg import hirschberg; print(hirschberg('ABCBDAB', 'BDCABA'))"
  ```

### Qué genera la ejecución

- `data/resultados.csv`: tiempo de CPU, memoria máxima y número de llamadas de cada versión y tamaño.
- `data/grafica_tiempo.png`, `data/grafica_memoria.png` y `data/grafica_llamadas.png`.
- Por pantalla, la tabla de resultados en formato Markdown.

El experimento completo tarda unos minutos, porque la versión A en el peor caso con n = 14 necesita unos 7 s por medición y se repite varias veces, y con n = 16 se espera hasta el límite de 60 s antes de marcarla como `timeout`. Los tiempos absolutos dependen del equipo, y los órdenes de crecimiento deben ser los mismos.

## Problemas frecuentes

| Problema | Solución |
|---|---|
| `python: command not found` / `'python' no se reconoce` | Usar `python3` (Linux/macOS) o `py` (Windows) en lugar de `python`. |
| `make: command not found` / `make` no existe en Windows | Usar `python run_all.py`, que no necesita make. |
| `make` usa un Python distinto al deseado | `make PYTHON=python3` |
| `externally-managed-environment` al hacer `pip install` | Crear un entorno virtual (`python3 -m venv .venv` y activarlo), o usar `pip install --user --break-system-packages -r requirements.txt` como último recurso. |
| `No module named matplotlib` / `pytest` | Activar el entorno virtual y repetir `pip install -r requirements.txt`. |
| `ModuleNotFoundError: lcs_dp` al lanzar un script a mano | Ejecutar desde la raíz del proyecto, como en los ejemplos (`python src/benchmark.py`). |
| PowerShell no deja activar el entorno | `Set-ExecutionPolicy -Scope Process Bypass`, o usar CMD. |
| El experimento tarda demasiado | `python run_all.py --rapido`. |

## Estructura del proyecto

```
lcs-actividad1/
├── src/
│   ├── lcs_recursiva.py    # Versión A: recursiva directa (con contador de llamadas)
│   ├── lcs_hirschberg.py   # Versión B: Hirschberg (divide y vencerás, DP de dos filas, trabaja con índices)
│   ├── lcs_dp.py           # Versión C: programación dinámica tabular
│   ├── generador.py        # Generación reproducible de cadenas (aleatorias y peor caso)
│   ├── benchmark.py        # Medición de tiempo de CPU y memoria máxima
│   ├── extra_a.py          # Medidas extra de A (cadenas aleatorias n = 16, 18, 20 y peor caso n = 16)
│   └── graficas.py         # Gráficas y tabla de resultados
├── tests/test_lcs.py       # Pruebas: casos límite, ejemplo del Tema 3 y 200 parejas aleatorias
├── data/                   # resultados.csv y gráficas generadas
├── run_all.py              # Ejecuta todo con un único comando (multiplataforma)
├── Makefile                # Equivalente a run_all.py para Linux/macOS
├── pytest.ini
├── requirements.txt
└── README.md
```

## Metodología experimental

- **Datos:** para n ∈ {6, 8, 10, 12, 14, 16} se usa el **peor caso** de la versión A (`"A"*n` frente a `"B"*n`, sin símbolos comunes). Para n ∈ {100, 250, 500, 1000, 2000} se usan cadenas aleatorias sobre el alfabeto ACGT con semilla fija. La versión A solo se ejecuta en los tamaños pequeños.
- **Tiempo:** tiempo de CPU del proceso (`time.process_time`), mediana de 3 repeticiones.
- **Memoria:** pico de memoria asignada por Python (`tracemalloc`), en una ejecución aparte para no alterar el tiempo.
- **Aislamiento:** cada medición se ejecuta en un proceso nuevo, con un tiempo máximo de 60 s. Si se supera, la fila queda como `timeout` en el CSV.

### Limitaciones

- `tracemalloc` no cuenta la pila de llamadas, por lo que la memoria de la versión A queda infravalorada (teóricamente O(m+n) marcos de pila). Además cuenta cada entero grande como objeto, por lo que la memoria de B no crece de forma perfectamente regular entre tamaños.
- Se mide una sola pareja por tamaño y los tiempos varían algo entre ejecuciones según la carga de la máquina; con tamaños pequeños, la diferencia entre B y C puede incluso invertirse por el ruido de medición.

## Resultados principales

Medidos en un equipo con Intel Core i5-1135G7, 16 GB de RAM, Omarchy Linux y Python 3.14.10. Los valores exactos están en `data/resultados.csv`.

| n | A: tiempo (ms) | A: llamadas | B: tiempo (ms) | B: MB | C: tiempo (ms) | C: MB |
|---|---|---|---|---|---|---|
| 6 | 0,167 | 1 847 | 0,027 | 0,0005 | 0,015 | 0,0005 |
| 8 | 2,35 | 25 739 | 0,028 | 0,0005 | 0,017 | 0,0009 |
| 10 | 32,7 | 369 511 | 0,036 | 0,0006 | 0,020 | 0,0012 |
| 12 | 479 | 5 408 311 | 0,041 | 0,0006 | 0,026 | 0,0016 |
| 14 | 7 140 | 80 233 199 | 0,057 | 0,0006 | 0,031 | 0,002 |
| 16 | timeout (> 60 s) | 1 202 160 779 (medición individual: 122 s) | 0,082 | 0,0006 | 0,044 | 0,0026 |
| 100 | — | — | 1,97 | 0,0026 | 1,04 | 0,0863 |
| 250 | — | — | 11,3 | 0,0062 | 6,25 | 0,5202 |
| 500 | — | — | 43,8 | 0,0122 | 28,4 | 2,185 |
| 1000 | — | — | 181 | 0,0587 | 118 | 12,02 |
| 2000 | — | — | 714 | 0,1479 | 494 | 56,01 |

Conclusiones breves:

- **A** es exponencial: el número de llamadas coincide exactamente con 2·C(2n, n) − 1, y con n = 16 ya tarda más de dos minutos.
- **C** es la más simple y rápida, pero su memoria crece como n² (56 MB con n = 2000).
- **B** mantiene el tiempo O(m·n), con una constante algo mayor, y reduce la memoria a O(n) (unas 380 veces menos con n = 2000).

La memoria completa, con el análisis detallado y las gráficas, está en el PDF de la entrega.

## Referencias

- Hirschberg, D. S. (1975). *A linear space algorithm for computing maximal common subsequences.* Communications of the ACM, 18(6), 341–343.
- Cormen, Leiserson, Rivest y Stein. *Introduction to Algorithms* (capítulo de programación dinámica, LCS).
- Material de la asignatura: Temas 1, 2 y 3.
