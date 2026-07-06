import mlflow

experiment = mlflow.get_experiment_by_name(
    "SklearnLinearRegression"
)

runs = mlflow.search_runs(
    [experiment.experiment_id]
)

print(runs.T)