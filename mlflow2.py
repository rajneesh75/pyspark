import mlflow

experiment = mlflow.get_experiment_by_name("LinearRegressionScratch")
runs = mlflow.search_runs([experiment.experiment_id])
latest_run = runs.iloc[0]

learning_rate = float(latest_run["params.learning_rate"])
epochs = float(latest_run["params.epochs"])
print(f"learning_rate {learning_rate} epochs {epochs}")

slope = float(latest_run["params.slope"])
intercept = float(latest_run["params.intercept"])
print(f"slope {slope} intercept {intercept}")

hours_studied = 8
predicted_score = slope * hours_studied + intercept
print(predicted_score)