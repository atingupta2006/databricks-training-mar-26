# Unity Catalog–Enabled Databricks Workspace — Setup Guide

This document explains how to **enable and use Unity Catalog (UC)** with a Databricks workspace, with emphasis on **Microsoft Azure** (aligned with this course’s **Azure Databricks + ADLS Gen2** pattern). Concepts apply similarly on **AWS** and **GCP** with different storage and identity primitives.

> **Note:** Databricks product UIs and exact menu names change over time. Always cross-check with **[Databricks Unity Catalog documentation](https://docs.databricks.com/en/data-governance/unity-catalog/index.html)** for your workspace version.

---

## 1. What you are enabling

**Unity Catalog** is Databricks’ **centralized governance layer** for data and AI assets:

- **Metastore** — top-level container; holds metadata for catalogs, schemas (databases), tables, volumes, etc.
- **Catalog** — top-level namespace (often one per domain or environment: `prod`, `dev`, `finance`).
- **Schema** — grouping of tables/views within a catalog (similar to a “database”).
- **Managed vs external tables** — managed storage under UC-managed locations vs your cloud storage (ADLS/S3/GCS) via **external locations**.

Enabling UC means: your workspace is **assigned to a Unity Catalog metastore**, identities can be granted **fine-grained privileges**, and objects are discoverable in **Catalog** explorer and SQL.

---

## 2. Prerequisites and decisions

### 2.1 Subscription and product SKU

- Workspaces that use Unity Catalog typically require a **Databricks plan that includes UC** (commonly **Premium** or equivalent; confirm with your Databricks account team or Azure Marketplace offering).
- You need permission to:
  - Create or manage the **Databricks account** (account console).
  - Create **Azure resources** (storage account, optionally Key Vault).
  - Assign **Azure AD** users/groups to Databricks.

### 2.2 Identity model

- **Users and groups** are usually synchronized from **Azure Entra ID (Azure AD)** via **SCIM** or invited as workspace users.
- **Service principals** and **managed identities** are used for **machine** access (jobs, clusters, storage access connectors).

Decide early:

| Question | Typical choice |
|----------|----------------|
| One metastore per region or shared? | Often **one metastore per region** for that cloud account. |
| Storage for metastore root? | Dedicated **ADLS Gen2** container (isolated from ad-hoc lab data). |
| Who is **metastore admin**? | Small set of platform admins (not all data engineers). |

### 2.3 Network (optional but important)

- If storage uses **firewalls** or **private endpoints**, plan **private connectivity** (e.g. Azure Private Link) between Databricks and storage **before** cutting over production workloads.

---

## 3. High-level flow (Azure)

1. **Databricks account admin** opens the **Account Console** (not the workspace UI).
2. **Create a Unity Catalog metastore** (one per supported region as needed).
3. Configure **metastore storage** (ADLS Gen2) and **Azure access** (**managed identity** / access connector).
4. **Assign your workspace(s)** to that metastore.
5. In the workspace, create **catalogs**, **schemas**, **external locations** (and **storage credentials**), then **GRANT** privileges to users/groups.
6. **Validate** with `SHOW CATALOGS`, `CREATE TABLE`, and Catalog UI.

---

## 4. Step-by-step: Account console and metastore (Azure)

> Exact clicks: **Account Console → Data → Metastores** (or **Unity Catalog**), then **Create metastore**.

### 4.1 Create or identify ADLS Gen2 for the metastore

1. In **Azure Portal**, create (or use) a **Storage account** with **hierarchical namespace enabled** (Gen2).
2. Create a **container** dedicated to UC metastore root (e.g. `uc-metastore-root`).  
   - Restrict access; this holds UC **internal** metadata and managed assets depending on configuration.
3. Note:
   - **Storage account name**
   - **Container name**
   - **Subscription / resource group**

### 4.2 Create the metastore in Databricks Account Console

1. Sign in to **[Databricks Account Console](https://accounts.cloud.databricks.com/)** as **account admin** (or role that can manage metastores).
2. Navigate to **Metastores** / **Unity Catalog** setup.
3. Choose **region** (must match where your workspace will attach, per Databricks rules for that cloud).
4. Provide:
   - **Metastore name** (e.g. `uc-metastore-eastus`).
   - **ADLS Gen2** root path, typically:  
     `abfss://<container>@<storageaccount>.dfs.core.windows.net/<optional-prefix>`
5. Complete the **Azure access** setup:
   - Databricks will guide you to create or use an **Azure Databricks Access Connector** (managed identity) and grant that identity **appropriate RBAC on the storage account** (e.g. **Storage Blob Data Contributor** on the container or scoped path — follow the **official wizard**, as least-privilege templates evolve).

### 4.3 Assign the workspace to the metastore

1. In Account Console, open the metastore → **Workspaces** (or **Assign workspace**).
2. **Assign** your training or production workspace.
3. Confirm the workspace **default catalog** behavior (Databricks may set **`main`** or workspace defaults; you can adjust policies later).

**Important:** Until a workspace is assigned to a metastore, it **cannot** fully use Unity Catalog objects as the primary governance model (legacy Hive metastore may still exist for older assets — migration is a separate topic).

---

## 5. Workspace-side setup (after metastore assignment)

Open the **Databricks workspace** (not Account Console).

### 5.1 Confirm Unity Catalog is active

- Open **Catalog** (left sidebar) or **Data** → **Catalog**.
- You should see at least the **`main`** catalog (and possibly **`samples`**).

Run in a SQL warehouse or notebook (SQL cell):

```sql
SHOW CATALOGS;
```

### 5.2 Create a catalog and schema (example)

Replace names with your organization’s conventions.

```sql
CREATE CATALOG IF NOT EXISTS training_dev;
CREATE SCHEMA IF NOT EXISTS training_dev.silver;
```

### 5.3 External locations and storage credentials (ADLS)

To register **tables on ADLS** paths (like this course’s `abfss://.../data/...`):

1. **Storage credential** — links Databricks to your cloud vault / identity for that storage.
   - Azure: often **Azure service principal** or **managed identity** via **credential** object in UC.
2. **External location** — UC object pointing to a **URL prefix** (e.g. `abfss://container@account.dfs.core.windows.net/data/`).
3. **Grant** `CREATE EXTERNAL TABLE` (and related) on that location to the right groups.

> **Security:** Prefer **narrow paths** (one external location per environment or domain), not the entire storage account root, unless policy requires otherwise.

Typical SQL pattern (illustrative — parameter names depend on how you created the credential in UI):

```sql
-- Example only; credential name must exist in your workspace
CREATE EXTERNAL LOCATION IF NOT EXISTS training_adls_data
  URL 'abfss://<container>@<storage>.dfs.core.windows.net/data/'
  WITH (STORAGE CREDENTIAL `<your_storage_credential_name>`);

GRANT READ FILES, WRITE FILES ON EXTERNAL LOCATION `training_adls_data` TO `<group_or_principal>`;
```

*(Exact `GRANT` syntax and privileges vary by Databricks version; use the in-product privilege reference.)*

### 5.4 Create an external table on ABFS (example)

After grants are correct:

```sql
CREATE TABLE training_dev.silver.flights
USING DELTA
LOCATION 'abfss://<container>@<storage>.dfs.core.windows.net/data/day03/silver/flights_clean';
```

Or use **managed tables** in a **managed storage location** configured for that catalog (organization-dependent).

---

## 6. Access control (who can see what)

### 6.1 Prefer groups over individuals

- In **Account Console** / **Workspace**: sync **Entra ID groups** (e.g. `uc-data-engineers`, `uc-analysts-readonly`).
- **Grant** at **catalog**, **schema**, **table**, or **external location** level.

Examples (illustrative):

```sql
GRANT USE CATALOG ON CATALOG training_dev TO `data-engineers`;
GRANT USE SCHEMA ON SCHEMA training_dev.silver TO `data-engineers`;
GRANT SELECT ON TABLE training_dev.silver.flights TO `analysts-readonly`;
```

### 6.2 Service principals for jobs

- Register an **Entra ID enterprise application** (service principal).
- Add it to Databricks **account** / **workspace** per your admin model.
- Grant **minimum** UC privileges for the job’s tables and locations.

### 6.3 Clusters / SQL warehouses

- **Access mode** must be **UC-compatible** (e.g. **Shared** with UC, **Single user** for some SP scenarios — see current Databricks docs for your runtime).
- **Personal access tokens** and legacy table ACLs behave differently under UC; standardize on **UC grants**.

---

## 7. Verification checklist

| Check | How |
|-------|-----|
| Metastore attached | Account Console shows workspace under metastore. |
| Catalog visible | `SHOW CATALOGS` in SQL. |
| Can create schema | `CREATE SCHEMA` succeeds. |
| External location works | `DESCRIBE EXTERNAL LOCATION` or create test external table. |
| Least privilege | Test as a **non-admin** user with only the expected grants. |
| Lineage / explorer | Table appears in **Catalog** UI with correct owner and permissions. |

---

## 8. Common issues and fixes

| Symptom | Likely cause | Direction |
|--------|----------------|-----------|
| `PERMISSION_DENIED` on ABFS | External location / credential / RBAC on storage | Fix **storage credential**, **external location** grants, and Azure **IAM** on the path. |
| Workspace not in metastore | Not assigned in Account Console | Assign workspace to metastore. |
| Cannot use UC on cluster | Wrong **access mode** or old cluster policy | Create **UC-compatible** cluster / SQL warehouse. |
| `main` only, cannot create catalog | Missing **metastore admin** or account-level restriction | Metastore admin must create catalog or delegate `CREATE CATALOG`. |
| Hive metastore vs UC confusion | Legacy `hive_metastore` catalog still visible | Plan **migration**; new work should target **UC catalogs**. |

---

## 9. Relation to this training (ABFS labs)

This course’s notebooks often use **`spark.conf` OAuth** and **`abfss://`** paths **without** registering UC objects. That is valid for **learning** and **ADLS access**.

**Production / Day 4+ governance** typically adds:

- **External locations** + **storage credentials** for those same ABFS prefixes.
- **Catalog/schema** for **`training_dev.silver.*`** instead of only path-based writes.
- **Grants** to groups and service principals.

You can **keep the same physical Delta files** and **register** them in UC via `CREATE TABLE ... LOCATION 'abfss://...'` once permissions exist.

---

## 10. Official references (keep bookmarked)

- [Unity Catalog overview](https://docs.databricks.com/en/data-governance/unity-catalog/index.html)
- [Get started — enable Unity Catalog](https://docs.databricks.com/en/data-governance/unity-catalog/get-started.html) *(title may vary slightly by doc revision)*
- [Azure — Unity Catalog](https://docs.databricks.com/en/administration-guide/account-settings-e2/azure-unity-catalog.html) *(Azure-specific metastore and connector steps)*
- [External locations](https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-ddl-create-external-location.html)
- [Storage credentials](https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-ddl-create-storage-credential.html)

---

## 11. Summary

1. **Account admin** creates **Unity Catalog metastore** backed by **ADLS Gen2** and **Azure access connector / managed identity**.
2. **Assign** the **workspace** to the metastore.
3. In the workspace, define **storage credentials** → **external locations** → **catalogs/schemas** → **grants**.
4. Use **UC-compatible** compute and validate with **SQL** and the **Catalog** UI.

For organizational rollout, add **naming standards**, **environment separation** (dev/test/prod catalogs), and **auditing** (audit logs, lineage) as separate workstreams.

---

*Training reference document — not a substitute for your organization’s security review or Databricks support.*
