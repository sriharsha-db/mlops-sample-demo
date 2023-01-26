import os
import json
import requests
import base64

from databricks_cli.sdk.api_client import ApiClient
from databricks_cli.jobs.api import JobsApi
from databricks_cli.runs.api import RunsApi

api_client = ApiClient(
  host  = os.getenv('DATABRICKS_HOST'),
  token = os.getenv('DATABRICKS_TOKEN')
)
jobs_api = JobsApi(api_client)
runs_api = RunsApi(api_client)

file_dir="scripts/cicd"
for file_name in os.listdir(file_dir):
    if file_name.endswith("job.json"):
        print(f"Job update for {file_name}")
        with open(os.path.join(file_dir, file_name)) as json_file:
          req_json = json.load(json_file)
          existing_jobs = jobs_api._list_jobs_by_name(req_json['name'])
          if len(existing_jobs) == 1:
            job_id = existing_jobs[0]['job_id']
            jobs_api.delete_job(job_id)
            print(f"deleting the existing job {job_id} and creating a new one")
          
          job_create_resp = jobs_api.create_job(req_json)
          print("created a new job with details -",job_create_resp)

          jobs_api.run_now(job_id=job_create_resp['job_id'], notebook_params=None, 
          python_named_params=None, python_params=None, spark_submit_params=None, jar_params=None)