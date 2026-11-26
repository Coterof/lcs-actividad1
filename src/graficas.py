import csv
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RAIZ = Path(__file__).resolve().parent.parent
CSV = RAIZ / "data" / "resultados.csv"
NOMBRES = {"A": "A: recursiva", "B": "B: Hirschberg", "C": "C: DP tabular"}
MARCAS = {"A": "o", "B": "s", "C": "^"}


def leer():
    datos = {"A": [], "B": [], "C": []}
    with open(CSV) as fh:
        for r in csv.DictReader(fh):
            if r["estado"] == "ok":
                datos[r["version"]].append({
                    "n": int(r["n"]),
                    "t": float(r["tiempo_cpu_s"]),
                    "m": float(r["memoria_pico_MB"]),
                    "ll": int(r["llamadas"]) if r["llamadas"] else None})
    return datos


def grafica(xs_ys, titulo, xlabel, ylabel, fichero):
    fig, ax = plt.subplots(figsize=(6, 4))
    for v, (xs, ys) in xs_ys.items():
        if xs:
            ax.plot(xs, ys, marker=MARCAS.get(v, "o"), label=NOMBRES.get(v, v))
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_title(titulo)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.savefig(RAIZ / "data" / fichero, dpi=200, bbox_inches="tight")
    plt.close(fig)


def main():
    d = leer()
    grafica({v: ([f["n"] for f in d[v]], [f["t"] for f in d[v]]) for v in d},
            "Tiempo de CPU frente a n", "n (longitud de cada cadena)",
            "Tiempo de CPU (s, escala log)", "grafica_tiempo.png")
    grafica({v: ([f["n"] for f in d[v]], [f["m"] for f in d[v]]) for v in d},
            "Memoria máxima frente a n", "n (longitud de cada cadena)",
            "Pico de memoria (MB, escala log)", "grafica_memoria.png")
    # Llamadas de A frente a celdas de la tabla de C (n*n)
    a = d["A"]
    grafica({"A": ([f["n"] for f in a], [f["ll"] for f in a]),
             "C": ([f["n"] for f in a], [(f["n"] + 1) ** 2 for f in a])},
            "Llamadas de A frente a celdas de C", "n",
            "Llamadas / celdas (escala log)", "grafica_llamadas.png")
    # Tabla en Markdown para copiar a la memoria
    print("| n | " + " | ".join(NOMBRES[v] + " (s / MB)" for v in "ABC") + " |")
    print("|---|---|---|---|")
    ns = sorted({f["n"] for v in d for f in d[v]})
    for n in ns:
        celdas = []
        for v in "ABC":
            f = next((x for x in d[v] if x["n"] == n), None)
            celdas.append(f"{f['t']:.4g} / {f['m']:.4g}" if f else "N/A")
        print(f"| {n} | " + " | ".join(celdas) + " |")


if __name__ == "__main__":
    main()
