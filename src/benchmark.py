import csv, json, statistics, subprocess, sys, time, tracemalloc
from pathlib import Path

from generador import generar
import lcs_recursiva, lcs_hirschberg, lcs_dp

FUNCS = {"A": lcs_recursiva.lcs_rec, "B": lcs_hirschberg.hirschberg, "C": lcs_dp.lcs_dp}
PEQUENOS = [6, 8, 10, 12, 14, 16]       # peor caso: A, B y C
GRANDES = [100, 250, 500, 1000, 2000]   # aleatorias: solo B y C
TIMEOUT = 60                            # segundos por ejecución
REPS = 3                                # repeticiones del tiempo
SALIDA = Path(__file__).resolve().parent.parent / "data" / "resultados.csv"


def worker(version, n, modo, tipo):
    """Se ejecuta en un proceso nuevo: mide una sola cosa y la imprime en JSON."""
    a, b = generar(n, tipo)
    f = FUNCS[version]
    if modo == "tiempo":
        t0 = time.process_time()
        r = f(a, b)
        valor = time.process_time() - t0            # tiempo de CPU
    else:
        tracemalloc.start()
        r = f(a, b)
        _, valor = tracemalloc.get_traced_memory()  # pico en bytes
        tracemalloc.stop()
    llamadas = lcs_recursiva.llamadas if version == "A" else None
    print(json.dumps({"valor": valor, "longitud": len(r), "llamadas": llamadas}))


def ejecutar(version, n, modo, tipo):
    try:
        out = subprocess.run(
            [sys.executable, __file__, "--worker", version, str(n), modo, tipo],
            capture_output=True, text=True, timeout=TIMEOUT, check=True)
    except subprocess.TimeoutExpired:
        return None
    return json.loads(out.stdout)


def main(rapido=False):
    peq = PEQUENOS[:3] if rapido else PEQUENOS
    gra = GRANDES[:2] if rapido else GRANDES
    plan = ([(v, n, "peor") for n in peq for v in "ABC"] +
            [(v, n, "aleatorio") for n in gra for v in "BC"])
    SALIDA.parent.mkdir(exist_ok=True)
    filas = []
    for v, n, tipo in plan:
        tiempos, r = [], None
        for _ in range(REPS):
            r = ejecutar(v, n, "tiempo", tipo)
            if r is None:
                break
            tiempos.append(r["valor"])
        m = ejecutar(v, n, "memoria", tipo) if r is not None else None
        if r is None or m is None:
            fila = [v, n, tipo, "", "", "", "", "timeout"]
        else:
            fila = [v, n, tipo, round(statistics.median(tiempos), 6),
                    round(m["valor"] / 1e6, 4), r["llamadas"] or "",
                    r["longitud"], "ok"]
        filas.append(fila)
        print(fila, flush=True)
    with open(SALIDA, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["version", "n", "tipo", "tiempo_cpu_s", "memoria_pico_MB",
                    "llamadas", "longitud_lcs", "estado"])
        w.writerows(filas)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--worker":
        worker(sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5])
    else:
        main(rapido="--rapido" in sys.argv)
