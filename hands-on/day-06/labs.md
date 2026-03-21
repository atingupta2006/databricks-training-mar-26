# Day 06 — Delta Advanced Features — Labs

## Shared Databricks Account
- **Account**: Shared Databricks Account — Use Your Student ID
- **Student IDs**: u01–u16
- **Workspace Folder**: `day06-uXX` (replace XX with your student ID)
- **Cluster**: `day06-cluster-uXX` (pre-configured for each student)

## Lab 1: Time Travel and Table History

### Objective
Learn to query historical versions of Delta tables using Time Travel and explore transaction history.

### Prerequisites
- Day 5 notebooks completed
- Azure Data Lake Storage mount configured

### Tasks

#### Task 1.1: Setup and Initial Data Load
1. Open `01-Day6-Time-Travel-and-Table-History.ipynb`
2. Update `STUDENT_ID` to your assigned ID (u01-u16)
3. Run the prerequisite check to ensure Day 5 tables exist
4. Create a transactions table with sample data

```python
# Expected code structure
data = [(101, 5000, "2024-02-01"), (102, 7000, "2024-02-02"), (103, 4500, "2024-02-03")]
columns = ["transaction_id", "amount", "transaction_date"]
df = spark.createDataFrame(data, columns)
df.write.format("delta").mode("overwrite").save(f"abfss://shared@dbstorage.dfs.core.windows.net/day06-u{STUDENT_ID}/transactions")
```

**Success Criteria**: Table created successfully with 3 records.

#### Task 1.2: Update Data and Check History
1. Update a transaction record
2. Run `DESCRIBE HISTORY` to view transaction log

```python
from delta.tables import DeltaTable

delta_table = DeltaTable.forPath(spark, f"abfss://shared@dbstorage.dfs.core.windows.net/day06-u{STUDENT_ID}/transactions")
delta_table.update("transaction_id = 101", {"amount": "6000"})

# Check history
spark.sql(f"DESCRIBE HISTORY delta.`abfss://shared@dbstorage.dfs.core.windows.net/day06-u{STUDENT_ID}/transactions`").show()
```

**Success Criteria**: History shows 2 versions (0 and 1).

#### Task 1.3: Time Travel Queries
1. Query the original version (version 0)
2. Query using timestamp

```python
# Query version 0
original_df = spark.read.format("delta").option("versionAsOf", 0).load(f"abfss://shared@dbstorage.dfs.core.windows.net/day06-u{STUDENT_ID}/transactions")
original_df.show()

# Query using timestamp (adjust timestamp as needed)
timestamp_df = spark.read.format("delta").option("timestampAsOf", "2024-01-01 00:00:00").load(f"abfss://shared@dbstorage.dfs.core.windows.net/day06-u{STUDENT_ID}/transactions")
timestamp_df.show()
```

**Success Criteria**: Original data shows amount 5000 for transaction 101.

#### Task 1.4: Restore to Previous Version
1. Restore the table to version 0
2. Verify the restoration

```python
delta_table.restoreToVersion(0)

# Verify
restored_df = spark.read.format("delta").load(f"abfss://shared@dbstorage.dfs.core.windows.net/day06-u{STUDENT_ID}/transactions")
restored_df.show()
```

**Success Criteria**: Data restored to original values.

## Lab 2: Delta Performance Optimization

### Objective
Optimize Delta tables for better query performance using OPTIMIZE, ZORDER, and constraints.

### Tasks

#### Task 2.1: Z-Ordering for Query Performance
1. Open `02-Day6-Delta-Performance-Optimization.ipynb`
2. Create a bank transactions table
3. Apply Z-Ordering on customer_id

```python
# Create table with sample data
data = [(101, "C001", 5000, "2024-01-01"), (102, "C002", 7000, "2024-01-02")]
columns = ["transaction_id", "customer_id", "amount", "transaction_date"]
df = spark.createDataFrame(data, columns)
df.write.format("delta").mode("overwrite").save(f"abfss://shared@dbstorage.dfs.core.windows.net/day06-u{STUDENT_ID}/bank_transactions")

