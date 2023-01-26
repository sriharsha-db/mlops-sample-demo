# Databricks notebook source
# MAGIC %md
# MAGIC 
# MAGIC # Sample notebook

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC ## Aux steps for auto reloading of dependent files

# COMMAND ----------

# MAGIC %load_ext autoreload
# MAGIC %autoreload 2

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC ## Example usage of existing code

# COMMAND ----------

from cal_house.utils import get_zero_matric
get_zero_matric(5,3)

# COMMAND ----------

import mlflow

common_config = {"database": "sriharsha_feature_store", "table": "sklearn_housing"}
test_etl_config = {"output": common_config}

test_ml_config = {
    "input": common_config,
    "experiment": "/Shared/mlops-sample-demo"
}

try:
  _ = mlflow.create_experiment(name=test_ml_config['experiment'])
except Exception as e:
  print("Experiment already exists.", e)

# COMMAND ----------

from cal_house.tasks.sample_etl_task import SampleETLTask

etl_pipeline = SampleETLTask(spark, test_etl_config)
etl_pipeline.launch()

table_name = f"{test_etl_config['output']['database']}.{test_etl_config['output']['table']}"
spark.table(table_name).show(20)

# COMMAND ----------

from cal_house.tasks.sample_ml_task import SampleMLTask

ml_job = SampleMLTask(spark, test_ml_config)
ml_job.launch()

experiment = mlflow.get_experiment_by_name(test_ml_config['experiment'])
experiment.experiment_id
