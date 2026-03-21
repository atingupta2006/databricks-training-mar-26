# Day 04 — Labs (`labs.md`)

## Theme

**Unity Catalog governance** — personal schema, **views** over shared **Day 3 Delta** paths on **ABFS**, metadata commands, **GRANT** patterns, and **lineage** discovery.

## Duration

**~5 hours** total. Suggested time boxes are indicative; the session may reorder or assign parts as homework.

| Lab | Topic | Suggested time |
|-----|--------|----------------|
| Before you start | Preconditions | 10 min |
| Lab 1 | Workspace, UC compute, ADLS | 25–35 min |
| Lab 2 | Schema + views | 60–90 min |
| Lab 3 | Metadata (`SHOW` / `DESCRIBE`) | 25–35 min |
| Lab 4 | Security & grants | 35–45 min |
| Lab 5 | Lineage & discovery | 25–35 min |
| Lab 6 | Cleanup (optional) | 10 min |

---

## How to use this document

* Work **in order** unless directed otherwise — **Lab 2** depends on **Lab 1** and **Day 3** data.
* Check off **Success criteria** as you go; they double as a **submission checklist** if required.
* Theory and diagrams: `README.md`. UC setup for admins: `docs/unity-catalog-enabled-workspace-setup.md`.

---

## Prerequisites (before Lab 1)

* [ ] **Day 3** notebooks ran successfully so **Delta** exists at (typical paths):
  * `.../data/day03/silver/flights_clean`
  * `.../data/day03/gold/flights_by_destination`
* [ ] You know your **`STUDENT_ID`** (`u01`–`u16` or as assigned).
* [ ] Workspace has **Unity Catalog** enabled and you can attach **UC-compatible** compute.
* [ ] You have access to **`02-Mount-Azure-Data-Lake.ipynb`** + **`01-Day4-Unity-Catalog-Fundamentals.ipynb`** + **`03-Day4-Unity-Catalog-Security-Lineage.ipynb`** in the **same** workspace folder (or adjusted `%run` paths).

---

## Databricks account — Student ID

| Item | Convention | Example |
|------|------------|---------|
| **Workspace folder** | `day04-uXX` | `day04-u07` |
| **Compute** | UC-compatible **cluster** or **SQL warehouse** | Per class standard |
| **Notebook variable** | `STUDENT_ID = "uXX"` | `"u07"` → schema **`main.day04_u07_lab`** |

**Important:** Use **your** ID everywhere. Duplicate **`u01`** values cause schema collisions in shared accounts.

---

# Lab 1 — Workspace, UC compute, ADLS path

## Objective

Confirm **Unity Catalog** is in use for your compute and that **`base_path`** resolves to **`abfss://.../data`** via the mount helper.

## Tasks

1. Create workspace folder **`day04-uXX`** (match your student ID).
2. Attach **Unity Catalog**–compatible compute:
   * **Cluster:** UC access mode **Shared** or **Single user** per org policy, **not** legacy “No Isolation” if UC is required.
   * **SQL warehouse:** acceptable if notebooks are written to run on warehouse (confirm with whoever runs your environment).
3. Copy into that folder:
   * **`02-Mount-Azure-Data-Lake.ipynb`**
   * **`01-Day4-Unity-Catalog-Fundamentals.ipynb`**
   * **`03-Day4-Unity-Catalog-Security-Lineage.ipynb`**
4. Either:
   * Run **`02-Mount-Azure-Data-Lake`** end-to-end (set **client secret**), **or**
   * Open **`01-Day4-...`**, run **`%run ./02-Mount-Azure-Data-Lake`**, then the **paths** cell.
5. In a scratch cell, print **`base_path`** and verify it starts with **`abfss://`** and ends with **`/data`** (or your org’s equivalent).

## Success criteria

* [ ] No OAuth / configuration errors when reading from **`base_path`**.
* [ ] You can state your **`abfss://`** prefix in one line (for your own notes).

## If you get stuck

