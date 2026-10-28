# post_canonJAM — Exploración combinatoria de cadenas JAM

Carpeta de **exploración empírica** del espacio de cadenas JAM bajo la
clasificación en cuatro celdas. Aquí no hay código de producción: los
resultados son material crudo para el paper *Stacking as words* y para
guiar el diseño de Laminar.

**No requiere a Jessica.** Todo lo que hay aquí se puede verificar con
`canonJAM` + `caugjam` + Python. Lo que descubramos se le entrega servido
después.

---

## Qué se buscaba

Tres preguntas, en orden de ambición decreciente:

1. **¿La clasificación en cuatro celdas es universal?** ¿Depende de la
   opción (1–8) o solo de la estructura de palabras?
2. **¿Existe una fórmula cerrada para `|Pp(k)|`?** Y si existe, ¿es
   universal o PL-específica?
3. **¿La canonicalización de cadena `κ(a)` conmuta con la proyección a
   palabra?** Es decir, ¿es `π_k(κ(a))` el mínimo de la órbita de `π_k(a)`
   bajo `G`?

De fondo, la pregunta que guía todo:

> ¿Qué propiedades de una cadena canónica `κ(a)` son **invariantes bajo
> el grupo** `G = S₃ × ℤ/2`, y qué propiedades dependen del **tamaño
> `k`** de la cadena?

---

## Convención del sitio distinguible

La convención **`star_or_plus0`** —buscar el `*x`, si no hay buscar el
`+0`— es **S₃-equivariante para las 8 opciones** (Test 9). Las otras
convenciones fallan en algunas opciones:

| Convención | Opciones donde es S₃-equivariante |
|---|---|
| `std (+0)` | 1, 2, 3, 4, 5, 7 |
| `star (*x)` | 5, 6, 7, 8 |
| **`star_or_plus0`** | **1–8 (todas)** |
| **`rarest`** | **1–8 (todas)** |

**`star_or_plus0` es la convención canónica del paper**. Es la única
natural y estable bajo `S₃` en todo el alfabeto. Habilita el Lemma 1
(uniformidad de fibras) para todas las opciones.

---

## Hallazgos acumulados

### Test 3 — Clasificación base (opción 1, k = 2..11)

| k | órbitas | celdas | PP | Pp | pP | Ap |
|---|---|---|---|---|---|---|
| 2 | 2 | 2 | 1 | 0 | 1 | 0 |
| 3 | 4 | 3 | 1 | 0 | 2 | 1 |
| 4 | 10 | 3 | 2 | 0 | 4 | 4 |
| 5 | 25 | 3 | 1 | 0 | 8 | 16 |
| **6** | 70 | **4** | 4 | **1** | 14 | 51 |
| 7 | 196 | 3 | 1 | 0 | 26 | 169 |
| **8** | 574 | **4** | 6 | **4** | 48 | 516 |
| **9** | 1681 | **4** | 3 | **1** | 78 | 1599 |
| **10** | 5002 | **4** | 10 | **16** | 152 | 4824 |
| 11 | 14884 | 3 | 1 | 0 | 242 | 14641 |

**Hallazgo principal**: la celda **Pp** es no vacía **si y solo si** `k`
tiene un divisor propio `d ∈ [3, k/2]`. Es decir: `k` compuesto, `k ≥ 6`,
`k ≠ 4`. Se activa en `k=6` (con `AABAAB`), se desactiva en `k=7` (primo),
se reactiva en `k=8`.

**Universalidad**: las celdas no vacías son idénticas en las 4 opciones
binarias (1–4) para cada `k` testeado.

**BPL ≅ BU a nivel celda**: las opciones 2 y 3 tienen distribuciones
idénticas celda por celda para todo `k = 2..8`. Es la contrapartida
combinatoria de la Proposición 10 de `art.tex`.

### Test 5 — Refinamiento de Ramsdell (k = 2..8)

