# Content validation (maintainers)

Use this checklist after large edits to notebooks or handouts.

## Automated checks

```bash
# All notebooks must parse as JSON
python -c "import json, pathlib; root=pathlib.Path('hands-on');
[json.loads(p.read_text(encoding='utf-8')) for p in root.rglob('*.ipynb')];
print('OK: ipynb JSON')"

# Python helpers
python -m py_compile internal/build_day03_notebooks.py
python -m py_compile internal/build_day05_notebooks.py
```

Regenerate Day 3 notebooks after editing `internal/build_day03_notebooks.py`:

```bash
python internal/build_day03_notebooks.py
```

Regenerate Day 4 notebooks after editing `internal/build_day04_notebooks.py`:

```bash
python internal/build_day04_notebooks.py
```

Regenerate Day 5 notebooks after editing `internal/build_day05_notebooks.py`:

```bash
python internal/build_day05_notebooks.py
```

## Consistency rules (this repo)

| Topic | Expected |
|-------|-----------|
| Primary data access | **ABFS** (`abfss://...`), OAuth via **`spark.conf`**, **`%run ./02-Mount-Azure-Data-Lake`** in **every** lesson notebook that touches ADLS (see **`hands-on/README.md`**) |
| Avoid in lab paths | **`dbutils.fs.mount`**, **File Store** as the main data root, per-student **`/mnt/data-uXX`** |
| Day 1 CSV path | **`BASE_PATH + "/2010-summary.csv"`** (file under `data/2010-summary.csv`) |
| Day 1 JSON path | **`BASE_PATH + "/json/2015-summary.json"`** |
| Spark Connect | Avoid **RDD** (`.rdd`, `sc.parallelize`) in notebooks; use **DataFrame / SQL** |

## Manual spot-checks

- [ ] `hands-on/day-01/labs.md` Task 6–7 match `01-Day1-...ipynb` intro cells.
- [ ] `hands-on/day-02/instructor-README.md` matches ABFS + `%run` (not mount-only).
- [ ] `data/README.md` matches ADLS upload layout.
- [ ] Root `README.md` → `docs/unity-catalog-enabled-workspace-setup.md` link resolves.

## Runtime (Databricks)

Notebooks are **not** executed in CI; validate on a cluster with:

- Delta Lake enabled (Day 3).
- Service Principal secret set in `02-Mount-Azure-Data-Lake`.
- ADLS paths containing the flight files at the expected keys.
