# Se utiliza el SAT solver Z3.
# Si no lo tiene instalado utilice: pip install z3-solver.
from z3 import Bool, Solver, Implies, sat


# Declaración de variables proposicionales para los colores de los países.
azul = [Bool(f"C_{i}_A") for i in range(13)]
rojo = [Bool(f"C_{i}_R") for i in range(13)]
verde = [Bool(f"C_{i}_V") for i in range(13)]

# Declaración de variables proposicionales para indicar países limítrofes.
limitrofe = [
    [Bool(f"L_{i}_{j}") if i < j else None for j in range(13)]
    for i in range(13)
]

solver = Solver()

# A cada país se le tiene que asignar un único color.
for i in range(13):
    solver.add(
        (azul[i] | rojo[i] | verde[i]) &
        (~azul[i] | ~rojo[i]) &
        (~azul[i] | ~verde[i]) &
        (~rojo[i] | ~verde[i])
    )

# Dos países limítrofes no puedes tener el mismo color.
for i in range(13):
    for j in range(i+1, 13):
        solver.add(
            Implies(limitrofe[i][j], ~(azul[i] & azul[j])) &
            Implies(limitrofe[i][j], ~(rojo[i] & rojo[j])) &
            Implies(limitrofe[i][j], ~(verde[i] & verde[j]))
        )

# Las fronteras en América del Sur.
# 0 : Perú
# 1 : Chile
# 2 : Argentina
# 3 : Ecuador
# 4 : Bolivia
# 5 : Uruguay
# 6 : Paraguay
# 7 : Guyana
# 8 : Surinam
# 9 : Guayana Francesa
# 10 : Venezuela
# 11 : Brasil
# 12 : Colombia
solver.add(
    limitrofe[0][1] &
    limitrofe[0][3] &
    limitrofe[0][4] &
    limitrofe[0][11] &
    limitrofe[0][12] &
    limitrofe[1][2] &
    limitrofe[1][4] &
    limitrofe[2][4] &
    limitrofe[2][5] &
    limitrofe[2][6] &
    limitrofe[3][12] &
    limitrofe[4][6] &
    limitrofe[4][11] &
    limitrofe[5][11] &
    limitrofe[6][11] &
    limitrofe[7][8] &
    limitrofe[7][10] &
    limitrofe[7][11] &
    limitrofe[8][9] &
    limitrofe[8][11] &
    limitrofe[9][11] &
    limitrofe[10][11] &
    limitrofe[10][12] &
    limitrofe[11][12]
)

# Verificación de la 3-coloración del mapa.
if solver.check() == sat:
    modelo = solver.model()
    verdaderas = [v for v in modelo if modelo[v] == True and str(v)[0] != "L"]
    print(f"Coloración del mapa: {verdaderas}")
else:
    print("El mapa no se puede pintar con tres colores")