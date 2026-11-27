import time
from generador import generar_par, generar_peor_caso
import lcs_recursiva as R

for n in (16, 18):
    a, b = generar_par(n)
    t = time.process_time(); r = R.lcs_rec(a, b)
    print(f"aleatorio n={n}: {R.llamadas} llamadas, LCS={len(r)}, {time.process_time()-t:.1f} s")

a, b = generar_peor_caso(16)   # tarda ~2 min
t = time.process_time(); R.lcs_rec(a, b)
print(f"peor caso n=16: {R.llamadas} llamadas, {time.process_time()-t:.0f} s")
