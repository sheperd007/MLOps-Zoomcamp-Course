# MLOps Zoomcamp — Course Work & Notes

Hands-on coursework for the [DataTalksClub MLOps Zoomcamp](https://github.com/DataTalksClub/mlops-zoomcamp), taking an ML model from notebook to production: experiment tracking, workflow orchestration, deployment, monitoring, and engineering best practices. Most modules build on the classic **NYC taxi trip-duration prediction** problem.

**Tech stack:** Python · scikit-learn · XGBoost · MLflow · Weights & Biases · Optuna · Prefect · Docker · Evidently · FastAPI · pytest · pandas / PyArrow

---

## Overview

Each numbered folder corresponds to a module of the Zoomcamp and contains the code, notebooks, and configuration produced while working through it. The running example is a regression model that predicts taxi-ride duration from NYC TLC trip-record data (Parquet), with later modules wrapping that model in orchestration, deployment, and monitoring tooling. The repository closes with a self-contained capstone project (`07-projects/`).

## What's inside

| Path | Module | Contents |
|------|--------|----------|
| `01-intro/` | Introduction | `duration-prediction.ipynb` — baseline regression on NYC taxi data (`DictVectorizer` + `LinearRegression` / `Lasso` / `Ridge`), RMSE evaluation. |
| `02-experiment-tracking/` | Experiment tracking | Two tracking backends. **MLflow**: `preprocess_data.py`, `hpo.py` (Optuna `TPESampler` hyper-parameter search over `RandomForestRegressor`), notebook `02.ipynb`. **Weights & Biases**: `train.py`, `sweep.py`, `preprocess_data.py` using W&B artifacts and sweeps. |
| `03-orchestration/` | Orchestration | `orchestrate.py` — a Prefect `@flow`/`@task` pipeline (read → feature engineering → XGBoost training → MLflow logging/registry). `prefect.yaml`, `deployment.yaml`, local `mlflow.db`, and sample green-taxi Parquet data. |
| `04-deployment/` | Deployment | Batch scoring with a pickled `model.bin` (`dv`, `model`): `starter.py` / `starter.ipynb` read a month of trips and write predictions. `Dockerfile.txt` builds on the course's `svizor/zoomcamp-model` base image. |
| `05-monitoring/` | Monitoring | `baseline_model_nyc_taxi_data.ipynb` — data-drift and quality monitoring with **Evidently** (`ColumnDriftMetric`, `DatasetDriftMetric`, `DatasetMissingValuesMetric`) over a `LinearRegression` baseline. |
| `06-best-practices/` | Best practices | Productionised batch job `batch.py` packaged with **Pipenv** (`Pipfile`/`Pipfile.lock`) and Docker; unit tests in `tests/test_batch.py` (**pytest**). Reads/writes Parquet, including S3 paths via `s3fs`. |
| `07-projects/1/` | Capstone | An end-to-end deployment project (FastAPI service + MLflow model loading) shipped via GitLab CI/CD onto a Docker Swarm cluster behind Traefik. See its own [README](07-projects/1/README.md) for the full design. |

## Methods / Approach

- **Modelling.** Trip duration is derived from pickup/dropoff timestamps and filtered to 1–60 minutes; pickup/dropoff location IDs are one-hot encoded with `DictVectorizer` and combined with `trip_distance`. Models range from linear regression baselines to `RandomForestRegressor` and `XGBoost`, evaluated with RMSE.
- **Experiment tracking.** Runs, parameters, metrics, and artifacts are logged to MLflow and Weights & Biases; hyper-parameter optimisation uses Optuna (TPE) and W&B sweeps.
- **Orchestration.** Training is expressed as a Prefect flow of retry-aware tasks and deployed through `prefect.yaml` / `deployment.yaml`.
- **Deployment.** The trained pipeline is serialised and run as a containerised batch scorer.
- **Monitoring.** Evidently reports track input drift and data-quality metrics against a reference dataset.
- **Engineering.** The batch job is dependency-pinned with Pipenv, containerised, and covered by pytest unit tests.

## How to run

> Each module is self-contained — `cd` into the folder before running its commands. NYC TLC Parquet files are downloaded from the public TLC / course datasets.

**Experiment tracking (MLflow + Optuna):**

```bash
cd 02-experiment-tracking/MLflow
python preprocess_data.py --raw_data_path <data> --dest_path ./output
mlflow server --backend-store-uri sqlite:///mlflow.db   # start the tracking server
python hpo.py --data_path ./output --num_trials 10
```

**Experiment tracking (Weights & Biases):**

```bash
cd 02-experiment-tracking/wandb
python train.py --wandb_project <project> --wandb_entity <entity> --data_artifact <artifact>
python sweep.py   # launch a W&B sweep
```

**Orchestration (Prefect):**

```bash
cd 03-orchestration
python orchestrate.py
prefect deploy   # uses prefect.yaml / deployment.yaml
```

**Deployment (batch scoring):**

```bash
cd 04-deployment
python starter.py <year> <month>
```

**Best practices (containerised batch + tests):**

```bash
cd 06-best-practices
pipenv install --dev
pytest tests/
docker build -t taxi-batch .
docker run taxi-batch <year> <month>
```

## Notes

This is a learning repository; some artifacts (W&B/MLflow run logs, local `mlflow.db`, cached Parquet and pickle files) are committed for reference and reproducibility rather than as a polished package. The capstone in `07-projects/1/` documents its own architecture and deployment steps.

## Links

- Course: [DataTalksClub MLOps Zoomcamp](https://github.com/DataTalksClub/mlops-zoomcamp)
- Data: [NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

## License

Released under the [MIT License](LICENSE).