| k | periódicas | H | R | S₃P | **S₃P-only** | R-only | H-only |
|---|---|---|---|---|---|---|---|
| 2 | 1 | 1 | 0 | 1 | 0 | 0 | 0 |
| 3 | 1 | 1 | 0 | 1 | 0 | 0 | 0 |
| 4 | 2 | 1 | 0 | 2 | **1** | 0 | 0 |
| 5 | 1 | 1 | 0 | 1 | 0 | 0 | 0 |
| 6 | 5 | 2 | 1 | 4 | **1** | 0 | 0 |
| 7 | 1 | 1 | 0 | 1 | 0 | 0 | 0 |
| 8 | 10 | 2 | 0 | 6 | **4** | 0 | 0 |

**Hallazgo**:
- `H-only = 0` siempre → todo palíndromo estricto es S₃P (con σ=id).
- `S₃P-only > 0` desde k=4 → S₃P captura palabras que Ramsdell no
  clasifica como H ni R (e.g. `ABAB`, `AABBAABB`, `ABCAABCA`).
- **`R-only = 0` en todo k ≤ 8** → bajo la definición estándar de R
  (3-ciclo + rotación), `R ⊆ S₃P`. Esto **contradice** la frase del paper
  "S₃P es incomparable con R".

### Test 6 — Estabilidad de la celda bajo fibración

Las matrices de transición (padre → hijo) **no son diagonal-dominantes**.
Hay transiciones por todos lados:

- `PP → Ap` en k=7: 8 de 11 extensiones.
- `Ap → pP` en k=8: 47 transiciones.
- `Ap → PP` en k=8: 4 transiciones (sorpresa).

**La celda NO es estable bajo fibración**: padre e hijo pueden estar en
celdas distintas. Caveat importante para el paper.

### Test 7 — Densidad asintótica

| k | Ap/% |
|---|---|
| 2 | 0.00 |
| 3 | 25.00 |
| 4 | 40.00 |
| 5 | 64.00 |
| 6 | 72.86 |
| 7 | 86.22 |
| 8 | 89.90 |

**La fracción de Ap crece monótonamente**. Para k grande, casi todo cae
en Ap. La celda es un **invariante grueso** solo para k pequeño/intermedio.

### Test 8 — Mapa de definiciones de R

Probamos cinco definiciones de R:

| Definición | R\S₃P para k ≤ 8 |
|---|---|
| `R_standard` (3-ciclo + rotación) | **0** |
| `R_nontrivial` (idem, m ≥ 1) | **0** |
| `R_mirror` (σ(w) = reverse(rotᵐ(w))) | **0** |
| `R_any_sigma` (cualquier σ∈S₃ + rotación) | > 0 pero trivial (|R|=|words|) |
| `R_period_pow3` | **0** |

**Ninguna definición no trivial da R\S₃P ≠ ∅**. La incomparabilidad con R
no se sostiene bajo estas definiciones.

### Test 9 — Convenciones del sitio distinguible

`star_or_plus0` es la única convención natural S₃-equivariante para las 8
opciones. `rarest` también funciona pero es más frágil.

### Test 10 — Diagrama de Venn (H, R, S₃P, P)

Confirmado empíricamente:
- `H ⊆ S₃P` (región H·¬S siempre vacía)
- `R ⊆ S₃P` (región R·¬S siempre vacía bajo R estándar)
- La celda Pp (`¬H·¬R·¬S·P`) emerge en k=6, 8, 9, 10
- La celda Ap (`¬H·¬R·¬S·¬P`) domina desde k=3

### Test 11 + Test 13 — Fórmula cerrada para |Pp(k)|

**Confirmada para op1 (PL) hasta k = 15**, incluyendo predicciones
independientes fuera del rango de ajuste (k ≤ 12):

| k | predicho | real | estructura de k |
|---|---|---|---|
| 13 | 0 | 0 | primo |
| 14 | 169 | 169 | 2 · 7 |
| 15 | 17 | 17 | 3 · 5 |

