from mlflow.tracking import MlflowClient

client = MlflowClient()
experiment = client.get_experiment_by_name("LinearRegressionScratch")
print(experiment)

runs = client.search_runs(
    experiment_ids=[experiment.experiment_id]
)

for run in runs:
    print(run.info.run_id)
    print(run.data.metrics)
    print(run.data.params)
    print("-" * 40)