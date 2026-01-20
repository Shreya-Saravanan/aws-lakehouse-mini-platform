import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col, to_timestamp, to_date

# Resolve job arguments
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# ---------- READ RAW DATA ----------
customers = spark.read.option("header", "true").csv(
    "s3://shreya-finance-lakehouse-raw-2026/raw/customers/"
)

accounts = spark.read.option("header", "true").csv(
    "s3://shreya-finance-lakehouse-raw-2026/raw/accounts/"
)

transactions = spark.read.option("header", "true").csv(
    "s3://shreya-finance-lakehouse-raw-2026/raw/transactions/"
)

# ---------- CLEAN & TYPE ----------
transactions_clean = transactions \
    .withColumn("amount", col("amount").cast("double")) \
    .withColumn("transaction_ts", to_timestamp(col("transaction_ts"), "yyyy-MM-dd'T'HH:mm:ss")
    ) \
    .withColumn("transaction_date", to_date(col("transaction_ts"))
    )
    
accounts_clean = accounts.withColumn("balance", col("balance").cast("double"))

customers_clean = customers.withColumn("credit_score",col("credit_score").cast("int"))

# ---------- WRITE CURATED ----------
customers_clean.write.mode("overwrite").parquet(
    "s3://shreya-finance-lakehouse-raw-2026/curated/customers/"
)

accounts_clean.write.mode("overwrite").parquet(
    "s3://shreya-finance-lakehouse-raw-2026/curated/accounts/"
)

transactions_clean.write \
    .mode("overwrite") \
    .partitionBy("transaction_date") \
    .parquet(
    "s3://shreya-finance-lakehouse-raw-2026/curated/transactions/"
)

job.commit()