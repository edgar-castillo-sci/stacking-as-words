# stacking-as-words

*[Read in English](README.md)*

Estructura combinatoria de las configuraciones de apilamiento en
materiales laminados de panal, representadas como cadenas JAM y
proyectadas sobre palabras en un alfabeto de tres letras `{A, B, C}`.

## Autor

Edgar Castillo (Independent Researcher)

## Base científica

Construye sobre:

> Arcudia, J., Ortiz-Chi, F., Sanchez-Valenzuela, A., Aspuru-Guzik, A.,
> Merino, G. (2023). "Joining and arrangement of multilayers: A string
> representation for honeycomb layered materials." Matter, 6(5),
> 1503–1513. doi: 10.1016/j.matt.2023.02.014

y sobre los papers de canonicalización (canonJAM) y aumentación canónica
(caugJAM) en preparación. Los resultados aquí son el material empírico
para el manuscrito *Stacking as Words: The combinatorial structure of
JAM chains* (en preparación).

## Qué hace

Cada cadena JAM se proyecta a una palabra sobre `{A, B, C}`, donde cada
letra registra el sitio de Wyckoff del token distinguido en la capa
correspondiente. Dos propiedades booleanas de la palabra —ser
**S3-palindrómica** y ser **periódica**— particionan el espacio de
órbitas en cuatro celdas:

| Celda | ¿S3-palindrómica? | ¿Periódica? |
|---|---|---|
| `PP` | sí | sí |
| `Pp` | no | sí |
| `pP` | sí | no |
| `Ap` | no | no |

Los resultados principales:

1. **Universalidad cualitativa.** Qué celdas son no vacías depende solo
   del nivel `k`, no de la opción (1–8). Verificado empíricamente.
2. **Forma cerrada para `|Pp(k)|` en PL.** Vía inversión de Möbius,
   `|Pp(k)| = Σ_{d|k, 3≤d<k} N'(d)`, confirmada para `k ≤ 15` incluyendo
   predicciones fuera de rango (`k=13 → 0`, `k=14 → 169`, `k=15 → 17`).
3. **Generalización `(q/3)^k`.** Para opciones sin buckled pairs
   (2, 3, 4, 6, 8), `|Pp(k)|_op = |Pp(k)|_PL · (q/3)^k`. Verificada
   empíricamente. Las opciones 5 y 7 (con buckled pairs) rompen el
   patrón; la obstrucción estructural está identificada.
4. **Corrección a Ramsdell.** `R ⊆ S3P`, no "incomparable con R".
5. **`κ` vs `κ^word`.** El representante canónico `κ(a)` (column-major)
   y la forma canónica de su palabra `κ^word(π(a))` (row-major) divergen
   desde `k=6` — un caveat estructural para uso downstream.

## Contenido

- `sw/` — helpers compartidos (`is_s3_palindromic`, `is_periodic`,
  `classify`, `chain_to_word`, `load_canonical`, `load_fibration`).
- `experiments/` — 13 scripts independientes, cada uno reproduce uno de
  los resultados. No son tests de pytest: se corren con `python3`.
- `tests/` — checks rápidos de pytest de los cinco claims (usados por CI).
- `outputs/` — salida capturada de los experimentos, como evidencia.
- `docs/research_notes.md` — las notas exploratorias completas (formato largo).
- `docs/roadmap.md` — roadmap de desarrollo y estado actual.

## Dependencias

`stacking-as-words` depende de [`caugJAM`](https://github.com/edgar-castillo-sci/caugJAM)
v0.1.0 (pinneado) por dos cosas:

1. **Cadenas canónicas** — `caugjam.generate_poda(option, k)` genera los
   representantes canónicos de cadenas JAM de `k` capas (usado por
   todos los experimentos excepto `exp15_random_words.py`).
2. **Datos de fibración** — `caugJAM/scripts/fibration.py` genera las
   tablas padre→hijo usadas por `exp06` y `exp16`.

Las cadenas canónicas se cachean en `data/` (gitignored), así que se
generan una vez y se reutilizan. Los datos de fibración **no** se
auto-generan por este paquete: copia los `.tsv` de
`caugJAM/scripts/fibration.py`, o apunta `$SW_DATA_DIR` a un directorio
que los contenga.

Si `caugjam` no está instalado:
- `exp15_random_words.py` sigue funcionando (combinatoria pura).
- Los demás experimentos fallan con `ModuleNotFoundError` cuando
  intentan regenerar una caché faltante.

Dependencias transitivas: `canonjam` (traída por `caugjam`) y `numpy`
(traída por ambos).

## Instalación

Requiere `caugjam` v0.1.0 o superior:

```bash
pip install "caugjam @ git+https://github.com/edgar-castillo-sci/caugJAM.git@v0.1.0"
pip install -e ".[tests]"
```

## Ejecución rápida

```bash
# Suite de CI rápida (~5 segundos)
pytest -v

# Experimentos completos (minutos)
python3 experiments/exp13_generalized_formula.py
python3 experiments/exp14_canonical_structure.py
```

## Datos

Salidas grandes regenerables (`data/**/canonicas.txt`, fibration `.tsv`)
**no se versionan**. Se regeneran a demanda con `caugjam.generate_poda`,
o se proveen vía la variable de entorno `$SW_DATA_DIR`. Las salidas
capturadas de los experimentos (`outputs/*.txt`) sí se versionan como
evidencia.

## Procedencia de los datos

`data/summary/*.tsv` contiene evidencia versionada de los resultados del
paper (conteos por celda por nivel y opción, y `N'(d)` para PL). Estos
archivos se generaron con **caugJAM v0.1.0**
(doi:10.5281/zenodo.23721460) y se verificaron contra el método completo
de **canonJAM v1.2.1** (doi:10.5281/zenodo.23720668) en cada nivel.

Para auditar los datos sin instalar caugJAM:

```bash
python3 experiments/verify_data.py
```

Esto carga los `.tsv` versionados y los compara contra los valores
esperados del paper (rápido: < 1 s). Para recomputarlos desde cero con
caugJAM:

```bash
python3 experiments/verify_data.py --regenerate
```

La cadena de procedencia es: **canonJAM** (definición de `κ`) →
**caugJAM** (generador) → `data/summary/*.tsv` (evidencia archivada) →
`verify_data.py` (verificación independiente). Ver `data/README.md`
para detalles.

## Citación

```bibtex
@software{stacking_as_words,
  author       = {Castillo, Edgar},
  title        = {{stacking-as-words: Combinatorial structure of JAM chains}},
  year         = {2026},
  publisher    = {Zenodo},
  howpublished = {\url{https://github.com/edgar-castillo-sci/stacking-as-words}},
  note         = {DOI to be assigned}
}
```

## Licencia

MIT (ver `LICENSE`).
