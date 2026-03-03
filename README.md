# End to End Deep Learning Project - MLFLOW - DVC

## Workflows
1. Update config.yaml
2. Update secrets.yaml [Optional]
3. Update params.yaml
4. Update the entity
5. Update the configuration 
6. Update the components
7. Update the pipeline
8. Update the main.py
9. Update the dvc.yaml
10. app.py


# How to run?
### STEPS:
Clone the repository

https://github.com/sableen-kaur788/KideyDeepLearning

### STEP 01- Create a environment after opening the repository
```bash
python -m venv .venv
```
```bash
.venv/scripts/activate
```
### STEP 02- install the requirements
```bash
pip install -r requirements.txt
```
##### cmd
- mlflow ui

### dagshub
[dagshub](https://dagshub.com/)

```bash
export MLFLOW_TRACKING_URI "https://dagshub.com/sableen-kaur788/KideyDeepLearning.mlflow"
export MLFLOW_TRACKING_USERNAME "sableen-kaur"
export MLFLOW_TRACKING_PASSWORD ""
```

```bash
import dagshub
dagshub.init(repo_owner='sableen-kaur788', repo_name='KideyDeepLearning', mlflow=True)
import mlflow
with mlflow.start_run():
  mlflow.log_param('parameter name', 'value')
  mlflow.log_metric('metric name', 1)
```


### DVC cmd

1. dvc init
2. dvc repro
3. dvc dag


## About MLflow & DVC

MLflow

 - Its Production Grade
 - Trace all of your expriements
 - Logging & taging your model


DVC 

 - Its very lite weight for POC only
 - lite weight expriements tracker
 - It can perform Orchestration (Creating Pipelines)