| Symptom | Check |
|---------|--------|
| `base_path` undefined | Run **`%run ./02-Mount-Azure-Data-Lake`** first; cluster restart = re-run. |
| Secret / auth errors | **client_secret**, SP permissions on container, clock skew. |
| Wrong container | **`adlsAccountName`** / **`containerName`** in **02-Mount** match your ADLS layout. |

---

# Lab 2 — Personal schema & views over Day 3 Delta

## Objective

Create **`main.day04_uXX_lab`** and **views** **`flights_silver_v`**, **`flights_gold_v`**, and the **projection** view **`flights_silver_dest_only_v`** (destination + count only) that read **`delta.\`abfss://.../data/day03/...\``** — **without** copying data.

## Tasks

1. **Verify Day 3 paths** on ADLS (or run Day 3 notebook **01** once) so Silver and Gold Delta directories exist under your shared **`data/day03/`** tree.
2. Open **`01-Day4-Unity-Catalog-Fundamentals.ipynb`**.
3. Set **`STUDENT_ID = "uXX"`** in the designated cell (must match **your** folder suffix).
4. Run cells through:
   * **CREATE SCHEMA** (or equivalent) for **`main.day04_uXX_lab`**.
   * **CREATE VIEW** for **`flights_silver_v`** pointing at the **Silver** Delta path.
   * **CREATE VIEW** for **`flights_gold_v`** pointing at the **Gold** Delta path.
   * **CREATE VIEW** for **`flights_silver_dest_only_v`** (column minimization / governance pattern).
   * **`spark.table(...)`** cell aggregating through the projection view.
5. Run **sanity** queries: e.g. **`SELECT COUNT(*) FROM main.day04_uXX_lab.flights_silver_v`** (and Gold).
6. Open **Catalog Explorer** (left rail **Data** / **Catalog**):
   * Navigate to **`main`** → **`day04_uXX_lab`**.
   * Confirm both **views** appear.

## Success criteria

* [ ] Schema **`main.day04_uXX_lab`** exists.
* [ ] All **three** views return data (Silver full, Gold, **dest-only** projection).
* [ ] Explorer lists your schema and views under the correct **`STUDENT_ID`**.

## Deliverables (if your cohort requires them)

* Screenshot or pasted output: **Silver** and **Gold** **`COUNT(*)`**.
* One sentence: **What physical path** does **`flights_silver_v`** read from?

## If you get stuck

| Symptom | Check |
|---------|--------|
| Path not found / table not found | **`base_path`** in view definition matches **actual** Day 3 output paths; typos in `abfss://` URI. |
| `CREATE SCHEMA` permission denied | Use the catalog or schema your workspace admin provides, or ask for `CREATE SCHEMA` on `main` (or another allowed catalog). |
| 0 rows | Day 3 pipeline not run or different container/account than Day 3. |

---

# Lab 3 — Metadata commands (`SHOW` / `DESCRIBE`)

## Objective

Use SQL (or notebook cells) to **list** objects and **describe** view metadata — type, definition text, properties where shown.

## Tasks

1. In **`01-Day4-Unity-Catalog-Fundamentals.ipynb`**, locate the **Explore metadata** (or similarly named) section.
2. Run cells that:
   * **`SHOW TABLES IN main.day04_uXX_lab`**
   * **`DESCRIBE`** / **`DESCRIBE EXTENDED`** on **`flights_silver_v`** and **`flights_gold_v`**
3. In the output, identify:
   * Object **type** = **VIEW** (not **MANAGED TABLE**).
   * Any **view text** / **comment** / **properties** rows your runtime displays.
4. Run the optional **`SHOW CREATE VIEW`** cell (if supported on your DBR).

## Success criteria

* [ ] **`SHOW TABLES`** lists **all** lab views (at least **three**).
* [ ] **`DESCRIBE EXTENDED`** runs without error for at least one view.
* [ ] You can answer: **Does this object store data files on its own?** (Expected: **No** — it points to Delta paths.)

