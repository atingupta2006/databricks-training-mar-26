# Day 06 — Delta Advanced Features

## Duration
4 hours

## Modules
(17) Time Travel & Table History — transaction history, DESCRIBE HISTORY, query previous versions, VERSION AS OF, TIMESTAMP AS OF; hands-on query historical data.  
(18) Delta Performance Optimization — small files problem, OPTIMIZE, ZORDER, liquid clustering, data skipping; hands-on optimize tables.

## Shared Databricks Account
- **Account**: Shared Databricks Account — Student ID
- **IDs**: u01–u16
- **Folder**: `day06-uXX`
- **Cluster**: `day06-cluster-uXX`

## Notebooks
1. [01-Day6-Time-Travel-and-Table-History.ipynb](notebooks/01-Day6-Time-Travel-and-Table-History.ipynb) — Time Travel and Change Data Capture (CDC) - Hands-on Labs
2. [02-Day6-Delta-Performance-Optimization.ipynb](notebooks/02-Day6-Delta-Performance-Optimization.ipynb) — Advanced Delta Table Optimizations and Constraints - Hands-on Labs
3. [03-Day6-Optimizing-Storage-and-Compute.ipynb](notebooks/03-Day6-Optimizing-Storage-and-Compute.ipynb) — Optimizing Storage and Compute Costs
4. [04-Day6-Adaptive-Query-Execution.ipynb](notebooks/04-Day6-Adaptive-Query-Execution.ipynb) — Adaptive Query Execution (AQE)
5. [05-Day6-Managing-Shuffles-and-Joins.ipynb](notebooks/05-Day6-Managing-Shuffles-and-Joins.ipynb) — Managing Shuffles and Broadcast Joins
6. [06-Day6-Performance-PySpark.ipynb](notebooks/06-Day6-Performance-PySpark.ipynb) — Performance PySpark
7. [07-Day6-Spark-Performance-Tuning-Joins.ipynb](notebooks/07-Day6-Spark-Performance-Tuning-Joins.ipynb) — Spark Performance Tuning Joins
8. [08-Day6-Delta-Table-Versioning.ipynb](notebooks/08-Day6-Delta-Table-Versioning.ipynb) — DeltaTableVersioning

## Prerequisites
- Complete Day 5 notebooks
- Azure Data Lake Storage mount configured
- Basic Delta Lake knowledge

## Labs Overview
### Time Travel & Table History
- Implement Time Travel to access historical data versions
- Restore data to previous states using Delta Lake
- Track and process changes using CDC techniques
- Use Structured Streaming for real-time CDC pipelines

### Delta Performance Optimization
- Performance tuning using Z-Ordering, Partitioning, and Data Skipping
- Implementing Constraints (Primary Keys, NOT NULL, Check Constraints)
- Compaction techniques (OPTIMIZE) and Storage Retention (VACUUM)
- Indexing methods like Bloom Filters and Delta Caching
- Adaptive Query Execution (AQE)
- Managing Shuffles and Broadcast Joins

## Key Concepts
- **Time Travel**: Query historical versions with VERSION AS OF / TIMESTAMP AS OF
- **DESCRIBE HISTORY**: View transaction log and changes
- **OPTIMIZE**: Compact small files and improve performance
- **ZORDER**: Cluster data for better query performance
- **Constraints**: Enforce data quality with CHECK constraints
- **AQE**: Dynamic query optimization at runtime
- **Broadcast Joins**: Optimize small table joins

## Validation Steps
- Verify Time Travel queries return correct historical data
- Check OPTIMIZE reduces file count and improves query speed
- Confirm constraints prevent invalid data insertion
- Monitor AQE plan changes in query execution

## Troubleshooting
- Ensure CDF enabled for change data feed
- Check table history for version availability
- Verify OPTIMIZE completes without errors
- Monitor cluster resources during performance tests
