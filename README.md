# MLOps demo

This repo is intended to demonstrate an end-to-end ML experimentation and MLOps workflow on Databricks, where a model trained in development environment, and is then deployed in production.

Below points are touch based in this demo project:
1.  How to structure multiple ML Models codes in single project. 
2.  Continuation of Model Packgaing as Docker Image post Training & Model validation step. (Optional to keep in same project/code base)
3.  Usage of Databricks low level python API to implement CI/CD steps for MLOps.

---
## Pipeline

Each pipeline (e.g model training pipeline) is deployed as a [Databricks job](https://docs.databricks.com/data-engineering/jobs/jobs.html), where these jobs are deployed to a Databricks workspace using [Databricks Python API](https://docs.databricks.com/dev-tools/python-api.html) 

The ML Model training pipelines is defined as a json file (mlops-sample-demo/cicd/jobs/mlops_telco_churn_job.json). It has following steps:
- `setup`
    -   This task will help with setup and preparation of MLFlow experiments, feature tables & model registry
- `featurization`
    -   This step will read the input raw data, perform feature extraction and then write the data to feature tables. If required this step can alter the schema of feature tables and add tags and data sources to feature store.
- `ml training`
    -   Starts the ml training job to create ML Models and log the model to registry. It will try to resolve the envionrments from config and pickup the right hyper parameters to train the model.
- `model transition`
    -   The trained ML model is evaluated on base and realtime data. Then compared with existing model in production, based on the performance metrics the model is then transitioned to production stage and triggered next step of Docker image build.

---

## CI/CD Workflow

1. Run the notebooks in development environment to have a regular ML experiment experience.
2. Create and test the pipeline using Databricks Jobs UI and update the Job Json in the cicd/jobs section of the project.
3. Code is then committed to the development branch along with test cases.
4. Developer creates a pull request for the main branch. This will trigger a github action to perform unit and integration tests for the dev code base. [Continuous Integration]
5. Once all tests and review is completed, the pull request is merged to main branch.
6. The project owner will then create a release branch from main like `v1.0.0`. This will trigger a code deployment to the production envionrment [Continuous deployment of code]
7. Based on the github actions, the complete job will trigger which will include the steps from the above described pipeline. This would include
    * Model Ops for training the model, moving it to stage for validation and then moving it to production for deployment.

---

### Installing project requirements

```bash
pip install -r test-requirements.txt
```

#### Running unit tests

For unit testing, please use `pytest`:
```
pytest tests/unit --cov
```

Please check the directory `tests/unit` for more details on how to use unit tests.
In the `tests/unit/conftest.py` you'll also find useful testing primitives, such as local Spark instance with Delta support, local MLflow and DBUtils fixture.