# Apply Z-Ordering
spark.sql(f"OPTIMIZE delta.`abfss://shared@dbstorage.dfs.core.windows.net/day06-u{STUDENT_ID}/bank_transactions` ZORDER BY (customer_id)")
```

**Success Criteria**: OPTIMIZE command completes successfully.

#### Task 2.2: Add Constraints
1. Add a check constraint to ensure amount >= 0

```python
spark.sql(f"ALTER TABLE delta.`abfss://shared@dbstorage.dfs.core.windows.net/day06-u{STUDENT_ID}/bank_transactions` ADD CONSTRAINT amt_nonneg CHECK (amount >= 0)")
```

**Success Criteria**: Constraint added without errors.

#### Task 2.3: Test Constraint Validation
1. Try to insert invalid data (negative amount)
2. Verify the constraint prevents invalid data

```python
# This should fail
try:
    invalid_df = spark.createDataFrame([(104, "C003", -1000, "2024-01-04")], columns)
    invalid_df.write.format("delta").mode("append").save(f"abfss://shared@dbstorage.dfs.core.windows.net/day06-u{STUDENT_ID}/bank_transactions")
except Exception as e:
    print(f"Expected error: {e}")
```

**Success Criteria**: Insert fails with constraint violation error.

#### Task 2.4: Partitioned Tables
1. Create a partitioned table for loan data
2. Load data and verify partitioning

```python
spark.sql(f"""
CREATE TABLE loan_foreclosures (
    loan_id STRING,
    customer_id STRING,
    outstanding_balance DOUBLE,
    foreclosure_date DATE
) USING DELTA
PARTITIONED BY (foreclosure_date)
LOCATION 'abfss://shared@dbstorage.dfs.core.windows.net/day06-u{STUDENT_ID}/loan_foreclosures'
""")

# Insert sample data
loan_data = [("L001", "C001", 100000.0, "2024-01-01")]
loan_df = spark.createDataFrame(loan_data, ["loan_id", "customer_id", "outstanding_balance", "foreclosure_date"])
loan_df.write.insertInto("loan_foreclosures")
```

**Success Criteria**: Data inserted and partitioned correctly.

## Lab 3: Advanced Performance Tuning

### Objective
Explore additional optimization techniques including AQE, broadcast joins, and storage optimization.

### Tasks

#### Task 3.1: Adaptive Query Execution
1. Open `04-Day6-Adaptive-Query-Execution.ipynb`
2. Enable AQE and observe query plan changes

```python
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
```

**Success Criteria**: AQE settings configured.

#### Task 3.2: Broadcast Joins
1. Open `05-Day6-Managing-Shuffles-and-Joins.ipynb`
2. Create small and large tables
3. Force broadcast join and observe performance

```python
# Hint for broadcast
df1.join(df2.hint("broadcast"), "join_column")
```

**Success Criteria**: Join uses broadcast strategy.

#### Task 3.3: Storage Optimization
1. Open `03-Day6-Optimizing-Storage-and-Compute.ipynb`
2. Analyze storage costs and optimization strategies

**Success Criteria**: Understanding of storage optimization concepts.

## Validation and Success Criteria

### Overall Success Criteria
- All notebooks run without critical errors
- Time travel queries return correct historical data
- OPTIMIZE commands complete successfully
- Constraints prevent invalid data insertion
- Performance optimizations show measurable improvements

### Common Issues
- **Path Errors**: Ensure STUDENT_ID is correctly set
- **Permission Errors**: Check Azure storage access
- **Version Errors**: Verify available versions with DESCRIBE HISTORY
- **Constraint Errors**: Drop existing constraints before re-adding

### Performance Validation
- Compare query execution times before/after optimization
- Check file counts using `DESCRIBE DETAIL`
- Monitor cluster metrics during optimization operations

## Additional Resources
- [Delta Time Travel Documentation](https://docs.databricks.com/delta/delta-time-travel.html)
- [Delta Optimize Guide](https://docs.databricks.com/delta/delta-optimize.html)
- [Delta Constraints](https://docs.databricks.com/delta/delta-constraints.html)
