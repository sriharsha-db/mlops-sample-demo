import os
import json
from argparse import ArgumentParser
from databricks_cli.sdk.api_client import ApiClient
from databricks_cli.jobs.api import JobsApi
from databricks_cli.runs.api import RunsApi

class UpdateDatabricksJobs():
  '''
  Class to handle the databricks jobs updates as part of CICD process
  '''
  def __init__(self) -> None:
    api_client = ApiClient(
      host  = os.getenv('DATABRICKS_HOST'),
      token = os.getenv('DATABRICKS_TOKEN')
    )
    self.jobs_api = JobsApi(api_client)
    self.runs_api = RunsApi(api_client)

    self.reset_json_template = {"new_settings":{}}
    self.run_now = None

    self.parser = ArgumentParser()
    self.parser.add_argument("env")
    self.parser.add_argument('tag_branch')
    self.parser.add_argument('git_ref')

  def parse_args(self) -> None:
    args = self.parser.parse_args()
    self.git_ref = args.git_ref
    self.git_tag_branch = args.tag_branch
    self.env = args.env
    print(f"env={self.env}, git reference={self.git_ref}, git tag/branch={self.git_tag_branch}")

  def _get_jobs_list(self) -> dict:
    file_dir="cicd"
    jobs_dict = {}
    for file_name in os.listdir(file_dir):
      if file_name.endswith("job.json"):
          print(f"Job update for {file_name}")
          with open(os.path.join(file_dir, file_name)) as json_file:
            req_json = json.load(json_file)
            jobs_dict[file_name] = req_json
    return jobs_dict

  def _update_env_value(self, req_json) -> None:
    name = str(req_json['name'])
    req_json['name'] = name.replace('env', self.env)

  def _update_git_version(self, req_json) -> None:
    if self.git_ref == 'branch':
      req_json['git_source']['git_branch'] = self.git_tag_branch
    elif self.git_ref == 'tag':
      req_json['git_source']['git_tag'] = self.git_tag_branch
    else:
      req_json['git_source']['git_tag'] = 'main'

  def update_jobs(self) -> None:
    jobs_dict = self._get_jobs_list()
    job_create_resp = None
    for file_name, req_json in jobs_dict.items():
      self._update_env_value(req_json)
      self._update_git_version(req_json)
      existing_jobs = self.jobs_api._list_jobs_by_name(req_json['name'])
      if len(existing_jobs) == 1:
        self.reset_json_template['new_settings'] = req_json
        self.reset_json_template['job_id'] = existing_jobs[0]['job_id'] 
        print(f"reset the existing job {file_name} with details")
        print(self.reset_json_template)
        job_create_resp = self.jobs_api.reset_job(self.reset_json_template)
      else:
        print("created a new job with details ",file_name)
        print(req_json)
        job_create_resp = self.jobs_api.create_job(req_json)

      if self.run_now:
        print(f"running run now for the job {file_name}")
        self.jobs_api.run_now(job_id=job_create_resp['job_id'], notebook_params=None, 
        python_named_params=None, python_params=None, spark_submit_params=None, jar_params=None)


if __name__ == '__main__':
  update_obj = UpdateDatabricksJobs()
  update_obj.parse_args()
  update_obj.update_jobs()