La fórmula:

\[
|Pp(k)|_G = \sum_{d \mid k,\ 3 \le d < k} N'(d),
\qquad N'(d) = \sum_{e \mid d} \mu(d/e)\, A'(e),
\]

con \(A'(d) = |Pp(d)| + |Ap(d)|\) (número de órbitas no-S₃P de longitud \(d\)).

**Valores de N'(d) para PL**:

| d | N'(d) | d | N'(d) |
|---|---|---|---|
| 3 | 1 | 10 | 4824 |
| 4 | 4 | 11 | 14641 |
| 5 | 16 | 12 | 43988 |
| 6 | 51 | 13 | 132496 |
| 7 | 169 | 14 | 397683 |
| 8 | 516 | 15 | 1194632 |
| 9 | 1599 | | |

### Test 13 — Generalización a las 8 opciones

La fórmula PL **no es universal**: es PL-específica, porque asume
biyección palabra ↔ cadena (válido solo en op1, donde cada fila tiene
un único `+0` y los dos `+j` son indistinguibles).

**Para opciones sin buckled pairs** (op2, op3, op4, op6, op8):

\[
|Pp(k)|_{\text{op}} = |Pp(k)|_{\text{PL}} \cdot (q/3)^k
\]

Confirmada a \(k \le 9\) para op2/op3/op6 (\(q=6\), factor \(2^k\)) y
a \(k \le 6\) para op4/op8 (\(q=12\), factor \(4^k\)):

| opción | q | k=6 real | k=6 pred | k=9 real | k=9 pred |
|---|---|---|---|---|---|
| 1 (PL) | 3 | 1 | 1 | 1 | 1 |
| 2, 3, 6 | 6 | 64 | 64 | 512 | 512 |
| 4, 8 | 12 | 4096 | 4096 | — | — |

**Para opciones con buckled pairs** (op5, op7): la fórmula \((q/3)^k\)
**falla**:

| opción | k=6 real | k=6 pred \((q/3)^k\) | k=9 real | k=9 pred |
|---|---|---|---|---|
| 5 (Janus 1H) | 268 | 64 | 6400 | 512 |
| 7 (Janus 1H extendido) | 18848 | 4096 | — | — |

La causa estructural es que el par \((+x-y)\) introduce un estabilizador
bajo \(v\) (el par \((+x-x)\) es \(v\)-invariante), rompiendo la
biyección cadena ↔ palabra. La forma cerrada para op5 y op7 queda como
trabajo futuro; el límite está claramente identificado.

**Este es el resultado teórico más fuerte del proyecto**: una fórmula
cerrada, exacta, confirmada fuera de rango, y una generalización parcial
con la anomalía localizada.

**Predicciones pendientes (falsables)**:
- op1, k=16: 520
- op1, k=18: 1651
- op1, k=20: 4844
- op1, k=24: 44560
- op2/op3/op6, k=10: 16 · 2^10 = 16384

### Test 12 — Universalidad cualitativa

**Archivo**: `Test_12_universality.py`

Las **celdas no vacías** son idénticas en las 8 opciones para cada
`k ≤ 8`. Los **conteos** por celda no lo son. Ejemplo `k=6`:

| opción | PP | Pp | pP | Ap |
|---|---|---|---|---|
| 1 (PL) | 4 | 1 | 14 | 51 |
| 2 (BPL) | 128 | 64 | 504 | 3264 |
| 5 (Janus 1H) | 264 | 268 | 940 | 2488 |
| 6 (Janus 1T) | 128 | 64 | 504 | 3264 |

La universalidad es **cualitativa, no cuantitativa**. Op2 y op3 dan
exactamente los mismos conteos en todas las celdas y todos los `k`
(contrapartida de la Proposición 10 de `art.tex`).

### Test 14 — `κ` column-major ≠ `κ^word` row-major para `k ≥ 6`

Analiza la estructura de las palabras canónicas. Resultados:

- **`κ(a)` siempre empieza con `A`** (k=2..8, todas las opciones).
- **`π_k(κ(a))` es el mínimo row-major de la órbita para `k ≤ 5`, pero
  no para `k ≥ 6`**:

| k | canónicas | coinciden | divergen | % |
|---|---|---|---|---|
| 2 | 2 | 2 | 0 | 0% |
| 3 | 4 | 4 | 0 | 0% |
| 4 | 10 | 10 | 0 | 0% |
| 5 | 25 | 25 | 0 | 0% |
| 6 | 70 | 67 | 3 | 4.3% |
| 7 | 196 | 189 | 7 | 3.6% |
| 8 | 574 | 541 | 33 | 5.7% |

**No es un bug**: es una propiedad estructural de los dos órdenes.
`κ` es mínimo column-major (columna 1a, luego 1b, luego 1c);
`κ^word` es mínimo row-major (fila 1, luego fila 2, ...). Para `art.tex`
es un caveat honesto (la `κ` que se usa para filtrar no produce palabras
canónicas bajo orden lexicográfico de palabra). Para `Stacking as words`
es una línea de trabajo: `κ^word` es un objeto distinto, computable en
`O(k)` pero con técnica diferente (rotaciones, no ordenamiento de columnas).

### Test 15 — Densidad de celdas para palabras aleatorias

Si tomamos una palabra uniforme en `{A,B,C}^k`:

| k | P(PP) | P(Pp) | P(pP) | P(Ap) | P(S₃P) | P(per) |
|---|---|---|---|---|---|---|
| 2 | 0.335 | 0.000 | 0.665 | 0.000 | 1.000 | 0.335 |
| 3 | 0.112 | 0.000 | 0.443 | 0.444 | 0.556 | 0.112 |
| 4 | 0.111 | 0.000 | 0.297 | 0.592 | 0.408 | 0.111 |
| 5 | 0.012 | 0.000 | 0.197 | 0.791 | 0.209 | 0.012 |
| 6 | 0.029 | 0.016 | 0.116 | 0.839 | 0.145 | 0.045 |
| 7 | 0.002 | 0.000 | 0.072 | 0.926 | 0.074 | 0.002 |
| 8 | 0.005 | 0.008 | 0.044 | 0.944 | 0.048 | 0.012 |
| 10 | 0.001 | 0.004 | 0.016 | 0.979 | 0.017 | 0.005 |
| 12 | 0.000 | 0.001 | 0.006 | 0.993 | 0.006 | 0.001 |
| 20 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 |

**P(Ap) → 1** exponencialmente. `P(S₃P) ~ 6·3^{-⌊k/2⌋}`,
`P(per) ~ O(3^{-k/2})`. Comparado con Test 7: las celdas estructuradas
(PP, pP) aparecen sobrerrepresentadas en órbitas (porque tienen
estabilizadores grandes).

### Test 16 — Transiciones prohibidas y estado efímero

Transiciones prohibidas para `k ≤ 7`:

- `PP → Pp`
- `Pp → PP`
- `Pp → Pp`

Es decir, **`Pp` es un estado efímero**: puede aparecer como padre pero
ningún hijo de un padre `Pp` está en `Pp`.

Distribución condicional agregada (`k ≤ 7`):

| padre | PP | Pp | pP | Ap | total |
|---|---|---|---|---|---|
| PP | 0.250 | 0.000 | 0.125 | 0.625 | 24 |
| Pp | 0.000 | 0.000 | 0.167 | 0.833 | 6 |
| pP | 0.030 | 0.030 | 0.036 | 0.904 | 167 |
| Ap | 0.003 | 0.003 | 0.064 | 0.929 | 1446 |

`Ap → Ap` domina (92.9%). Todas las filas convergen a `Ap`. La matriz
**no estabiliza** entre `n` y `n+1` (4–7 de 12 entradas dentro de ±0.05).

### Estabilizadores BPL ≅ BU

Los cinco estabilizadores de las órbitas BU coinciden **exactamente** con
los de BPL (no solo hasta conjugación):

- `n=2`: `{(0,1):1, (0,):1, (0,11):1, (0,9):1, (0,7):1}` en ambas.
- `n=4`: distribuciones coinciden celda por celda.

Esto cierra la Proposición 10 de `art.tex` con verificación exhaustiva
(no solo "hasta conjugación").

---

## Qué puertas abre

### Para `Stacking as words`

1. **Un resultado teórico confirmado fuera de rango**: la fórmula de
   Möbius PL para `|Pp(k)|`, verificada hasta `k=15` con predicciones
   independientes (\(0, 169, 17\)).
2. **Una generalización parcial**: `|Pp(k)| = |Pp(k)|_PL · (q/3)^k` para
   opciones sin buckled pairs (op2, op3, op4, op6, op8), confirmada
   hasta \(k=9\).
3. **Una anomalía estructural**: op5 y op7 (con buckled pairs) rompen
   el patrón por la simetría del par \((+x-y)\). Segundo paper o
   apéndice.
4. **Un caveat honesto**: `κ` (column-major) y `κ^word` (row-major)
   divergen para `k ≥ 6`. La clasificación en celdas usa `κ^word`;
   el filtrado usa `κ`. Hay que declararlo.
5. **Una corrección al paper**: `R ⊆ S₃P`, no "incomparable con R"
   (Tests 5, 8, 10). La celda `Pp` es la que separa S₃P de Ramsdell
   sin necesidad de invocar incomparabilidad.
6. **Una caracterización de la dinámica**: `Pp` es efímero en el fibrado
   (Test 16), `Ap` domina asintóticamente (Test 7), y la distribución
   condicional no estabiliza. Eso restringe qué se puede decir de la
   augmentación canónica.

### Para Laminar

1. **`κ` column-major es el invariante correcto para filtrar**; no
   necesita cambios.
2. **La augmentación no puede usar la celda como criterio de poda**
   (Test 16: `Pp` es efímero, `Ap → Ap` domina pero no estabiliza).
3. **La distribución condicional no estabiliza** para `n ≤ 7`; Laminar
   debe computar `κ` nivel a nivel, no asumir asintótica.
4. **Las opciones sin buckled pairs tienen `|Pp(k)|` precomputable** con
   la fórmula \((q/3)^k\). Cero costo en modo exhaustivo: puedes
   predecir el tamaño de `Pp` antes de enumerar. Op5 y op7 van al modo
   muestreo antes que las demás.

### Para la comunidad de materiales 2D

- La clasificación en cuatro celdas da un **lenguaje cualitativo**
  (qué celdas son no vacías en cada `k`) que es **universal sobre las
  8 opciones**. Sirve para caracterizar polytipos sin recalcular todo.
- La fórmula PL de `|Pp(k)|` da un **conteo exacto** de un subconjunto
  no trivial de polytipos, verificable contra tablas publicadas.
- La generalización \((q/3)^k\) conecta el conteo con el tamaño del
  alfabeto y el tamaño del grupo, cerrando el círculo con Burnside.

---

## Qué significa para la augmentación canónica

La augmentación canónica (McKay) necesita tres cosas: una función padre
`π : X_{k+1} → X_k`, compatibilidad con `κ`, y una cota de complejidad.
Los resultados de esta carpeta restringen las opciones:

### 1. `π` no puede preservar celda

Test 16 muestra que `Pp` es efímero y que `PP → Pp` y `Pp → PP` están
prohibidas. Cualquier intento de definir `π` como "preservar la celda del
padre" falla en `Pp`. La función padre **tiene** que estar basada en
`κ`, no en la celda.

### 2. La compatibilidad con `v` es el punto delicado

Test 14 muestra que `κ` (column-major) y `π_k` (row-major) no conmutan
para `k ≥ 6`. Para que `π` sea compatible con `κ` bajo `v`, hay que
decidir:

- **Opción A**: definir `π` en términos de `κ` (column-major), aceptando
  que la palabra asociada puede no ser canónica.
- **Opción B**: definir `π` en términos de `κ^word` (row-major),
  cambiando la canonicalización de cadena a row-major.
- **Opción C**: mantener `κ` column-major y declarar la no-conmutación
  como caveat, sin exigir que `π` conmute con `v` en el nivel de palabra.

Mi lectura: **A** para `art.tex` (filtrado), **B** para `Stacking as
words` (clasificación de polytipos). Son dos objetos distintos y eso está
bien.

### 3. La cota de complejidad

La augmentación ingenua cuesta `O(q · m · k)` por nivel. Con los
resultados de Test 13–14, no hay razón para esperar una mejora
asintótica: la estructura de columnas del Teorema 6 de `art.tex` sirve
para `κ`, no para `π`. La augmentación se queda en `O(qmk)` por nivel
(o `O(qmk log m)` si se usa árbol balanceado en vez de hash).

### 4. El invariante de poda

Test 16 descarta la celda como invariante de poda. El invariante natural
es `κ` (completo por el Teorema 3 de `art.tex`). Otras opciones posibles:
el **estabilizador** de la órbita (Test 12 lo usa implícitamente para el
pareo BPL↔BU), o la **palabra canónica** `κ^word` si se acepta la
no-conmutación. La elección depende de qué tan fino se quiera el poda.

### 5. Lo que **no** hay que hacer

- **No** asumir que la distribución condicional estabiliza (Test 16:
  solo 4–7 de 12 entradas dentro de ±0.05).
- **No** usar la fórmula PL para otras opciones sin el factor \((q/3)^k\)
  (Test 13).
- **No** identificar `κ` con `κ^word` (Test 14: divergen desde `k=6`).

---

## Los tests

| Test | Archivo | Qué hace |
|------|---------|----------|
| **3** | `Test_3.py` | Clasificación base de opciones 1–4 en las 4 celdas. Genera la tabla de celdas no vacías. |
| **5** | `Test_5_ramsdell.py` | Clasifica las palabras periódicas por H (palíndromo estricto), R (3-fold screw), y S₃P. Mide el refinamiento de S₃P sobre Ramsdell. |
| **6** | `Test_6_fibration.py` | Matriz de transición de celdas bajo fibración. Mide si la celda es estable. |
| **7** | `Test_7_density.py` | Fracción de órbitas en cada celda para k=2..11. Mide la densidad asintótica. |
| **8** | `Test_8_mapR.py` | Prueba 5 definiciones de R y verifica si alguna da R\S₃P ≠ ∅. |
| **9** | `Test_9_conventions.py` | Verifica S₃-equivariancia de varias convenciones del sitio distinguible para las 8 opciones. |
| **10** | `Test_10_venn.py` | Diagrama de Venn de las 16 regiones de (H, R, S₃P, P). |
| **11** | `Test_11_formula.py` | Verifica la fórmula cerrada para \|Pp(k)\| vía inversión de Möbius (op1). |
| **12** | `Test_12_universality.py` | Universalidad de las celdas no vacías en las 8 opciones. |
| **13** | `Test_13_universal_formula.py` | Fórmula PL confirmada a k≤15; generalización \((q/3)^k\) para opciones sin buckled pairs. |
| **14** | `Test_14_canonical_structure.py` | Estructura de palabras canónicas: κ empieza con A; κ ≠ κ^word para k≥6. |
| **15** | `Test_15_random_words.py` | Densidad de celdas para palabras aleatorias (comparación con Test 7). |
| **16** | `Test_16_transitions.py` | Transiciones prohibidas y estado efímero del fibrado. |

---

## Qué sigue

### Tests pendientes

Ninguno obligatorio. Los cuatro tests originalmente planeados (12–16)
están hechos. Posibles extensiones:

- **Test 17** — Verificar predicciones de Test 11 para `k=16, 18, 20, 24`.
- **Test 18** — Cerrar la fórmula para op5 y op7 (buckled pairs). Requiere
  cambiar la definición de `A'(d)` para incorporar el estabilizador del
  par.
- **Test 19** — MCMC sobre el grafo de órbitas para op1. Kernel de
  transición basado en Test 16, `κ` como invariante de deduplicación.
  Verificar cobertura contra exhaustivo a `n=12–15`.

### Para el paper

`Stacking as words` puede escribirse ya con los cinco resultados
confirmados:
1. Clasificación en cuatro celdas, universal cualitativamente.
2. Fórmula PL de `|Pp(k)|`, confirmada hasta k=15.
3. Generalización \((q/3)^k\) para opciones sin buckled pairs.
4. κ column-major ≠ κ^word row-major para k≥6.
5. `Pp` efímero, `Ap` dominante, transiciones prohibidas.

El MCMC (Test 19) es para Laminar, no para el paper de combinatoria.

---

## Cómo correr

### Requisitos
- `canonJAM` instalado (`pip install -e ..` desde `caugJAM/`)
- `caugjam` instalado (`pip install -e .` desde `caugJAM/`)
- Python 3.9+, `numpy`, `pytest`

### Todos los tests de golpe

```bash
cd post_canonJAM
mkdir -p outputs
for t in Test_3 Test_5_ramsdell Test_6_fibration Test_7_density \
         Test_8_mapR Test_9_conventions Test_10_venn Test_11_formula \
         Test_12_universality Test_13_universal_formula \
         Test_14_canonical_structure Test_15_random_words \
         Test_16_transitions; do
    echo "=== $t ==="
    python3 ${t}.py 2>&1 | tee outputs/${t}_output.txt
done
```

`tee` muestra el output en pantalla **y** lo guarda en `outputs/`. Así
no hay que capturar el scrollback después.

### Tests individuales

```bash
python3 Test_13_universal_formula.py 2>&1 | tee outputs/Test_13_output.txt
```

---

## Outputs guardados

Los resultados de la corrida actual están en `outputs/`:

| Archivo | Líneas | Contenido |
|---|---|---|
| `Test_12_output.txt` | 128 | Universalidad cualitativa |
| `Test_13_output.txt` | 322 | Fórmula PL confirmada a k≤15, generalización parcial |
| `Test_14_output.txt` | 53 | κ ≠ κ^word para k≥6 |
| `Test_15_output.txt` | 36 | Densidad de palabras aleatorias |
| `Test_16_output.txt` | 45 | Transiciones prohibidas |
| `stabilizer_types_output.txt` | 9 | Estabilizadores BPL ≅ BU |
| `stabilizer_conjclasses_output.txt` | 9 | Clases de conjugación BPL ≅ BU |
| **Total** | **602** | |

Los outputs de Tests 3–11 no están guardados en `outputs/` actualmente,
pero se pueden regenerar con los comandos de arriba.

---

## Estado del proyecto

| Test | Estado |
|---|---|
| 3 | ✓ clasificación base |
| 5 | ✓ refinamiento de Ramsdell |
| 6 | ✓ estabilidad bajo fibración (negativa) |
| 7 | ✓ densidad asintótica |
| 8 | ✓ mapa de definiciones de R |
| 9 | ✓ convenciones |
| 10 | ✓ diagrama de Venn |
| 11 | ✓ fórmula PL (k≤12) |
| **12** | **✓ universalidad cualitativa** |
| **13** | **✓ fórmula PL confirmada a k≤15 + generalización \((q/3)^k\)** |
| **14** | **✓ κ ≠ κ^word para k≥6** |
| **15** | **✓ densidad de palabras aleatorias** |
| **16** | **✓ transiciones prohibidas** |

**Cinco tests nuevos cerrados, un resultado confirmado fuera de rango,
una generalización parcial con la anomalía localizada.**
