"""Ejecuta todo el proyecto con un único comando, en cualquier sistema operativo.

    python run_all.py            # tests + experimentos completos + gráficas
    python run_all.py --rapido   # versión reducida, para comprobar que todo funciona

Equivale a `make`, pero no necesita make (útil en Windows).
"""
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent


def paso(titulo, argumentos):
    print(f"\n=== {titulo} ===", flush=True)
    resultado = subprocess.run([sys.executable, *argumentos], cwd=RAIZ)
    if resultado.returncode != 0:
        print(f"\nERROR en el paso: {titulo}", file=sys.stderr)
        sys.exit(resultado.returncode)


if __name__ == "__main__":
    rapido = ["--rapido"] if "--rapido" in sys.argv else []
    paso("1/3 Tests de correccion", ["-m", "pytest", "tests", "-q"])
    paso("2/3 Experimentos (tiempo y memoria)", ["src/benchmark.py", *rapido])
    paso("3/3 Graficas y tabla de resultados", ["src/graficas.py"])
    print("\nListo. Resultados en la carpeta data/ (resultados.csv y grafica_*.png).")
