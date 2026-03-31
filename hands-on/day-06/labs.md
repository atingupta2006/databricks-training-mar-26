# Day 06 — Delta Advanced Features — Labs

Aligned with Day 6 in the course outline (items 17 and 18).

If you are short on time: finish **01** through Lab 2, and **02** through Lab 1. Labs marked optional can wait.

---

## Paths

First cell in each notebook:

```python
BASE_PATH = "abfss://atininput@sadbtrng19032026.dfs.core.windows.net/data/"
STUDENT_ID = "u25"  # your assigned id
DAY5 = BASE_PATH + "/day5"
P_BASIC = DAY5 + "/delta/flight_summary_basic"
DAY6_PREFIX = f"{BASE_PATH}day06-{STUDENT_ID}"
```

You need `P_BASIC` from Day 5 notebook 01. Day 6 writes under `day06-{STUDENT_ID}`.

---

## Lab 1: Time travel (item 17)

**Notebook:** `01-Day6-Time-Travel-and-Table-History.ipynb`

**Goal:** Use table history and read older versions (`versionAsOf` / `timestampAsOf`, or SQL `VERSION AS OF` / `TIMESTAMP AS OF`).

### Task 1.1: Setup

1. Set `STUDENT_ID`, run the prerequisite check.
2. Create a small Delta table under `DAY6_PREFIX`.

```python
data = [(101, 5000, "2024-02-01"), (102, 7000, "2024-02-02"), (103, 4500, "2024-02-03")]
columns = ["transaction_id", "amount", "transaction_date"]
df = spark.createDataFrame(data, columns)
df.write.format("delta").mode("overwrite").save(f"{DAY6_PREFIX}/transactions")
```

### Task 1.2: History

Update or append, then `DESCRIBE HISTORY` on the path.

### Task 1.3: Time travel

Read a known older version; optionally use a timestamp.

### Task 1.4: Restore

Use `restoreToVersion` if you cover it in the slides.

Change data feed and streaming belong on Day 7 (item 19).

---

## Lab 2: Delta performance (item 18)

**Notebook:** `02-Day6-Delta-Performance-Optimization.ipynb`

**Goal:** OPTIMIZE and ZORDER; liquid clustering and data skipping in lecture.

### Core

Create sample Delta data, run `OPTIMIZE ... ZORDER BY`, inspect the plan (`EXPLAIN`).

### Optional in the same notebook

Partitioned `loan_foreclosures`, CHECK constraint, VACUUM, Bloom table property. Omit if you stay on the minimum outline.

---

## Lab 3: Extra (not in items 17–18)

1. [03-Day6-Optional-5min-Teaser.ipynb](notebooks/03-Day6-Optional-5min-Teaser.ipynb)
2. [notebooks/_archive/](notebooks/_archive/) — older long labs

---

## Validation

- Item 17: history and time travel work on student paths.
- Item 18: OPTIMIZE (and ZORDER if used) completes.

## Common problems

- Wrong `STUDENT_ID` or missing `P_BASIC`.
- No write permission to `DAY6_PREFIX`.
- Wrong version id — use `DESCRIBE HISTORY` first.

## References

- [Delta time travel](https://docs.databricks.com/delta/delta-time-travel.html)
- [OPTIMIZE](https://docs.databricks.com/delta/delta-optimize.html)
- [Z-order](https://docs.databricks.com/delta/data-skipping.html#z-ordering-for-lakehouse-queries)
- [Liquid clustering](https://docs.databricks.com/delta/clustering.html)