## Stretch (optional)

* Run **`SHOW CREATE VIEW`** (if supported on your DBR) and compare to the notebook’s **`CREATE VIEW`** text.
* Query **`information_schema`** snippets from notebook **03** if present.

---

# Lab 4 — Security & grants (often includes a live walkthrough)

## Objective

Understand **who** can grant access, **`SHOW GRANTS`**, and **GRANT / REVOKE** templates using **groups** (e.g. Entra ID).

## Tasks

1. Open **`03-Day4-Unity-Catalog-Security-Lineage.ipynb`**.
2. Run **`%run ./02-Mount-Azure-Data-Lake`** (if not already) and any **paths / STUDENT_ID** cells so context matches **Lab 2**.
3. Run **`SHOW GRANTS ON VIEW`** and **`SHOW GRANTS ON SCHEMA`** from notebook **03** (or SQL equivalents).
   * **Expectation:** Empty or limited rows if you are not **owner** — that is normal; a workspace owner or admin can show full grant output.
4. Run optional cells: **`information_schema.tables`** filter for your schema; **system lineage** samples — note if your role blocks them.
5. Review **SQL templates** for **`GRANT USAGE ON SCHEMA`**, **`GRANT SELECT ON VIEW`** (including **`flights_silver_dest_only_v`**), and **`REVOKE`**.
6. Discuss with the class: **least privilege**, **USAGE** on catalog/schema, **why groups beat** long user lists.

## Success criteria

* [ ] You ran **`SHOW GRANTS`** (view + schema) or saw instructor demo — understand **your** vs **admin** visibility.
* [ ] You can explain **one** reason **Entra ID groups** are preferred in **`GRANT`**.

## Stretch (optional)

* Draft (on paper) a **GRANT** plan: which group gets **SELECT** on **Gold** only vs **Silver + Gold**.

---

# Lab 5 — Lineage & discovery

## Objective

Connect **Catalog Explorer** **Lineage** (when available) to the underlying **Delta** paths under **`data/day03/`**.

## Tasks

1. In **Catalog Explorer**, open **`main.day04_uXX_lab.flights_silver_v`**.
2. Open the **Lineage** tab (or **Relationships**, depending on UI version).
3. Note **upstream** / **downstream** nodes:
   * If lineage is **sparse**, record that — views over **`delta.\`path\``** sometimes show limited graphs until jobs write through governed paths.
4. Repeat for **`flights_silver_dest_only_v`** — compare **column** coverage in the UI if shown.
5. In **`03-Day4-...`** or a SQL cell, re-run **`SHOW TABLES IN main.day04_uXX_lab`**.
6. (Optional) Open **Gold** view lineage and **compare** to Silver.

## Success criteria

* [ ] You located **Lineage** (or documented **why** it is empty).
* [ ] You can explain in your own words: **The view is UC metadata; the bytes live in ADLS Delta.**

---

# Lab 6 — Cleanup (optional)

## Objective

Drop your **personal lab schema** only if **class policy** allows (shared training accounts sometimes **keep** schemas for audit).

## Tasks

1. Confirm with the session lead **before** dropping anything.
2. If approved, in a SQL cell (replace **`uXX`**):

```sql
-- DESTRUCTIVE — only with explicit approval for your environment
-- DROP SCHEMA IF EXISTS main.day04_uXX_lab CASCADE;
```

## Success criteria

* [ ] Schema dropped **or** intentionally retained per class policy.

---

## End-of-day checklist

* [ ] **`STUDENT_ID`** correct on all notebooks you ran.
* [ ] Both views **query successfully**.
* [ ] You completed **Labs 1–3** at minimum; **4–5** as directed.
* [ ] Optional: note one **open question** for **Day 5** (Delta depth) vs **Day 4** (governance).

---

# End of Day 04 Labs

**Related:** `README.md` (theory), `hands-on/README.md` (mount pattern), Day 5 `hands-on/day-05/` (Delta labs next).
